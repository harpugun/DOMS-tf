from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from app import db
from app.models import Site, Point, Data
from app.forms import DataForm, DataVerticalForm, DataLoadcellForm
from app.views.user_views import login_required

bp = Blueprint('data', __name__, url_prefix='/data')


@bp.route('/create/<int:point_id>', methods=('GET', 'POST'))
@login_required
def data_create(point_id):
    point = Point.query.get_or_404(point_id)

    if point.type == "지중경사계":
        form = DataVerticalForm()
    elif point.type == "하중계":
        form = DataLoadcellForm()
    else:
        form = DataForm()

    if request.method == 'POST' and form.validate_on_submit():
        if point.type == '지중경사계':
            data = Data(measuringdate=form.measuringdate.data, data09=form.data09.data)
        elif point.type == "하중계":
            data = Data(measuringdate=form.measuringdate.data, data01=form.data01.data,
                        data02=form.data02.data, data03=form.data03.data)
        else:
            data = Data(measuringdate=form.measuringdate.data, data01=form.data01.data)
        point.data_set.append(data)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('point.point_detail', point_id=point_id))

    if point.type == '지중경사계':
        return render_template('data/vertical_form.html', form=form)
    else:
        return render_template('data/data_form.html', form=form)

@bp.route('/modify/<int:data_id>', methods=('GET', 'POST'))
@login_required
def data_modify(data_id):
    data = Data.query.get_or_404(data_id)

    if request.method == 'POST':
        if data.point.type == '지중경사계':
            form = DataVerticalForm()
        elif data.point.type == "하중계":
            form = DataLoadcellForm()
        else:
            form = DataForm()

        if form.validate_on_submit():
            form.populate_obj(data)
            db.session.commit()
            return redirect(url_for('point.point_detail', point_id=data.point_id))
    else:
        if data.point.type == '지중경사계':
            form = DataVerticalForm(obj=data)
        elif data.point.type == "하중계":
            form = DataLoadcellForm(obj=data)
        else:
            form = DataForm(obj=data)

    if data.point.type == '지중경사계':
        return render_template('data/vertical_form.html', form=form)
    else:
        return render_template('data/data_form.html', form=form)

@bp.route('/delete/<int:data_id>')
@login_required
def data_delete(data_id):
    data = Data.query.get_or_404(data_id)
    point_id = data.point.id

    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('point.point_detail', point_id=point_id))
