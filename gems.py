import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup

SITE_URL = 'https://us.diablo3.blizzard.com'
SITE_GEMS_URL = 'https://us.diablo3.blizzard.com/en-us/item/gem'

async def get_gem_links():
    async with aiohttp.ClientSession() as session:
        async with session.get(SITE_GEMS_URL + '/') as resp:
            html = await resp.text()
            html = BeautifulSoup(html, 'html.parser')

            # Get weapon links from column 2
            gems_container = html.find('div', {'class': 'row1'})
            gems_links = {link.attrs['href'] for link in gems_container.find_all('a')}

            gems_coroutines = [scrape_gems_items(SITE_URL + link) for link in gems_links]
            gems_result = await asyncio.gather(*gems_coroutines)
            return gems_result


async def scrape_gems_items(url):
    print('Scraping ' + url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            html = await resp.text()
            html = BeautifulSoup(html, 'html.parser')
            items_html = html.find_all('div', {'class': 'detail-text'})
            items_array = []
            for item in items_html:
                name = item.h2

                if name != None:
                    # Creating record for item
                    item_data = []
                    item_data.append(name.get_text())

                    # Finding item secondary skill
                    item_skill = item.find('span', {'class': 'd3-color-ffff8000'})
                    item_skill = item_skill.get_text()
                    item_data.append(item_skill)

                    items_array.append(item_data)

            return items_array