from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect
from datetime import datetime
import openpyxl

from app import db
from app.models import Site, Point, Data
from app.forms import PointForm
from app.views.user_views import login_required

bp = Blueprint('paper', __name__, url_prefix='/paper')

@bp.route('/week/')
@login_required
def paper_week():
    point_list = Point.query.all()
    return render_template('paper/paper_week.html', point_list=point_list)

@bp.route('/print_data/<int:point_id>, how_page, from_dateg, to_dateg')
@login_required
def data_print(point_id):
    site = Site.query.get_or_404(1)
    point = Point.query.get_or_404(point_id)
    page_type = request.args.get('how_page')
    from_date = request.args.get('from_dateg')
    to_date = request.args.get('to_dateg')

    if from_date == "초기데이터" and to_date == "최종데이터":
        data_list = Data.query.filter_by(point_id=point_id).order_by(Data.measuringdate)
        data_list_ea = Data.query.filter_by(point_id=point_id).order_by(Data.measuringdate).count()
    elif from_date == "초기데이터":
        data_list = Data.query.filter_by(point_id=point_id).\
            filter(Data.measuringdate <= to_date).order_by(Data.measuringdate)
        data_list_ea = Data.query.filter_by(point_id=point_id).\
            filter(Data.measuringdate <= to_date).order_by(Data.measuringdate).count()
    elif to_date == "최종데이터":
        data_list = Data.query.filter_by(point_id=point_id).\
            filter(Data.measuringdate >= from_date).order_by(Data.measuringdate)
        data_list_ea = Data.query.filter_by(point_id=point_id).\
            filter(Data.measuringdate >= from_date).order_by(Data.measuringdate).count()
    else:
        data_list = Data.query.filter_by(point_id=point_id).\
            filter(Data.measuringdate >= from_date).\
            filter(Data.measuringdate <= to_date).\
            order_by(Data.measuringdate)
        data_list_ea = Data.query.filter_by(point_id=point_id).\
            filter(Data.measuringdate >= from_date).\
            filter(Data.measuringdate <= to_date).\
            order_by(Data.measuringdate).count()

    if data_list_ea != 0 :
        if point.type == "지중경사계":
            min_value = max_value = 0.0
            if data_list[-1]:
                for inclino in data_list[-1].data09.split(','):
                    if max_value < float(inclino): max_value = float(inclino)
                    if min_value > float(inclino): min_value = float(inclino)
                if abs(max_value) > abs(min_value):
                    point.cst16 = max_value
                else:
                    point.cst16 = min_value
                db.session.commit()
            return render_template('paper/data_print.html', point=point, site=site, data_list=data_list, \
                                   data_list_ea=data_list_ea, from_date=from_date, to_date=to_date)
        else:
            old_date = data_list[0].measuringdate
            old_termDisplacement = 0
            for data in data_list:
                data.data11 = (datetime.strptime(str(data.measuringdate), "%Y-%m-%d %H:%M:%S") - datetime.strptime(str(point.startdate), "%Y-%m-%d")).days
                data.data12 = (datetime.strptime(str(data.measuringdate), "%Y-%m-%d %H:%M:%S") - datetime.strptime(str(old_date), "%Y-%m-%d %H:%M:%S")).days

                if point.type == "지하수위계":
                    data.data13 = (data.data01 - data_list[0].data01)
                    if data.data12 != 0:
                        data.data14 = (data.data13 - old_termDisplacement) / data.data12
                    else:
                        data.data14 = 0

                if point.type == "하중계":
                    data.data04 = point.cst12*(point.cst13-(data.data01+data.data02+data.data03))

                if point.type == "지표침하계":
                    data.data13 = (data.data01 - data_list[0].data01) * 1000
                elif point.type == "하중계":
                    if Data.query.filter_by(point_id=point_id).count()  > 1:
                        data.data13 = float(data.data04 - data_list[0].data04)
                    else:
                        data.data13 = 0
                else:
                    data.data13 = (data.data01 - data_list[0].data01)

                if point.type == "변형률계":
                    data.data04 = data.data13/1000000 * point.cst11
                    data.data15 = data.data04 - old_termDisplacement
                    old_termDisplacement = data.data04
                else:
                    data.data15 = data.data13 - old_termDisplacement
                    old_termDisplacement = data.data13
                old_date = data.measuringdate
            db.session.commit()
            if point.type == "지하수위계": point.cst16 = data.data14
            else: point.cst16 = data.data13
            db.session.commit()
            return render_template('paper/data_print.html', point=point, site=site, data_list=data_list, \
                                   data_list_ea=data_list_ea, from_date=from_date, to_date=to_date, page_type=page_type)
    else:
        return render_template('paper/data_print.html', point=point, site=site, data_list=data_list,\
                               flowdate=0, data_list_ea=data_list_ea, \
                               from_date=from_date, to_date=to_date, page_type=page_type)