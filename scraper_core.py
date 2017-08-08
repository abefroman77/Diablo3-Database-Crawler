import asyncio
import aiohttp
from bs4 import BeautifulSoup


SITE_URL = 'https://us.battle.net'
SITE_ITEMS_URL = 'https://us.battle.net/d3/en/item'
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
            armor_column = armor_column.find('div', {'class': 'half-column'})
            armor_links = {link.attrs['href'] for link in armor_column.find_all('a')}

            # Adding links for armor items from second column
            armor_links.add('/d3/en/item/pants/')
            armor_links.add('/d3/en/item/boots/')
            armor_coroutines = [scrape_armor_items(SITE_URL + link) for link in armor_links]
            armor_result = await asyncio.gather(*armor_coroutines)
            return armor_result


async def get_weapon_links():
    async with aiohttp.ClientSession() as session:
        async with session.get(SITE_ITEMS_URL + '/') as resp:
            html = await resp.text()
            html = BeautifulSoup(html, 'html.parser')
            weapons_column = html.find('div', {'class': 'column-2'})
            weapon_links = {link.attrs['href'] for link in weapons_column.find_all('a')}
            weapon_coroutines = [scrape_weapon_items(SITE_URL + link) for link in weapon_links]
            weapons_result = await asyncio.gather(*weapon_coroutines)
            return weapons_result


async def scrape_armor_items(url):
    print('Scraping ' + url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            html = await resp.text()
            html = BeautifulSoup(html, 'html.parser')
            items_html = html.findAll('div', {'class': 'item-details-text'})
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
                    item_value = item.find('ul', {'class': 'item-armor-weapon'}).li.p.span.get_text()
                    item_data.append(item_value)

                    # If it's a set item, get set name
                    try:
                        item_set = item.find('li', {'class': 'item-itemset-name'}).span.get_text()
                    except AttributeError:
                        item_set = 'None'
                    item_data.append(item_set)

                    items_array.append(item_data)

            return items_array


async def scrape_weapon_items(url):
    print('Scraping ' + url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            html = await resp.text()
            html = BeautifulSoup(html, 'html.parser')
            items_html = html.findAll('div', {'class': 'item-details-text'})
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

                    # Finding DPS
                    item_dps = item.find('li', {'class': 'big'})
                    item_dps = item_dps.find('span', {'class': 'value'}).get_text()
                    item_data.append(item_dps)

                    # Finding damage range
                    damage_range_html = item.find('ul', {'class': 'item-weapon-damage'})
                    damage_range = ''
                    for i, element in enumerate(damage_range_html.li.p.children):
                        if i == 0:
                            damage_range = element.get_text() + '-' + element.next_sibling.next_sibling.get_text()
                    item_data.append(damage_range)

                    # Finding attack speed
                    attack_speed = ''
                    for element in damage_range_html.li.next_sibling.next_sibling.p.span:
                        attack_speed = element
                    item_data.append(attack_speed)

                    items_array.append(item_data)

            return items_array


def get_all_results():
    loop = asyncio.get_event_loop()
    yield loop.run_until_complete(get_weapon_links())
    yield loop.run_until_complete(get_armor_links())
    loop.close()











