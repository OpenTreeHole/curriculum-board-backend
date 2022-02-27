from tortoise import fields
from tortoise.fields import ManyToManyRelation
from tortoise.models import Model


class CourseGroup(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    code = fields.TextField()
    department = fields.TextField()
    course_list: ManyToManyRelation["Course"] = fields.ManyToManyField(model_name="models.Course",
                                                                       related_name="course_groups")


class Course(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    code = fields.TextField()
    code_id = fields.TextField()
    credit = fields.FloatField()
    department = fields.TextField()
    teacher = fields.TextField()

    year = fields.TextField()
    """
    学年。如果是非秋季学期，则年数为（实际日期年数 - 1）。
    """

    semester = fields.IntField()
    """
    学期。
    1：秋季学期；
    2：（第二年的）寒假；
    3：（第二年的）春季学期；
    4：（第二年的）暑假
    """

    review_list: ManyToManyRelation["Review"] = fields.ManyToManyField(model_name="models.Review",
                                                                       related_name="courses")
    course_groups: fields.ManyToManyRelation[CourseGroup]


class Review(Model):
    id = fields.IntField(pk=True)
    title = fields.TextField()

    content = fields.TextField()
    reviewer_id = fields.IntField()
    time_created = fields.DatetimeField(auto_now_add=True)
    rank = fields.TextField()
    remark = fields.IntField()
    courses: fields.ManyToManyRelation[Course]
