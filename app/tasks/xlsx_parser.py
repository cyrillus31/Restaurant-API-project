import os
import shutil

import pandas as pd

file_path = 'admin/Menu.xlsx'
cwd = os.getcwd()
absolute_path = os.path.join(cwd, file_path)


def update_previous_state_file():
    shutil.copyfile(absolute_path, absolute_path+".tmp")


def convert_to_dict(objects: list) -> dict:
    return {object["id"]: object for object in objects}

def parser(target: str | None = None, from_previous_state: bool = False):
    if from_previous_state:
        absolute_path += '.tmp'


    df = pd.read_excel(absolute_path, header=None)
    arr = df.to_numpy()

    menus = []
    submenus = []
    dishes = []
    for row in arr:
        if pd.notna(row[0]):
            menu = {'id': str(row[0]).split('.')[0], 'title': row[1], 'description': row[2]}
            menus.append(menu)
            menu_id = menu['id']
        if pd.notna(row[1]) and type(row[1]) != str:
            submenu = {'id': str(row[1]), 'title': row[2], 'description': row[3], 'menu_id': menu_id}
            submenus.append(submenu)
            submenu_id = submenu['id']
        if pd.notna(row[3]) and type(row[2]) != str:
            dish = {'id': str(row[2]), 'title': row[3], 'description': row[4],
                    'price': str(row[5]), 'submenu_id': submenu_id}
            dishes.append(dish)

    menus = convert_to_dict(menus)
    submenus = convert_to_dict(submenus)
    dishes = convert_to_dict(dishes)

    if target == 'menus':
        return menus
    elif target == 'submenus':
        return submenus
    elif target == 'dishes':
        return dishes

    return menus, submenus, dishes


pmenus, psubmenus, pdishes = parser(from_previous_state=True)
menus, submenus, dishes = parser()

def get_objects_to_update_and_to_delete(prev_objects: dict, curr_objects: dict) -> list:
    if prev_objects == curr_objects:
        return []
            




if __name__ == '__main__':
    menus, submenus, dishes = parser()
    print(menus, '\n')
    print(submenus, '\n')
    print(dishes, '\n')
