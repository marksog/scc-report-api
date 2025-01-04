from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import extract
from datetime import datetime, timedelta
from app.models import Report
from app.schemas import ReportSchema

summaries_bp = Blueprint('summaries', __name__)
report_schema = ReportSchema(many=True)

def get_sunday(date_obj):
    # If Sunday is day=6 in date_obj.weekday(), offset accordingly
    offset = (date_obj.weekday() + 1) % 7
    return date_obj - timedelta(days=offset)

@summaries_bp.route('/weekly', methods=['GET'])
@jwt_required()
def weekly_summary():
    user_id = get_jwt_identity()
    date_str = request.args.get('date')
    if not date_str:
        return jsonify({"error": "Date parameter is required"}), 400
    
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    sunday = get_sunday(date_obj)
    saturday = sunday + timedelta(days=6)

    reports = Report.query.filter(
        Report.user_id == user_id,
        Report.date >= sunday,
        Report.date <= saturday
    ).all()

@summaries_bp.route('/monthly', methods=['GET'])    
@jwt_required()
def monthly_summary():
    user_id = get_jwt_identity()
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    if not year or not month:
        return jsonify({"error": "Year and month parameters are required"}), 400
    
    reports = Report.query.filter(
        Report.user_id == user_id,
        extract('year', Report.date) == year,
        extract('month', Report.date) == month
    ).all()
    return jsonify(report_schema.dump(reports)), 200

@summaries_bp.route('/yearly', methods=['GET'])
@jwt_required()
def yearly_summary():
    user_id = get_jwt_identity()
    year = request.args.get('year', type=int)
    if not year:
        return jsonify({"error": "Year parameter is required"}), 400
    reports =  Report.query.filter(
        Report.user_id == user_id,
        extract('year', Report.date) == year
    ).all()
    return jsonify(report_schema.dump(reports)), 200