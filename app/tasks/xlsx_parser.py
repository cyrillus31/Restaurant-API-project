import os
import shutil

import pandas as pd

file_path = 'admin/Menu.xlsx'
cwd = os.getcwd()
absolute_path = os.path.join(cwd, file_path)


def update_previous_state_file():
    shutil.copyfile(absolute_path, absolute_path+".tmp")


# def convert_to_dict(objects: list) -> dict:
    # return {object["id"]: object for object in objects}

def parser(from_previous_state: bool = False, absolute_path=absolute_path) -> dict:
    if from_previous_state:
        absolute_path += '.tmp'

    df = pd.read_excel(absolute_path, header=None)
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
            submenus[url_key] = {'id': id, 'title':title, 'description':description, 'menu_id': menu_id}
            submenu_id = id
        if pd.notna(row[3]) and type(row[2]) != str:
            id = str(row[2]).split('.')[0]
            title = row[3]
            description = row[4]
            price = str(row[5])
            url_key = f'menus/{menu_id}/submenus/{submenu_id}/dishes/{id}'
            dishes[url_key] = {'id': id, 'title': title, 'description': description,
                'price': price, 'submenu_id': submenu_id
            }


    # if target == 'menus':
        # return menus
    # elif target == 'submenus':
        # return submenus
    # elif target == 'dishes':
        # return dishes

    return {"menus": menus, "submenus": submenus, "dishes": dishes}



def get_objects_to_update_and_to_delete(prev_objects: dict, curr_objects: dict) -> dict:
    result = {"update" : [], "delete": []}
    if prev_objects == curr_objects:
        return result
    for key in prev_objects:
        if key not in curr_objects:
            result["delete"].append(prev_objects[key])
            continue 

        if prev_objects[key] != curr_objects[key]:
            result["update"].append({key: curr_objects[key]})
    return result
            



if __name__ == '__main__':
    menus, submenus, dishes = parser()
    print(menus, '\n')
    print(submenus, '\n')
    print(dishes, '\n')
