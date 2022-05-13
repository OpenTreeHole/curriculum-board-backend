import asyncio
import json
from typing import Optional

from tortoise import Tortoise

from config import database_config

LESSON_JSON = r"D:\Code\FDUCourseData\data\insert\insert.json"


async def main():
    await Tortoise.init(config=database_config)
    await Tortoise.generate_schemas()
    with open(LESSON_JSON, 'r', encoding='utf8') as fp:
        json_data = json.load(fp)
        json_course: dict
        for json_course in json_data:
            from models import Course, CourseGroup
            group: Optional[CourseGroup] = await CourseGroup.get_or_none(code=json_course['code'])
            body_dict = {'name': json_course['name'], 'code': json_course['code'], 'code_id': json_course['no'],
                         'department': json_course['department'], 'teachers': json_course['teachers'],
                         'max_student': json_course['maxStudent'], 'week_hour': json_course['weekHour'],
                         'credit': json_course['credits'], 'campus_name': json_course['campusName'],
                         'year': 2021,
                         'semester': 3}
            if group is None:
                group = await CourseGroup.create(**body_dict)

            course_added = await Course.create(**body_dict)
            await group.course_list.add(course_added)


if __name__ == "__main__":
    asyncio.run(main())
