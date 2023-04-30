import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup

SITE_URL = 'https://us.diablo3.blizzard.com'
SITE_ITEMS_URL = 'https://us.diablo3.blizzard.com/en-us/item'
LEGENDARY_ITEM_CLASS = {'class': 'd3-color-orange'}
SET_ITEM_CLASS = {'class': 'd3-color-green'}

async def get_armor_links():
    async with aiohttp.ClientSession() as session:
        async with session.get(SITE_ITEMS_URL + '/') as resp:
            html = await resp.text()
            html = BeautifulSoup(html, 'html.parser')

            # Finding first column
            armor_column = html.find('div', {'class': 'column-1'})

            # Finding first half-column
            armor_column1 = armor_column.find('div', {'class': 'half-column'})
            armor_links = {link.attrs['href'] for link in armor_column1.find_all('a')}

            # Adding links for armor items from second column
            armor_column2 = armor_column1.findNextSibling('div', {'class': 'half-column'})
            for link in armor_column2.find_all('a'):
                armor_links.add(link.attrs['href'])

            armor_coroutines = [scrape_armor_items(SITE_URL + link) for link in armor_links]
            armor_result = await asyncio.gather(*armor_coroutines)
            return armor_result


async def scrape_armor_items(url):
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

                    # Finding armor value
                    try:
                        item_value = item.find('ul', {'class': 'item-armor-weapon'}).li.span.get_text()
                        # item_data.append(item_value)
                    except:
                        item_value = 'None'
                    item_data.append(item_value)

                    # If it has a secondary skill, get skill text
                    if 'Set' not in item_type:
                        try:
                            item_skill = item.find('span', {'class': 'd3-color-ffff8000'}).get_text()
                            try:
                                item_skill += item.find('span', {'class': 'd3-color-ffff8000'}).find_next('span', {'class': 'd3-color-ffff0000'}).get_next()
                            except:
                                None
                        except AttributeError:
                            item_skill = 'None'
                        # Get specific class, if any
                        try:
                            class_specific = item.find('span', {'class': 'd3-color-ffff0000'}).get_text()
                            class_specific = class_specific[1:]
                            class_specific_list = class_specific.split(" Only")
                            class_specific = class_specific_list[0]
                        except:
                            class_specific = "All"
                        item_data.insert(0, class_specific)
                    else:
                        item_skill = 'None'
                        class_specific = "Set" # for filtering later - class not in item page
                        item_data.insert(0, class_specific)
                    item_data.append(item_skill)

                    # If it's a set item, get set name
                    if 'Set' in item_type:
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
                    else:
                        setStr = 'None'
                    item_data.append(setStr)

                    # If the item is from a set or has a secondary skill, add to the item array
                    if item_skill != 'None' or setStr != 'None':
                        items_array.append(item_data)

            return items_array

