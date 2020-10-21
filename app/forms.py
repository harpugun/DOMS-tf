from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, DateField, RadioField, SelectField, FloatField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Optional, Length, EqualTo, Email



class UserCreateForm(FlaskForm):
    username = StringField('ID(필수)', validators=[DataRequired(), Length(min=3, max=25)], render_kw={"placeholder": "ID"})
    password1 = PasswordField('비밀번호', validators=[DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')], render_kw={"placeholder": "비밀번호"})
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()], render_kw={"placeholder": "비밀번호 확인"})
    truename = StringField('사용자명(필수)', validators=[DataRequired()], render_kw={"placeholder": "이름"})
    company = StringField('회사명', validators=[Optional()], render_kw={"placeholder": "회사명"})
    phone = StringField('전화번호', validators=[Optional()], render_kw={"placeholder": "전화번호"})
    email = StringField('이메일', validators=[Optional()], render_kw={"placeholder": "이메일"})

class UserModifyForm(FlaskForm):
    from app.defines import members_types
    members_types = members_types()

    truename = StringField('사용자명(필수)', validators=[DataRequired()], render_kw={"placeholder": "이름"})
    company = StringField('회사명', validators=[Optional()], render_kw={"placeholder": "회사명"})
    phone = StringField('전화번호', validators=[Optional()], render_kw={"placeholder": "전화번호"})
    email = StringField('이메일', validators=[Optional()], render_kw={"placeholder": "이메일"})
    power = SelectField('권한', choices = members_types, validators=[DataRequired()])

class UserLoginForm(FlaskForm):
    username = StringField('ID(필수)', validators=[DataRequired(), Length(min=3, max=25)], render_kw={"placeholder": "ID"})
    password = PasswordField('비밀번호(필수)', validators=[DataRequired()], render_kw={"placeholder": "비밀번호"})

class SiteForm(FlaskForm):
    fullname = StringField('현장명(필수)', validators=[DataRequired()])
    nickname = StringField('현장심볼(필수)', validators=[DataRequired()])
    type = StringField('현장타입(필수)', validators=[DataRequired()])
    service = StringField('용역명(필수)', validators=[DataRequired()])
    order = StringField('발주처', validators=[Optional()])
    supervisor = StringField('감리단', validators=[Optional()])
    constructor = StringField('시공사', validators=[Optional()])
    cost = IntegerField('계약금액', validators=[Optional()])
    endcost = IntegerField('기성금액', validators=[Optional()])
    startdate = DateField('시작일시', validators=[Optional()])
    enddate = DateField('종료일시', validators=[Optional()])
    memo = TextAreaField('히스토리', validators=[Optional()])

class PointForm(FlaskForm):
    from app.defines import measuring_types, area_types
    measuring_types = measuring_types()
    area_types = area_types()

    area = SelectField('구역', choices = area_types, validators=[DataRequired()])
    number = StringField('계측기명(I경,W수,P침,T틸,C크,E하,S변) ', validators=[DataRequired()])
    type = SelectField('계측기종류', choices = measuring_types, validators=[DataRequired()])
    installdate = DateField('설치일시', validators=[DataRequired()])
    startdate = DateField('초기치일시', validators=[DataRequired()])
    enddate = DateField('종료일시', validators=[Optional()])
    locate = StringField('설치위치', validators=[Optional()])
    active = RadioField('Active', choices = [(1, '활성'), (0, '비활성')], validators=[DataRequired()])
    cst01 = FloatField('관리기준1차(누적)', validators=[DataRequired()])
    cst02 = FloatField('관리기준2차(누적)', validators=[Optional()])
    cst03 = FloatField('관리기준3차(누적)', validators=[Optional()])
    cst04 = FloatField('관리기준1차(일일)', validators=[Optional()])
    cst05 = FloatField('관리기준2차(일일)', validators=[Optional()])
    cst06 = FloatField('관리기준3차(일일)', validators=[Optional()])
    cst07 = FloatField('관리기준1차(심도)', validators=[Optional()])
    cst08 = FloatField('관리기준2차(심도)', validators=[Optional()])
    cst09 = FloatField('관리기준3차(심도)', validators=[Optional()])
    cst10 = FloatField('IW(설치심도)', validators=[Optional()])
    cst11 = FloatField('E(S/N), S(Ep)', validators=[Optional()])
    cst12 = FloatField('E(GF), S(A)', validators=[Optional()])
    cst13 = FloatField('E(LZ)', validators=[Optional()])
    cst14 = FloatField('E(설계축력)', validators=[Optional()])
    cst15 = FloatField('E(JF)', validators=[Optional()])

class DataForm(FlaskForm):
    measuringdate = DateField('계측일시', validators=[DataRequired()])
    data01 = FloatField('데이터01', validators=[DataRequired()])
    data02 = FloatField('데이터02', validators=[Optional()])
    data03 = FloatField('데이터03', validators=[Optional()])

class DataLoadcellForm(FlaskForm):
    measuringdate = DateField('계측일시', validators=[DataRequired()])
    data01 = FloatField('데이터01', validators=[DataRequired()])
    data02 = FloatField('데이터02', validators=[DataRequired()])
    data03 = FloatField('데이터03', validators=[DataRequired()])

class DataVerticalForm(FlaskForm):
    measuringdate = DateField('계측일시', validators=[DataRequired()])
    data09 = StringField('경사계 데이터', validators=[DataRequired()])

