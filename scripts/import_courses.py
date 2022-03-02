import asyncio
import json
import re
from typing import Pattern, Match, Optional

from tortoise import Tortoise

from config import database_config

LESSON_JSON = r"D:\Download\lessons(1)\lessons\lessons_364.json"


def extract_semester_from_str(semester_str: str) -> int:
    semester_pattern: Pattern[str] = re.compile(r'(\d+)学期', re.I)
    match = semester_pattern.search(semester_str)
    if '寒' in semester_str or '冬' in semester_str:
        return 2
    if '暑' in semester_str or '夏' in semester_str:
        return 4
    if match.group(1) == '1':
        return 1
    elif match.group(1) == '2':
        return 3
    return -1


async def main():
    await Tortoise.init(config=database_config)
    await Tortoise.generate_schemas()
    with open(LESSON_JSON, 'r', encoding='utf8') as fp:
        year_pattern: Pattern[str] = re.compile(r'(\d+)-(\d+)学年', re.I)
        json_data = json.load(fp)
        json_course: dict
        for json_course in json_data:
            year_matches: Optional[Match[str]] = year_pattern.search(json_course['semester'])
            from models import Course, CourseGroup
            group: Optional[CourseGroup] = await CourseGroup.get_or_none(code=json_course['code'])
            body_dict = {'name': json_course['name'], 'code': json_course['code'], 'code_id': json_course['code_id'],
                         'department': json_course['department'], 'teachers': json_course['teachers'],
                         'max_student': json_course['max_student'], 'week_hour': json_course['week_hour'],
                         'credit': json_course['credit'],
                         'year': year_matches.group(1),
                         'semester': extract_semester_from_str(json_course['semester'])}
            if group is None:
                group = await CourseGroup.create(**body_dict)

            course_added = await Course.create(**body_dict)
            await group.course_list.add(course_added)
            print(json_course['code'])


if __name__ == "__main__":
    asyncio.run(main())
