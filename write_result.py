import csv


def save_weapon_result(filename, data):
    with open(filename, 'w+') as csv_file:
        print('Saving weapons to ' + filename)
        writer = csv.writer(csv_file)
        writer.writerow(('Name', 'Item type', 'DPS', 'Damage range', 'Attack speed'))
        for item in data:
            for record in item:
                writer.writerow(record)
        print('Done !')


def save_armor_result(filename, data):
    with open(filename, 'w+') as csv_file:
        print('Saving armors to ' + filename)
        writer = csv.writer(csv_file)
        writer.writerow(('Name', 'Item type', 'Armor value', 'Set'))
        for item in data:
            for record in item:
                writer.writerow(record)
        print('Done !')