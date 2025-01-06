from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Report, Prayer, Study, Outreach, Followup
from app.schemas import PrayerSchema, StudySchema, OutreachSchema, FollowupSchema, ReportSchema
from marshmallow import ValidationError
import logging

reports_bp = Blueprint('reports', __name__)
report_schema = ReportSchema()
prayer_schema = PrayerSchema()
study_schema = StudySchema()
outreach_schema = OutreachSchema()
followup_schema = FollowupSchema()

@reports_bp.route('/reports', methods=['POST'])
@jwt_required()
def create_report():
    user_id = get_jwt_identity()
    data = request.get_json()

    # Expect { "date": "YYYY-MM-DD", "prayers": [...], "studies": [...], "outreaches": [...], "followups": [...] }
    try:
        validated = report_schema.load(data, session = db.session)
    except ValidationError as err:
        return jsonify({"error_reports": err.messages}), 422
    
    new_report = Report(
        user_id=user_id,
        date=validated.date
    )
    db.session.add(new_report)
    db.session.flush()  # Flush to get the new report ID (repot.id)

    # Add prayers
    for p in validated.prayers:
        prayer_data = prayer_schema.dump(p)
        prayer_obj = Prayer(report_id=new_report.id, **prayer_data)
        db.session.add(prayer_obj)

    # Add studies
    for s in validated.studies:
        study_data = study_schema.dump(s)
        study_obj = Study(report_id=new_report.id, **study_data)
        db.session.add(study_obj)
    
    # Add outreaches
    for o in validated.outreaches:
        outreach_data = outreach_schema.dump(o)
        outreach_obj = Outreach(report_id=new_report.id, **outreach_data)
        db.session.add(outreach_obj)
    
    # Add followups 
    for f in validated.followups:
        followup_data = followup_schema.dump(f)
        followup_obj = Followup(report_id=new_report.id, **followup_data)
        db.session.add(followup_obj)
    
    db.session.commit()
    return jsonify(report_schema.dump(new_report)), 201

@reports_bp.route('/<int:report_id>', methods=['PUT'])
@jwt_required()
def edit_report(report_id):
    user_id = get_jwt_identity()
    report = Report.query.filter_by(id=report_id, user_id=user_id).first()
    if not report:
        return jsonify({"error": "Report not found or not yours"}), 404

    data = request.get_json()

    try:
        if "date" in data:
            report.date = data["date"]
    except Exception as e:
        logging.error(f"Error updating report date: {e}")
        return jsonify({"error": "Error updating report date"}), 400
    
    try:
        if "prayers" in data:
            for p in data["prayers"]:
                prayer = Prayer.query.get(p.get("id"))
                if prayer:
                    prayer.prayer_chain_start = p.get("prayer_chain_start")
                    prayer.prayer_chain_end = p.get("prayer_chain_end")
                    prayer.prayer_group_day = p.get("prayer_group_day")
                    prayer.prayer_group_start = p.get("prayer_group_start")
                    prayer.prayer_group_end = p.get("prayer_group_end")
                else:
                    prayer_obj = Prayer(report_id=report.id, **p)
                    db.session.add(prayer_obj)
    except Exception as e:
        logging.error(f"Error updating prayers: {e}")
        return jsonify({"error": "Error updating prayers"}), 400
    
    try:
        if "outreach" in data:
            for s in data["outreaches"]:
                study = Study.query.get(s.get("id"))
                if study:
                    study.total_reached = s.get("total_reached")
                    study.already_saved = s.get("already_saved")
                    study.saved = s.get("saved")
                    study.saved_and_filled = s.get("saved_and_filled")
                    study.already_saved_and_filled = s.get("already_saved_and_filled")
                    study.healed = s.get("healed")
                    study.outreach_comments = s.get("outreach_comments")
                else:
                    study_obj = Study(report_id=report.id, **s)
                    db.session.add(study_obj)
    except Exception as e:
        logging.error(f"Error updating outreaches: {e}")
        return jsonify({"error": "Error updating outreaches"}), 400
    
    try:
        if "followups" in data:
            for f in data["followups"]:
                followup = Followup.query.get(f.get("id"))
                if followup:
                    followup.followup_persons = f.get("followup_persons")
                    followup.followup_details = f.get("followup_details")
                else:
                    followup_obj = Followup(report_id=report.id, **f)
                    db.session.add(followup_obj)
    except Exception as e:
        logging.error(f"Error updating followups: {e}")
        return jsonify({"error": "Error updating followups"}), 400
    
    db.session.commit()
    return jsonify(report_schema.dump(report)), 200