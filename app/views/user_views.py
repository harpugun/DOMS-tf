from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from app import db
from app.forms import UserLoginForm, UserCreateForm, UserModifyForm
from app.models import User
import functools

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        truename = form.truename.data,
                        company=form.company.data,
                        phone=form.phone.data,
                        email=form.email.data,
                        power='wait')
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('user/signup.html', form=form)

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        elif user.power == "wait":
            error = "관리자의 사용 승인까지 기다려 주세요."
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('user/login.html', form=form)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if (g.user is None) or (g.user.power=="wait"):
            return redirect(url_for('user.login'))
        return view(**kwargs)
    return wrapped_view

@bp.route('/list/')
@login_required
def user_list():
    if g.user.power != "admin":
        return redirect(url_for('user.login'))
    user_list = User.query.order_by(User.power.asc(), User.truename.asc())
    return render_template('user/user_list.html', user_list=user_list)

@bp.route('/modify/<int:user_id>', methods=('GET', 'POST'))
@login_required
def user_modify(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        form = UserModifyForm()
        if form.validate_on_submit():
            form.populate_obj(user)
            db.session.commit()
            return redirect(url_for('user.user_list', user_id=user_id))
    else:
        form = UserModifyForm(obj=user)
    return render_template('user/modify.html', form=form)

@bp.route('/delete/<int:user_id>')
@login_required
def user_delete(user_id):
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('user.user_list'))