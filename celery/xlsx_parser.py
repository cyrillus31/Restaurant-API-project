import pandas as pd

df = pd.read_excel(r"C:\\Users\\Kirill\\Desktop\\PROGRAMMING\\Projects\\ylab_university\\1homework\\admin\\Menu.xlsx", header=None)

arr = df.to_numpy()


def parser(target: str = None):
    menus = []
    submenus = []
    dishes = []
    for row in arr:
        if pd.notna(row[0]):
            menu = {"id": row[0], "title": row[1], "description": row[2]}
            menus.append(menu)
            menu_id = menu["id"]
        if pd.notna(row[1]) and type(row[1]) != str:
            submenu = {"id": row[1], "title": row[2], "description": row[3], "menu_id": menu_id}
            submenus.append(submenu)
            submenu_id = submenu["id"]
        if pd.notna(row[3]) and type(row[2]) != str:
            dish = {"id": row[1], "title": row[3], "description": row[4], "price": row[5], "submenu_id": submenu_id}
            dishes.append(dish)
    if target == "menus":
        return menus
    elif target == "submenus":
        return submenus
    elif target == "dishes":
        return dishes
    return menus, submenus, dishes        

if __name__ == "__main__":
    menus, submenus, dishes = parser()
    print(menus, "\n")
    print(submenus, "\n")
    print(dishes, "\n")