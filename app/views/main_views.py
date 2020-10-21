from flask import Blueprint, url_for, render_template
from werkzeug.utils import redirect
from app.models import Site, Point, Data
from app.views.user_views import login_required

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/hello')
def hello_daon():
    return '다온에 오신것을 환영합니다!!'

@bp.route('/')
@login_required
def index():
    site = Site.query.get_or_404(1)

    from app.defines import point_types_total
    point_types_total = point_types_total()
    point_now = len(Point.query.all())
    point_per = point_now / point_types_total * 100
    point_progress = [point_types_total, point_now, point_per]

    cost_total = site.cost
    cost_now = site.endcost
    cost_per = cost_now / cost_total * 100
    cost_progress = [cost_total, cost_now, cost_per]

    if point_now > 8:
        point_list = Point.query.order_by(Point.cst18.desc())[0:8]
    else:
        point_list = Point.query.order_by(Point.cst18.desc())

    point = Point.query.get_or_404(point_list[0].id)
    data_list = Data.query.filter_by(point_id=point.id).order_by(Data.measuringdate)
    data_list_ea = Data.query.filter_by(point_id=point.id).order_by(Data.measuringdate).count()

    return render_template('main/main_dashboard.html', site=site, point_list=point_list, point=point, \
                           data_list=data_list, data_list_ea=data_list_ea, \
                           point_progress=point_progress, cost_progress=cost_progress)