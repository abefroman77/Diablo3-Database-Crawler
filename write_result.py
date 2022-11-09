import csv


def save_weapon_result(filename, data):
    with open(filename, 'w+') as csv_file:
        print('Saving weapons to ' + filename)
        writer = csv.writer(csv_file)
        writer.writerow(('Class', 'Name', 'Item type', 'Secondary Skill', 'Set', 'Set Skills', 'DPS', 'Damage range', 'Attack speed'))
        for item in data:
            for record in item:
                for x in record:
                    writer.writerow(x)
        print('Done !')


def save_armor_result(filename, data):
    with open(filename, 'w+') as csv_file:
        print('Saving armors to ' + filename)
        writer = csv.writer(csv_file)
        writer.writerow(('Class', 'Name', 'Item type', 'Armor value', 'Secondary Skill', 'Set', 'Set Skills'))
        for item in data:
            for record in item:
                for x in record:
                    writer.writerow(x)
        print('Done !')


def save_gem_result(filename, data):
    with open(filename, 'w+') as csv_file:
        print('Saving gems to ' + filename)
        writer = csv.writer(csv_file)
        writer.writerow(('Name', 'Secondary Skill'))
        for item in data:
            for record in item:
                for x in record:
                    writer.writerow(x)
        print('Done !')


def save_active_result(filename, data):
    with open(filename, 'w+') as csv_file:
        # print(f"Saving {data[0]} actives to " + filename)
        writer = csv.writer(csv_file)
        writer.writerow((
            'Class', 
            'Skill Name', 
            'Skill Description', 
            'Rune 1 Name', 
            'Rune 1 Description',
            'Rune 2 Name',
            'Rune 2 Description',
            'Rune 3 Name',
            'Rune 3 Description',
            'Rune 4 Name',
            'Rune 4 Description',
            'Rune 5 Name',
            'Rune 5 Description'
            ))
        for item in data:
            for record in item:
                writer.writerow(record)
        print('Done !')


def save_passive_result(filename, data):
    with open(filename, 'w+') as csv_file:
        # print(f"Saving {data[0]} passives to " + filename)
        writer = csv.writer(csv_file)
        writer.writerow((
            'Class', 
            'Skill Name', 
            'Skill Description'
            ))
        for item in data:
            for record in item:
                writer.writerow(record)
        print('Done !')