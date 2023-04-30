import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup
from armor import get_armor_links, scrape_armor_items
from weapons import get_weapon_links, scrape_weapon_items
from gems import get_gem_links, scrape_gems_items
from active import get_active_links, scrape_active_skills
from passive import get_passive_links, scrape_passive_skills

SITE_URL = 'https://us.diablo3.blizzard.com/'
SITE_ITEMS_URL = 'https://us.diablo3.blizzard.com/en-us/item'
SITE_CLASSES_URL = 'https://us.diablo3.blizzard.com/en-us/class'
SITE_GEMS_URL = 'https://us.diablo3.blizzard.com/en-us/item/gem'
LEGENDARY_ITEM_CLASS = {'class': 'd3-color-orange'}
SET_ITEM_CLASS = {'class': 'd3-color-green'}

class_links = [
    'barbarian', 
    'crusader', 
    'demon-hunter', 
    'monk', 
    'necromancer', 
    'witch-doctor', 
    'wizard'
    ]

def get_all_results():
    loop = asyncio.get_event_loop()
    yield loop.run_until_complete(get_weapon_links())
#    yield loop.run_until_complete(get_armor_links())
#    yield loop.run_until_complete(get_gem_links())
#    for link in class_links:
#        yield loop.run_until_complete(get_active_links(link))
#        yield loop.run_until_complete(get_passive_links(link))
    loop.close()











