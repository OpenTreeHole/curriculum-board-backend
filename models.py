from tortoise import fields
from tortoise.fields import TextField, IntField, FloatField, ManyToManyRelation, DatetimeField
from tortoise.models import Model


class Course(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    credit = fields.FloatField()

    review_list: ManyToManyRelation["Review"] = fields.ManyToManyField(model_name="models.Review",
                                                                       related_name="courses")


class Review(Model):
    id = fields.IntField(pk=True)
    title = fields.TextField()
    reviewer_id = fields.IntField()
    time_created: DatetimeField = fields.DatetimeField(auto_now_add=True)
    rank = fields.TextField()
    remark = fields.IntField()
    courses: fields.ManyToManyRelation[Course]
