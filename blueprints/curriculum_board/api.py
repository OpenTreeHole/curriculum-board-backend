from typing import Optional, List

from sanic import Request, response, json
from sanic.exceptions import NotFound
from sanic_ext import validate
from sanic_ext.extensions.openapi import openapi
from sanic_ext.extensions.openapi.definitions import RequestBody
from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from blueprints import bp_curriculum_board
from blueprints.auth.decorator import authorized
from models import Review, Course

Tortoise.init_models(["blueprints.curriculum_board.api"], "models")

NewReviewPyd = pydantic_model_creator(Review, exclude=("id", "reviewer_id", "time_created", "courses"))
ReviewPyd = pydantic_model_creator(Review, include=("id", "reviewer_id", "time_created"))

CoursePyd = pydantic_model_creator(Course)
NewCoursePyd = pydantic_model_creator(Course, exclude=("id", "review_list"))



@bp_curriculum_board.post("/courses")
@openapi.body(
    RequestBody({"application/json": NewCoursePyd.construct()}))
@authorized()
@validate(json=NewCoursePyd)
async def add_course(request: Request, body: NewCoursePyd):
    course_added = await Course.create(**body.dict())
    print(str(CoursePyd.schema()))
    return json((await CoursePyd.from_tortoise_orm(course_added)).dict())


@bp_curriculum_board.get("/courses/<course_id:int>")
@authorized()
async def get_course(request: Request,course_id: int):
    course: Optional[Course] = await Course.get_or_none(id=course_id)
    if course is None:
        raise NotFound(f"Course with id {course_id} is not found")
    return json((await CoursePyd.from_tortoise_orm(course_added)).dict())

@bp_curriculum_board.post("/courses/<course_id:int>/reviews")
@openapi.body(
    RequestBody({"application/json": NewReviewPyd.construct(title="title", content="content", rank="C+", remark=10)}))
@authorized()
@validate(json=NewReviewPyd)
async def add_review(request: Request, body: NewReviewPyd, course_id: int):
    this_course: Optional[Course] = await Course.get_or_none(id=course_id)
    if this_course is None:
        raise NotFound(f"Course with id {course_id} is not found")

    review_added: Review = await Review.create(**body.dict(), reviewer_id=request.ctx.user_id)
    await this_course.review_list.add(review_added)
    return json((await ReviewPyd.from_tortoise_orm(review_added)).dict())


@bp_curriculum_board.get("/courses/<course_id:int>/reviews")
@authorized()
async def get_reviews(_: Request, course_id: int):
    this_course: Optional[Course] = await Course.get_or_none(id=course_id)
    if this_course is None:
        raise NotFound(f"Course with id {course_id} is not found")

    reviews: list[Review] = await this_course.review_list.all()
    return json([(await ReviewPyd.from_tortoise_orm(r)).dict() for r in reviews])
