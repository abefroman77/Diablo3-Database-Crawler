import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup

SITE_URL = 'https://us.diablo3.blizzard.com'
SITE_CLASSES_URL = 'https://us.diablo3.blizzard.com/en-us/class'

async def get_active_links(class_type):
    async with aiohttp.ClientSession() as session:
        url = SITE_CLASSES_URL + '/' + class_type + '/active/'
        async with session.get(url) as resp:
            html = await resp.text()
            html = BeautifulSoup(html, 'html.parser')
            # Finding table body
            tbody = html.find('tbody')

            # Finding links
            active_links = {link.attrs['href'] for link in tbody.find_all('a')}

            active_coroutines = [scrape_active_skills(SITE_URL + link) for link in active_links]
            active_result = await asyncio.gather(*active_coroutines)
            return active_result


async def scrape_active_skills(url):
    print('Scraping ' + url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            html = await resp.text()
            html = BeautifulSoup(html, 'html.parser')
            container = html.find('div', {'class': 'skill-left'})
            items_html = container.find_all('div', {'class':'rune-details'})
            items_array = []

            # Add class to array
            items_array.append(html.find('div', {'class': 'page-header'}).h2.a.get_text())
            
            # Add skill name to array
            name = html.find('h2', {'class': 'subheader-2'}).get_text()
            items_array.append(name.strip())
            
            # Add skill description
            item_str = ''
            descriptions = container.select('.skill-desc p')
            for desc in descriptions:
                if desc != descriptions[0]:
                    item_str += ' - '
                item_str += desc.get_text()
            items_array.append(item_str)
            
            # Loop through runes
            for item in items_html:
                # Add rune name
                item_name = item.find('h3', {'class':'subheader-3'}).get_text()
                items_array.append(item_name)

                # Add rune description
                div = item.find('div', {'class':'rune-desc'})
                p_tags = div.find_all('p')
                item_desc = ''
                for p in p_tags:
                    item_desc += p.get_text()
                items_array.append(item_desc)

            return items_array

