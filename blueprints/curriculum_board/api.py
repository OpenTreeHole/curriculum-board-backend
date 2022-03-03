from typing import Optional, Dict, Any, List

from sanic import Request, text
from sanic.exceptions import NotFound, Unauthorized
from sanic_ext import validate
from sanic_ext.extensions.openapi import openapi
from sanic_ext.extensions.openapi.definitions import RequestBody

from blueprints import bp_curriculum_board
from blueprints.auth.decorator import authorized
from models import Review, Course, CourseGroup
from utils.sanic_helper import jsonify_response, jsonify_list_response
from utils.tortoise_fix import pmc, pqc

NewReviewPyd = pmc(Review, exclude=("id", "reviewer_id", "time_created", "courses"))
GetReviewPyd = pmc(Review, exclude=("courses", "reviewer_id"))

NewCoursePyd = pmc(Course, exclude=("id", "review_list", "course_groups"))
GetCoursePyd = pmc(Course, exclude=("review_list.reviewer_id", "course_groups"))

GetSingleCourseGroupPyd = pmc(CourseGroup, exclude=("course_list.review_list.reviewer_id",))
GetMultiCourseGroupsPyd = pmc(CourseGroup, exclude=("course_list.review_list", "course_list.course_groups"))


@bp_curriculum_board.get("/courses")
@openapi.description("### Get all course groups (i.e. courses with the same code).")
@openapi.response(
    200,
    {
        "application/json": [GetMultiCourseGroupsPyd.construct(course_list=[GetCoursePyd.construct()])],
    }
)
@authorized()
async def get_course_groups(request: Request):
    course_groups: list[CourseGroup] = await CourseGroup.all()
    return await jsonify_list_response(GetMultiCourseGroupsPyd, course_groups)


@bp_curriculum_board.post("/courses")
@openapi.body(
    RequestBody({"application/json": NewCoursePyd.construct()})
)
@openapi.description("### Add a new course.")
@openapi.response(
    200,
    {
        "application/json": GetCoursePyd.construct(review_list=[GetReviewPyd.construct()]),
    }
)
@authorized()
@validate(json=NewCoursePyd)
async def add_course(request: Request, body: NewCoursePyd):
    body_dict: dict[str, Any] = body.dict()
    group: Optional[CourseGroup] = await CourseGroup.get_or_none(code=body_dict['code'])
    if group is None:
        group = await CourseGroup.create(**body_dict)

    course_added = await Course.create(**body_dict)
    await group.course_list.add(course_added)

    return await jsonify_response(GetCoursePyd, course_added)


@bp_curriculum_board.get("/courses/<course_id:int>")
@openapi.description("### Get a course object with given course id.")
@openapi.response(
    200,
    {
        "application/json": GetCoursePyd.construct(review_list=[GetReviewPyd.construct()]),
    }
)
@authorized()
async def get_course(request: Request, course_id: int):
    course: Optional[Course] = await Course.get_or_none(id=course_id)
    if course is None:
        raise NotFound(f"Course with id {course_id} is not found")
    return await jsonify_response(GetCoursePyd, course)


@bp_curriculum_board.post("/courses/<course_id:int>/reviews")
@openapi.body(
    RequestBody({
        "application/json": NewReviewPyd.construct(
            title="review title",
            content="review content",
            rank="B+",
            remark=9
        )
    })
)
@openapi.description("### Add a new review on course with given course id.")
@openapi.response(
    200,
    {
        "application/json": GetReviewPyd.construct()
    }
)
@authorized()
@validate(json=NewReviewPyd)
async def add_review(request: Request, body: NewReviewPyd, course_id: int):
    this_course: Optional[Course] = await Course.get_or_none(id=course_id)
    if this_course is None:
        raise NotFound(f"Course with id {course_id} is not found")

    review_added: Review = await Review.create(**body.dict(), reviewer_id=request.ctx.user_id)
    await this_course.review_list.add(review_added)
    return await jsonify_response(GetReviewPyd, review_added)


@bp_curriculum_board.delete("/reviews/<review_id:int>")
@openapi.description("### Delete a review with given review id.")
@openapi.response(
    200,
    {
        "text/plain": "Successfully remove review with id: 1."
    }
)
@authorized()
async def remove_review(request: Request, review_id: int):
    this_review: Optional[Review] = await Review.get_or_none(id=review_id)
    if this_review is None:
        raise NotFound(f"Review with id {review_id} is not found")
    if request.ctx.user_id != this_review.reviewer_id and not request.ctx.is_admin:
        raise Unauthorized("You have no permission to remove this review!")
    await this_review.delete()
    return text(f"Successfully remove review with id: {review_id}.")


@bp_curriculum_board.put("/reviews/<review_id:int>")
@openapi.body(
    RequestBody({
        "application/json": NewReviewPyd.construct(
            title="review title",
            content="review content",
            rank="B+",
            remark=9
        )
    })
)
@openapi.description("### Edit a review with given review id.")
@openapi.response(
    200,
    {
        "application/json": GetReviewPyd.construct()
    }
)
@authorized()
async def modify_review(request: Request, body: NewReviewPyd, review_id: int):
    this_review: Optional[Review] = await Review.get_or_none(id=review_id)
    if this_review is None:
        raise NotFound(f"Review with id {review_id} is not found")
    if request.ctx.user_id != this_review.reviewer_id and not request.ctx.is_admin:
        raise Unauthorized("You have no permission to remove this review!")
    await this_review.update_from_dict(**body.dict())
    return await jsonify_response(GetReviewPyd, this_review)


@bp_curriculum_board.get("/courses/<course_id:int>/reviews")
@openapi.description("### Get all reviews on course with given course id.")
@openapi.response(
    200,
    {
        "application/json": [GetReviewPyd.construct()]
    }
)
@authorized()
async def get_reviews(_: Request, course_id: int):
    this_course: Optional[Course] = await Course.get_or_none(id=course_id)
    if this_course is None:
        raise NotFound(f"Course with id {course_id} is not found")

    reviews: list[Review] = await this_course.review_list.all()
    return await jsonify_list_response(GetReviewPyd, reviews)
