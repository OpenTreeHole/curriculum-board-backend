from sanic import Request
from sanic.exceptions import NotFound
from sanic_ext import validate
from sanic_ext.extensions.openapi import openapi
from sanic_ext.extensions.openapi.definitions import RequestBody
from tortoise.contrib.pydantic import pydantic_model_creator
from blueprints import bp_curriculum_board
from blueprints.auth.decorator import authorized
from models import Review, Course

new_review = pydantic_model_creator(Review, exclude=("id", "reviewer_id", "time_created", "courses"))
review = pydantic_model_creator(Review, exclude=("courses",))


@bp_curriculum_board.post("/course/<course_id:int>/reviews")
@openapi.body(
    RequestBody({"application/json": new_review.construct(title="title", content="content", rank="C+", remark=10)}))
@authorized()
@validate(json=new_review)
async def add_review(request: Request, body: new_review, course_id: int):
    this_course: Course | None = await Course.get_or_none(id=course_id)
    if this_course is None:
        raise NotFound(f"Course with id {course_id} is not found")

    review_added: Review = await Review.create(**body.dict(), reviewer_id=request.ctx.user_id)
    await this_course.review_list.add(review_added)
    return (await review.from_tortoise_orm(review_added)).json()
