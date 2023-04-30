import asyncio
import aiohttp
import requests
import time
from bs4 import BeautifulSoup

SITE_URL = 'https://us.diablo3.blizzard.com'
SITE_ITEMS_URL = 'https://us.diablo3.blizzard.com/en-us/item'
LEGENDARY_ITEM_CLASS = {'class': 'd3-color-orange'}
SET_ITEM_CLASS = {'class': 'd3-color-green'}

async def get_weapon_links():
    async with aiohttp.ClientSession() as session:
        async with session.get(SITE_ITEMS_URL + '/') as resp:
            html = await resp.text()
            html = BeautifulSoup(html, 'html.parser')

            # Get weapon links from column 2
            weapons_column = html.find('div', {'class': 'column-2'})
            weapon_links = {link.attrs['href'] for link in weapons_column.find_all('a')}

            weapon_coroutines = [scrape_weapon_items(SITE_URL + link) for link in weapon_links]
            weapons_result = await asyncio.gather(*weapon_coroutines)
            return weapons_result


async def scrape_weapon_items(url):
    print('Scraping ' + url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            html = await resp.text()
            html = BeautifulSoup(html, 'html.parser')
            items_html = html.find_all('div', {'class': 'item-details-text'})
            items_array = []
            for item in items_html:
                # Finding legendary item
                item_class = LEGENDARY_ITEM_CLASS
                name = item.find('a', item_class)

                # If item is not legendary, trying to find set item
                if not name:
                    item_class = SET_ITEM_CLASS
                    name = item.find('a', item_class)
                if name:
                    # Creating record for item
                    item_data = []
                    item_data.append(name.get_text())

                    # Finding item type
                    item_type = item.find('ul', {'class': 'item-type'})
                    item_type = item_type.find('span', item_class).get_text()
                    item_data.append(item_type)

                    # If it has a secondary skill, get skill text
                    try:
                        item_skill = item.find('ul', {'class': 'item-effects'}).span.get_text()
                        try:
                            item_skill += item.find('span', {'class': 'd3-color-ffff8000'}).find_next('span', {'class': 'd3-color-ffff0000'}).get_next()
                        except:
                            None
                    except AttributeError:
                        item_skill = 'None'
                    if item_skill == '':
                        item_skill = 'None'
                    item_data.append(item_skill)

                    # Navigate to item page
                    try:
                        item_link = item.h3.a['href']
                    except AttributeError:
                        item_link = 'None'
                        item_set = 'None'
                    else:
                        item_link = 'https://us.diablo3.blizzard.com' + item_link
                        data = requests.get(item_link)
                        item_link_html = BeautifulSoup(data.text, 'html.parser')
                    
                    try:
                        class_specific = item_link_html.find('li', {'class': 'item-class-specific'}).a.get_text().strip()
                    except:
                        class_specific = "All"
                    item_data.insert(0, class_specific)

                    # If it's a set item, get set name
                    if 'Set' in item_type:
                        try:
                            item_set = item_link_html.find('li', {'class': 'item-itemset-name'}).span.p.span.get_text()    
                        except AttributeError:
                            item_set = 'None'
                    else:
                        item_set = 'None'
                    
                    item_data.append(item_set)

                    # If it's a set item, get set skills
                    setStr = ''
                    if 'Set' in item_type:
                        try:
                            item_set_skill = item.select('.item-itemset span')
                            for span in item_set_skill:
                                setStr += span.get_text()
                        except AttributeError:
                            setStr = 'None'
                            # item_data.append(setStr)
                    else:
                        setStr = 'None'

                    if setStr == '':
                        setStr = 'None'
                    item_data.append(setStr)

                    # Finding DPS
                    item_dps = item.find('li', {'class': 'big'})
                    item_dps = item_dps.find('span', {'class': 'value'}).get_text()
                    item_data.append(item_dps)

                    # Finding damage range
                    item_weapon_damage = item.select('.item-weapon-damage > li > span > p')
                    damage_range = item_weapon_damage[0].get_text()
                    item_data.append(damage_range)

                    # Finding attack speed
                    attack_speed = item_weapon_damage[1].get_text()
                    item_data.append(attack_speed)

                    if item_skill != 'None' or setStr != 'None':
                        items_array.append(item_data)

                #time.sleep(1)
            return items_array