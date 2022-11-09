import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup

SITE_URL = 'https://us.diablo3.blizzard.com'
SITE_CLASSES_URL = 'https://us.diablo3.blizzard.com/en-us/class'

async def get_passive_links(class_type):
    passive_links = [SITE_CLASSES_URL + '/' + class_type + '/passive/']

    passive_coroutines = [scrape_passive_skills(link) for link in passive_links]
    passive_result = await asyncio.gather(*passive_coroutines)
    return passive_result


async def scrape_passive_skills(url):
    print('Scraping ' + url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            html = await resp.text()
            html = BeautifulSoup(html, 'html.parser')
            # container = html.find('div', {'class': 'skill-left'})
            items_html = html.find_all('div', {'class':'skill-details'})
            items_array = []

            # Add class to array
            items_array.append(html.find('div', {'class':'page-header'}).h2.a.get_text())
            
            # Loop through skills
            for item in items_html:
                # Add rune name
                item_name = item.find('h3', {'class':'subheader-3'}).a.get_text()
                items_array.append(item_name)

                # Add rune description
                div = item.find('div', {'class':'skill-description'})
                p_tags = div.find_all('p')
                item_desc = ''
                for p in p_tags:
                    # print(p)
                    item_desc += p.get_text()
                items_array.append(item_desc)

            return items_array