class AnalysisDateForm(FlaskForm):
    analfromdate = DateField('분석 시작일', validators=[DataRequired()])
    analtodate = DateField('분석 종료일', validators=[DataRequired()])
    analarea = SelectField('구역 선택', choices=[], validators=[DataRequired()])
    analpoint = SelectField('계측기 선택', choices=[], validators=[DataRequired()])


"""
class ReportForm(FlaskForm):
    startdate = DateField('시작일시', validators=[DataRequired()])
    enddate = DateField('종료일시', validators=[DataRequired()])
    title = RadioField('표지', choices = [(1, '포함'), (0, '비활성')], validators=[DataRequired()])
    submit = RadioField('제출문', choices = [(1, '포함'), (0, '비활성')], validators=[DataRequired()])
    contents = RadioField('목차', choices = [(1, '포함'), (0, '비활성')], validators=[DataRequired()])
    chaptercover = RadioField('장별표지', choices = [(1, '포함'), (0, '비활성')], validators=[DataRequired()])
    summary = RadioField('개요', choices = [(1, '포함'), (0, '비활성')], validators=[DataRequired()])
    summary_fulfill = RadioField('과업 수행 개요', choices=[(1, '포함'), (0, '비활성')], validators=[DataRequired()])
    summary_task = RadioField('>과업 개요', choices=[(1, '포함'), (0, '비활성')], validators=[DataRequired()])
    summary_situation = RadioField('> 공사 현황', choices=[(1, '포함'), (0, '비활성')], validators=[DataRequired()])
    summary_map = RadioField('> 현장 위치도', choices=[(1, '포함'), (0, '비활성')], validators=[DataRequired()])
    land = RadioField('지형과 지질', choices=[(1, '포함'), (0, '비활성')], validators=[DataRequired()])
    land_topography = RadioField('> 지형', choices=[(1, '포함'), (0, '비활성')], validators=[DataRequired()])
    land_geology = RadioField('> 지질', choices=[(1, '포함'), (0, '비활성')], validators=[DataRequired()])
    survey = RadioField('계측 일반', choices=[(1, '포함'), (0, '비활성')], validators=[DataRequired()])
    survey_purpose = RadioField('> 계측의 목적', choices=[(1, '포함'), (0, '비활성')], validators=[DataRequired()])
    survey_flow = RadioField('> 계측관리 흐름도', choices=[(1, '포함'), (0, '비활성')], validators=[DataRequired()])
    survey_item = RadioField('> 계측 항목 설정', choices=[(1, '포함'), (0, '비활성')], validators=[DataRequired()])
    install = RadioField('계측기기의 설치 및 측정방법', choices=[(1, '포함'), (0, '비활성')], validators=[DataRequired()])
    install_point = RadioField('> 계측기', choices=[(1, '포함'), (0, '비활성')], validators=[DataRequired()])
    analysis = RadioField('계측 결과의 분석 방법', choices=[(1, '포함'), (0, '비활성')], validators=[DataRequired()])
    analysis_method = RadioField('> 분석법', choices=[(1, '포함'), (0, '비활성')], validators=[DataRequired()])
    oursite = RadioField('당 현장의 계측관리', choices=[(1, '포함'), (0, '비활성')], validators=[DataRequired()])
    oursite_plan = RadioField('> 계측기 계획 및 설치 현황', choices=[(1, '포함'), (0, '비활성')], validators=[DataRequired()])
    oursite_frequency = RadioField('> 계측 빈도', choices=[(1, '포함'), (0, '비활성')], validators=[DataRequired()])
    oursite_organize = RadioField('> 현장조직 및 인원투입', choices=[(1, '포함'), (0, '비활성')], validators=[DataRequired()])
    oursite_standard = RadioField('> 현장 관리기준 적용', choices=[(1, '포함'), (0, '비활성')], validators=[DataRequired()])
    oursite_overbrief = RadioField('> 관리기준 초과 시 보고 체계', choices=[(1, '포함'), (0, '비활성')], validators=[DataRequired()])
    oursite_brief = RadioField('> 보고 체계', choices=[(1, '포함'), (0, '비활성')], validators=[DataRequired()])
    result = RadioField('계측 결과 및 분석', choices=[(1, '포함'), (0, '비활성')], validators=[DataRequired()])
    result_site = RadioField('> 시공 현황', choices=[(1, '포함'), (0, '비활성')], validators=[DataRequired()])
    result_area = RadioField('> 구간별 현장계측 자료', choices=[(1, '포함'), (0, '비활성')], validators=[DataRequired()])
    result_area_measuring = RadioField('>> 계측기', choices=[(1, '포함'), (0, '비활성')], validators=[DataRequired()])
    conclusion = RadioField('결론', choices=[(1, '포함'), (0, '비활성')], validators=[DataRequired()])
    appendix = RadioField('부록', choices=[(1, '포함'), (0, '비활성')], validators=[DataRequired()])
    appendix_map = RadioField('> 현장위치도', choices=[(1, '포함'), (0, '비활성')], validators=[DataRequired()])
    appendix_blueprint = RadioField('> 계측도면', choices=[(1, '포함'), (0, '비활성')], validators=[DataRequired()])
    appendix_sheet = RadioField('> 계측 Data', choices=[(1, '포함'), (0, '비활성')], validators=[DataRequired()])
"""


