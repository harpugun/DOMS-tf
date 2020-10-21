from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect
from datetime import datetime, timedelta
import babel

from app import db
from app.models import Site, Point, Data
from app.forms import AnalysisDateForm
from app.views.user_views import login_required

bp = Blueprint('analysis', __name__, url_prefix='/analysis')

analfromdate = '2020-01-01'
analtodate = '2030-12-31'

@bp.route('/set/', methods=('GET', 'POST'))
@login_required
def anal_dateset():
    from app.defines import area_types, point_types
    area_types = area_types()
    point_types = point_types()
    area_type = []
    point_type = []
    point_choice = []

    for area, area_no in zip(area_types, range(len(area_types))):
        point1 = []
        point2 = []
        area_type.append(area[0])
        for point in point_types[area_no]:
            point1.append(point[0])
            point2.append([point[0],point[0]])
        point_type.append(point1)
        point_choice.append(point2)

    form = AnalysisDateForm()
    form.analarea.choices = area_types
    form.analpoint.choices = point_choice[0] # 나중에 손보자
    if request.method == 'POST' and form.validate_on_submit():
        global analfromdate, analtodate
        analfromdate = form.analfromdate.data
        analtodate = form.analtodate.data
        analarea = form.analarea.data
        analpoint = form.analpoint.data
        return redirect(url_for('analysis.anal_analysis', analarea=analarea, analpoint=analpoint))
    return render_template('analysis/analysis_form.html', form=form, area_type=area_type, point_type=point_type)

@bp.route('/')
@login_required
def anal_analysis():
    from app.defines import area_types, point_types
    area_types = area_types()
    point_types = point_types()
    area_type = []
    point_type = []
    point_choice = []
    analysis_list = []
    analysis_total = []
    forindex = 0

    anal_area = request.args.get('analarea')
    anal_point = request.args.get('analpoint')

    at_gap_min = at_gap_max = at_full_min = at_full_max = at_per_min = at_per_max = 0

    units = {
        '지중경사계': 'mm',
        '지하수위계': 'm',
        '구조물경사계': 'Degree',
        '균열측정계': 'mm',
        '지표침하계': 'mm',
        '하중계': 'Ton',
        '변형률계': '㎏/㎠'
    }

    for area, area_no in zip(area_types, range(len(area_types))):
        point1 = []
        point2 = []
        area_type.append(area[0])
        for point in point_types[area_no]:
            point1.append(point[0])
            point2.append([point[0],point[0]])
        point_type.append(point1)
        point_choice.append(point2)

    point_list = Point.query.filter(Point.area==anal_area).filter(Point.type==anal_point).order_by(Point.number)
    for point in point_list:
        if Data.query.filter_by(point_id=point.id).filter(Data.measuringdate >= analfromdate).\
            filter(Data.measuringdate <= analtodate + timedelta(days=1)).order_by(Data.measuringdate).count():
            data_init = Data.query.filter_by(point_id=point.id).order_by(Data.measuringdate).first()
            data_start = Data.query.filter_by(point_id=point.id).\
                filter(Data.measuringdate >= analfromdate ).\
                order_by(Data.measuringdate).first()
            data_end = Data.query.filter_by(point_id=point.id).\
                filter(Data.measuringdate <= analtodate + timedelta(days=1)). \
                order_by(Data.measuringdate.desc()).first()

            a_area = point.area # area
            a_type = point.type # point type
            a_number = point.number # point name
            a_date_from = data_start.measuringdate
            a_date_to = data_end.measuringdate
            a_days = (data_end.measuringdate - data_start.measuringdate).days
            a_standard = point.cst01 # 관리기준
            a_data_deep = 0

            # 전주/금주 측정 Data
            if point.type != "지중경사계":
                if point.type == "하중계" or point.type == "변형률계":
                    a_data_init = round(data_init.data04,3)
                    a_data_last = round(data_start.data04,3)
                    a_data_now = round(data_end.data04,3)
                else:
                    a_data_init = round(data_init.data01,3)
                    a_data_last = round(data_start.data01,3)
                    a_data_now = round(data_end.data01,3)
            else:
                ver_data_last = list(map(float, list(data_start.data09.split(","))))
                ver_data_now = list(map(float, list(data_end.data09.split(","))))
                a_data_init = 0.00
                a_data_now = round(max(ver_data_now),2)
                a_data_last = round(ver_data_last[ver_data_now.index(max(ver_data_now))], 2)
                a_data_deep = round((len(ver_data_now)-ver_data_now.index(max(ver_data_now))+1)/2-0.5,1)


            a_gap_month = round(a_data_now - a_data_last,3)
            a_gap_total = round(a_data_now - a_data_init,3)
            if point.type == "지표침하계":
                a_gap_month = round(a_gap_month*1000, 1)
                a_gap_total = round(a_gap_total*1000, 1)

            a_per = abs(round(a_gap_total/a_standard*100,2))
            if point.type == "지하수위계":
                if abs(a_gap_month/a_days) < point.cst01: a_safe = '안전'
                else: a_safe = '위험'
                a_per = abs(round((a_gap_month/a_days) / a_standard * 100, 2))
            else:
                if abs(a_gap_total) < point.cst01: a_safe = '안전'
                elif point.cst02 > abs(a_gap_total) >= point.cst01: a_safe = '주의'
                elif point.cst03 > abs(a_gap_total) >= point.cst02: a_safe = '경고'
                elif abs(a_gap_total) >= point.cst03: a_safe = '위험'

            analysis_list.append([a_area, a_type, a_number, \
                                  a_date_from, a_date_to, a_days, \
                                  a_data_init, a_data_last, a_data_now, a_data_deep, \
                                  a_gap_month, a_gap_total,  a_standard, a_per, a_safe])
            forindex = forindex+1
            if forindex == 1 :
                at_gap_min = at_gap_max = a_gap_month
                at_full_min = at_full_max = a_gap_total
                at_per_min = at_per_max = a_per


            if at_gap_min > a_gap_month : at_gap_min = a_gap_month
            if at_gap_max < a_gap_month : at_gap_max = a_gap_month
            if at_full_min > a_gap_total: at_full_min = a_gap_total
            if at_full_max < a_gap_total: at_full_max = a_gap_total
            if at_per_min > a_per: at_per_min = a_per
            if at_per_max < a_per: at_per_max = a_per

    if forindex > 0 :
        analysis_total.extend([at_gap_min,at_gap_max,at_full_min,at_full_max,at_per_min,at_per_max])

    return render_template('analysis/analysis.html', analfromdate=analfromdate, analtodate=analtodate, \
                           area_type=area_type, point_type=point_type, analysis_list=analysis_list, \
                           anal_area=anal_area, anal_point=anal_point, analysis_total=analysis_total, \
                           forindex=forindex, units=units)

