from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.fields import TextField, IntField, FloatField, ManyToManyRelation, DatetimeField
from tortoise.models import Model


class Course(Model):
    id: IntField = fields.IntField(pk=True)
    name: TextField = fields.TextField()
    credit: FloatField = fields.FloatField()

    review_list: ManyToManyRelation["Review"] = fields.ManyToManyField(model_name="models.Review",
                                                                       related_name="courses")


class Review(Model):
    id: IntField = fields.IntField(pk=True)
    title: TextField = fields.TextField()
    reviewer_id: IntField = fields.IntField()
    time_created: DatetimeField = fields.DatetimeField(auto_now_add=True)
    rank: TextField = fields.TextField()
    remark: IntField = fields.IntField()
    courses: fields.ManyToManyRelation[Course]