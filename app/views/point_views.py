from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect
from datetime import datetime, timedelta
import babel

from app import db
from app.models import Site, Point, Data
from app.forms import PointForm
from app.views.user_views import login_required

bp = Blueprint('point', __name__, url_prefix='/point')

from_date = '초기데이터'
to_date = '최종데이터'

@bp.route('/list/')
@login_required
def point_list():
    point_list = Point.query.order_by(Point.area.asc(), Point.number.asc()) # desc()
    return render_template('point/point_list.html', point_list=point_list)

@bp.route('/list_area/<area_choice>/')
@login_required
def point_list_area(area_choice):
    from app.defines import area_types
    area_types = area_types()

    if area_choice != "0":
        point_list = Point.query.filter(Point.area == area_choice).order_by(Point.number.asc()) # desc()
    else:
        point_list = Point.query.filter(Point.area == area_types[0][0]).order_by(Point.number.asc())  # desc()
    return render_template('point/point_list_area.html', point_list=point_list, area_types=area_types)

@bp.route('/list_point/<point_choice>/')
@login_required
def point_list_point(point_choice):
    from app.defines import point_types
    point_types = point_types()
    point_kind = []
    for point_type in point_types:
        for point in point_type:
            if point_kind.count(point[0]):
                pass
            else:
                point_kind.append(point[0])

    if point_choice != "0":
        point_list = Point.query.filter(Point.type == point_choice).order_by(Point.area.asc()) # desc()
    else:
        point_list = Point.query.filter(Point.type == point_types[0][0][0]).order_by(Point.area.asc())  # desc()
    return render_template('point/point_list_point.html', point_list=point_list, point_kind=point_kind)

@bp.route('/real/')
@login_required
def point_real():
    return render_template('point/point_real.html')

@bp.route('/create/', methods=('GET', 'POST'))
@login_required
def point_create():
    form = PointForm()
    if request.method == 'POST' and form.validate_on_submit():
        point = Point(area=form.area.data, number=form.number.data, type=form.type.data,
                      installdate=form.installdate.data, startdate=form.startdate.data,
                      enddate=form.enddate.data, locate=form.locate.data, active=form.active.data,
                      cst01=form.cst01.data, cst02=form.cst02.data, cst03=form.cst03.data,
                      cst04=form.cst04.data, cst05=form.cst05.data, cst06=form.cst06.data,
                      cst07=form.cst07.data, cst08=form.cst08.data, cst09=form.cst09.data,
                      cst10=form.cst10.data, cst11=form.cst11.data, cst12=form.cst12.data,
                      cst13=form.cst13.data, cst14=form.cst14.data, cst15=form.cst15.data )
        db.session.add(point)
        db.session.commit()
        return redirect(url_for('point.point_list'))
    return render_template('point/point_form.html', form=form)

@bp.route('/detail/<int:point_id>/')
@login_required
def point_detail(point_id):
    site = Site.query.get_or_404(1)
    point = Point.query.get_or_404(point_id)

    if from_date == "초기데이터" and to_date == "최종데이터":
        data_list = Data.query.filter_by(point_id=point_id).order_by(Data.measuringdate)
        data_list_ea = Data.query.filter_by(point_id=point_id).order_by(Data.measuringdate).count()
        data_list_org = Data.query.filter_by(point_id=point_id).order_by(Data.measuringdate)
    elif from_date == "초기데이터":
        data_list = Data.query.filter_by(point_id=point_id).\
            filter(Data.measuringdate <= to_date).order_by(Data.measuringdate)
        data_list_ea = Data.query.filter_by(point_id=point_id).\
            filter(Data.measuringdate <= to_date).order_by(Data.measuringdate).count()
        data_list_org = Data.query.filter_by(point_id=point_id).order_by(Data.measuringdate)
    elif to_date == "최종데이터":
        data_list = Data.query.filter_by(point_id=point_id).\
            filter(Data.measuringdate >= from_date).order_by(Data.measuringdate)
        data_list_ea = Data.query.filter_by(point_id=point_id).\
            filter(Data.measuringdate >= from_date).order_by(Data.measuringdate).count()
        data_list_org = Data.query.filter_by(point_id=point_id).order_by(Data.measuringdate)
    else:
        data_list = Data.query.filter_by(point_id=point_id).\
            filter(Data.measuringdate >= from_date).\
            filter(Data.measuringdate <= to_date).\
            order_by(Data.measuringdate)
        data_list_ea = Data.query.filter_by(point_id=point_id).\
            filter(Data.measuringdate >= from_date).\
            filter(Data.measuringdate <= to_date).\
            order_by(Data.measuringdate).count()
        data_list_org = Data.query.filter_by(point_id=point_id).order_by(Data.measuringdate)

    if data_list_ea != 0 :
        if point.type == "지중경사계":
            min_value = max_value = 0.0
            if data_list_org[-1]:
                for inclino in data_list_org[-1].data09.split(','):
                    if max_value < float(inclino): max_value = float(inclino)
                    if min_value > float(inclino): min_value = float(inclino)
                if abs(max_value) > abs(min_value):
                    point.cst16 = max_value
                else:
                    point.cst16 = min_value
                point.cst18 = abs(point.cst16 / point.cst01 * 100)
                db.session.commit()
            return render_template('point/point_detail.html', point=point, site=site, data_list=data_list, \
                                   data_list_ea=data_list_ea, from_date=from_date, to_date=to_date)
        else:
            old_date = data_list_org[0].measuringdate
            old_termDisplacement = 0
            for data in data_list_org:
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
                        data.data13 = float(data.data04 - data_list_org[0].data04)
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
            if point.type == "지하수위계":
                point.cst16 = data.data14
            else:
                point.cst16 = data.data13

            point.cst18 = abs(point.cst16 / point.cst01 * 100)
            db.session.commit()
            return render_template('point/point_detail.html', point=point, site=site, \
                                   data_list=data_list, data_list_ea=data_list_ea, \
                                   from_date=from_date, to_date=to_date)
    else:
        return render_template('point/point_detail.html', point=point, site=site, data_list=data_list, \
                               flowdate=0, data_list_ea=data_list_ea, from_date=from_date, to_date=to_date)

@bp.route('/modify/<int:point_id>', methods=('GET', 'POST'))
@login_required
def point_modify(point_id):
    point = Point.query.get_or_404(point_id)

    if request.method == 'POST':
        form = PointForm()
        if form.validate_on_submit():
            form.populate_obj(point)
            db.session.commit()
            return redirect(url_for('point.point_detail', point_id=point_id))
    else:
        form = PointForm(obj=point)
    return render_template('point/point_form.html', form=form)

@bp.route('/delete/<int:point_id>')
@login_required
def point_delete(point_id):
    point = Point.query.get_or_404(point_id)

    db.session.delete(point)
    db.session.commit()
    return redirect(url_for('point.point_list'))

@bp.route('/dateinit/<int:point_id>')
@login_required
def date_init(point_id):
    global from_date, to_date
    from_date = '초기데이터'
    to_date = '최종데이터'
    return redirect(url_for('point.point_detail', point_id=point_id))

@bp.route('/datemodify/<int:point_id>', methods=('POST',))
@login_required
def date_modify(point_id):
    global from_date, to_date
    from_date = request.form['from_date']
    to_date = request.form['to_date']+'a'
    return redirect(url_for('point.point_detail', point_id=point_id))

