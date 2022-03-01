import asyncio
import json
import os

from tortoise import Tortoise

from config import model_modules, database_config

LESSON_JSON = r"D:\Download\lessons(1)\lessons\lessons_364.json"


async def main():
    await Tortoise.init(config=database_config)
    with open(LESSON_JSON, 'r', encoding='utf8') as fp:
        json_data = json.load(fp)
        json_course: dict
        for json_course in json_data:
            from models import Course
            await Course.create(name=json_course['name'], credit=json_course['credit'])  # TODO Extract all fields
            # TODO create or insert to the course group


if __name__ == "__main__":
    asyncio.run(main())
