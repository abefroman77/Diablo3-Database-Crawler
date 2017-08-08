from scraper_core import get_all_results
from write_result import save_weapon_result, save_armor_result

weapon_results, armor_results = get_all_results()
save_weapon_result('results/weapon_data.csv', weapon_results)
save_armor_result('results/armor_data.csv', armor_results)
