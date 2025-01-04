from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validate, validates_schema, ValidationError
from .models import User, Report, Prayer, Study, Outreach, Followup

################################################
# User Schema
################################################

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ("password_hash",)

    password = fields.Str(load_only=True, required=True)
    is_admin = fields.Boolean(dump_only=True)

################################################
# Prayer Schema
################################################

class PrayerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Prayer
        load_instance = True

    prayer_group_day = fields.Str(validate=validate.OneOf(
        ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
    ), allow_none=True)

    @validates_schema
    def validate_times(self, data, **kwargs):
        start = data.get("prayer_chain_start")
        end = data.get("prayer_chain_end")
        if start and end and start >= end:
            raise ValidationError("prayer_chain_start must be before prayer_chain_end", "prayer_chain_start")

################################################
# Study Schema
################################################

class StudySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Study
        load_instance = True

    study_content = fields.Str(validate=validate.Length(max=2000))

################################################
# Outreach Schema
################################################

class OutreachSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Outreach
        load_instance = True

    total_reached = fields.Int(validate=validate.Range(min=0))
    saved = fields.Int(validate=validate.Range(min=0))
    healed = fields.Int(validate=validate.Range(min=0))

    @validates_schema
    def validate_outreach(self, data, **kwargs):
        if data.get('saved',0) > data.get('total_reached',0):
            raise ValidationError("saved cannot exceed total_reached", "saved")

################################################
# Followup Schema
################################################

class FollowupSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Followup
        load_instance = True

################################################
# Report Schema
################################################

class ReportSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Report
        load_instance = True

    prayers = fields.List(fields.Nested(PrayerSchema), required=False)
    studies = fields.List(fields.Nested(StudySchema), required=False)
    outreaches = fields.List(fields.Nested(OutreachSchema), required=False)
    followups = fields.List(fields.Nested(FollowupSchema), required=False)