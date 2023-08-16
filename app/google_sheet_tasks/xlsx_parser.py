import os
import shutil

import openpyxl
import pandas as pd

file_path = os.path.join('admin', 'Menu.xlsx')
cwd = os.getcwd()
absolute_path = os.path.join(cwd, file_path)
absolute_path_to_temp = os.path.join(cwd, 'admin/.previous_state_menu.xlsx')


def create_temp_if_doesnt_exist():
    if not os.path.exists(absolute_path_to_temp):
        wb = openpyxl.Workbook()
        wb.save(absolute_path_to_temp)


def update_previous_state_file():
    shutil.copyfile(absolute_path, absolute_path_to_temp)


def parser(from_previous_state: bool = False, path_to_xlsx=absolute_path) -> dict:
    if from_previous_state:
        path_to_xlsx = absolute_path_to_temp
    df = pd.read_excel(path_to_xlsx, header=None)
    arr = df.to_numpy()

    menus = {}
    submenus = {}
    dishes = {}
    for row in arr:
        if pd.notna(row[0]):
            id = str(row[0]).split('.')[0]
            title = row[1]
            description = row[2]
            url_key = f'menus/{id}'
            menus[url_key] = {'id': id, 'title': title, 'description': description}
            menu_id = id
        if pd.notna(row[1]) and type(row[1]) != str:
            id = str(row[1]).split('.')[0]
            title = row[2]
            description = row[3]
            url_key = f'menus/{menu_id}/submenus/{id}'
            submenus[url_key] = {'id': id, 'title': title, 'description': description, 'menu_id': menu_id}
            submenu_id = id
        if pd.notna(row[3]) and type(row[2]) != str:
            id = str(row[2]).split('.')[0]
            title = row[3]
            description = row[4]
            price = str(row[5])
            url_key = f'menus/{menu_id}/submenus/{submenu_id}/dishes/{id}'
            dishes[url_key] = {
                'id': id, 'title': title, 'description': description, 'price': price, 'submenu_id': submenu_id
            }

    return {'menus': menus, 'submenus': submenus, 'dishes': dishes}


def get_objects_to_update_create_and_to_delete(prev_objects: dict, curr_objects: dict) -> dict:
    result: dict[str, dict] = {'update': {}, 'delete': {}, 'create': {}}
    if prev_objects == curr_objects:
        return result
    for key in prev_objects:
        if key not in curr_objects:
            result['delete'][key] = prev_objects[key]
            continue
        if prev_objects[key] != curr_objects[key]:
            result['update'][key] = curr_objects[key]
            continue
    for key in curr_objects:
        if key not in prev_objects:
            result['create'][key] = curr_objects[key]
    return result


if __name__ == '__main__':
    create_temp_if_doesnt_exist()
    print(absolute_path)
    print(parser(from_previous_state=False))
