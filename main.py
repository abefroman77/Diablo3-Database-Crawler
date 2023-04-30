from scraper_core import get_all_results
from write_result import save_weapon_result, save_armor_result, save_gem_result, save_active_result, save_passive_result

weapon_results, armor_results, gem_results, active_results, passive_results = get_all_results()

save_weapon_result('results/weapon_data.csv', weapon_results)
save_armor_result('results/armor_data.csv', armor_results)
save_gem_result('results/gem_data.csv', gem_results)
save_active_result('results/active_data.csv', active_results)
save_passive_result('results/passive_data.csv', passive_results)