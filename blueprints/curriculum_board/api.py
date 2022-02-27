from typing import Optional, Dict, Any

from sanic import Request
from sanic.exceptions import NotFound
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

NewCoursePyd = pmc(Course, exclude=("id", "review_list"))
GetCoursePyd = pmc(Course, exclude=("review_list.reviewer_id",))

GetSingleCourseGroupPyd = pmc(CourseGroup, exclude=("course_list.review_list.reviewer_id",))
GetMultiCourseGroupsPyd = pqc(CourseGroup,
                              exclude=(
                                  "course_list.review_list",))  # TODO: Can we call .json(),.dict() upon pqc, like pmc?


# TODO: get course group list and return a GetMultiCourseGroupsPyd
# TODO: delete review (with user authorization confirmed)
# TODO: update review (with user authorization confirmed)

@bp_curriculum_board.post("/courses")
@openapi.body(
    RequestBody({"application/json": NewCoursePyd.construct()})
)
@openapi.description("Add a new course.")
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
@openapi.description("Get a course object with given course id.")
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
@openapi.description("Add a new review on course with given course id.")
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


@bp_curriculum_board.get("/courses/<course_id:int>/reviews")
@openapi.description("Get all reviews on course with given course id.")
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
