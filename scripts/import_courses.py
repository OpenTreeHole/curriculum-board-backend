import asyncio
import json
from typing import Optional

from tortoise import Tortoise

from config import database_config

LESSON_JSON = r"D:\Code\curriculum-board-backend\scripts\387.json"


async def main():
    await Tortoise.init(config=database_config)
    await Tortoise.generate_schemas()
    with open(LESSON_JSON, 'r', encoding='utf8') as fp:
        json_data = json.load(fp)
        json_course: dict
        for json_course in json_data:
            from models import Course, CourseGroup
            no: str = json_course['no']
            group: Optional[CourseGroup] = await CourseGroup.get_or_none(code=no[:-3])

            body_dict = {'name': json_course['name'], 'code': no[:-3], 'code_id': no,
                         'department': json_course['department'], 'teachers': json_course['teachers'],
                         # 'max_student': json_course['maxStudent'],
                         'credit': json_course['credits'],
                         'year': 2021,
                         'semester': 3,
                         'campus_name': '', 'max_student': 0,'week_hour':0}
            if group is None:
                group = await CourseGroup.create(**body_dict)

            course_added = await Course.create(**body_dict)
            await group.course_list.add(course_added)


if __name__ == "__main__":
    asyncio.run(main())
