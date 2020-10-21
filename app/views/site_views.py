from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect
from datetime import datetime


from .. import db
from app.models import Site, Point
from app.forms import SiteForm
from app.views.user_views import login_required

bp = Blueprint('site', __name__, url_prefix='/site')


@bp.route('/')
@login_required
def site_detail():
    site = Site.query.get_or_404(1)
    return render_template('site/site_detail.html', site=site)

@bp.route('/map')
@login_required
def site_map():
    site = Site.query.get_or_404(1)
    return render_template('site/site_map.html', site=site)

@bp.route('/modify/<int:site_id>', methods=('GET', 'POST'))
@login_required
def site_modify(site_id):
    site = Site.query.get_or_404(site_id)
    '''
    if g.user.power != "admin":
        flash('수정권한이 없습니다')
        return redirect(url_for('site.site_detail', site_id=site_id))
    '''
    if request.method == 'POST':
        form = SiteForm()
        if form.validate_on_submit():
            form.populate_obj(site)
            db.session.commit()
            return redirect(url_for('site.site_detail', site_id=site_id))
    else:
        form = SiteForm(obj=site)
    return render_template('site/site_form.html', form=form)

@bp.route('/volume')
@login_required
def site_volume():
    from app.defines import area_types, point_types
    area_types = area_types()
    point_types = point_types()
    site = Site.query.get_or_404(1)

    area_table = []
    for point_type,area_type in zip(point_types,area_types):
        for point_type2 in point_type:
            pointea = Point.query.filter(Point.area == area_type[0], Point.type == point_type2[0]).count()
            point_type2.append(pointea)
        area_table.append(len(point_type))

    return render_template('site/site_volume.html',
                           area_types = area_types, point_types = point_types,
                           site=site, area_table=area_table )

@bp.route('/frequency')
@login_required
def site_frequency():
    site = Site.query.get_or_404(1)
    return render_template('site/site_frequency.html', site=site)

@bp.route('/standard')
@login_required
def site_standard():
    site = Site.query.get_or_404(1)
    return render_template('site/site_standard.html', site=site)

@bp.route('/progress')
@login_required
def site_progress():
    site = Site.query.get_or_404(1)
    date_total = ((datetime.strptime(str(site.enddate), "%Y-%m-%d") - datetime.strptime(str(site.startdate), "%Y-%m-%d"))).days
    date_now = (datetime.now() - datetime.strptime(str(site.startdate), "%Y-%m-%d")).days
    dete_per = date_now / date_total * 100
    dete_progress = [date_total, date_now, dete_per]

    from app.defines import point_types_total
    point_types_total = point_types_total()
    point_now = len(Point.query.all())
    point_per = point_now / point_types_total * 100
    point_progress = [point_types_total, point_now, point_per]

    cost_total = site.cost
    cost_now = site.endcost
    cost_per = cost_now / cost_total * 100
    cost_progress = [cost_total, cost_now, cost_per]
    return render_template('site/site_progress.html', site=site, dete_progress=dete_progress,
                           point_progress=point_progress, cost_progress=cost_progress)