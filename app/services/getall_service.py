from fastapi import Depends

from app.utils import dish2dict, menu2dict, submenu2dict

from .. import models, schemas
from ..repositories import (
    DishRepository,
    MenuRepository,
    NotificationRepository,
    SubmenuRepository,
    TreeCacheRepository,
)


class GetAllService:
    def __init__(
        self,
        menu_repo: MenuRepository = Depends(),
        submenu_repo: SubmenuRepository = Depends(),
        dish_repo: DishRepository = Depends(),
    ) -> None:

        self.menu_repo = menu_repo
        self.submenu_repo = submenu_repo
        self.dish_repo = dish_repo
        self.cache_repository = TreeCacheRepository

    async def get_all(self, url_key: str,):
        result = {'all menus': []}
        cached_response = await self.cache_repository.get_tree(url_key)

        if cached_response:
            print('cache list hit')
            return cached_response

        async def get_related_submenus_list(menu_id=None) -> list:
            return await self.submenu_repo.get_all(menu_id=menu_id)

        async def get_related_dish_list(submenu_id=None) -> list:
            return await self.dish_repo.get_all(submenu_id=submenu_id)

        all_menus = await self.menu_repo.get_all()

        async def all_sumbenus_func() -> list:
            pass

        for menu in all_menus:
            related_submenus = await get_related_submenus_list(menu.id)
            result['all menus'].append({'menu': menu2dict(menu), 'submenus':
                                        [{'submenu': submenu, 'dishes': [dish for dish in map(dish2dict, await get_related_dish_list(submenu['id']))]}
                                         for submenu in map(submenu2dict, related_submenus)]})

        await self.cache_repository.add_tree(url_key, result)

        return result
