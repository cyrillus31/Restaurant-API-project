from app.database import async_session, get_session
from app import models
from xlsx_parser import parser
import asyncio
import os
import sys

path = os.getcwd()
print(path)
sys.path.append(path)


menus, submenus, dishses = parser()


async def main():
    async with async_session() as session:
        for menu in menus:
            new_menu = models.Menu(**menu)
            session.add(new_menu)
            await session.commit()

asyncio.run(main())
