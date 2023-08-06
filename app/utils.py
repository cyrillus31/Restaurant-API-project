from . import models


def menu2dict(model: models.Menu) -> dict:
    result = {
        'id': model.id,
        'description': model.description,
        'title': model.title,
        'submenus_count': model.submenus_count,
        'dishes_count': model.dishes_count,
    }
    return result


def submenu2dict(model: models.Submenu) -> dict:
    result = {
        'id': model.id,
        'description': model.description,
        'title': model.title,
        'dishes_count': model.dishes_count,
    }
    return result


def dish2dict(model: models.Submenu) -> dict:
    result = {
        'id': model.id,
        'description': model.description,
        'title': model.title,
        'price': model.price,
    }
    return result
