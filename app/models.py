from app import db


class Site(db.Model): # 현장db
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(30), nullable=False)  # 현장타입
    fullname = db.Column(db.String(30), unique=True, nullable=False)  # 현장명
    nickname = db.Column(db.String(10), unique=True, nullable=False)  # 현장 짧은이름
    service = db.Column(db.String(30), nullable=False)  # 용역명
    order = db.Column(db.String(10), nullable=True)  # 발주처
    supervisor = db.Column(db.String(10), nullable=True)  # 감리단
    constructor = db.Column(db.String(10), nullable=True)  # 시공사
    cost = db.Column(db.BigInteger, nullable=True)  # 계약금액
    endcost = db.Column(db.BigInteger, nullable=True)  # 기성금액
    startdate = db.Column(db.Date(), nullable=True)  # 시작일시
    enddate = db.Column(db.Date(), nullable=True)  # 종료일시
    memo = db.Column(db.Text(), nullable=True)  # 히스토리

class Point(db.Model): # 계측기
    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.String(10), nullable=True)  # 구역명
    number = db.Column(db.String(10), nullable=False)  # 계측기명
    type = db.Column(db.String(10), nullable=False)  # 계측기 종류
    installdate = db.Column(db.Date(), nullable=True)  # 설치일시
    startdate = db.Column(db.Date(), nullable=True)  # 초기치일시
    enddate = db.Column(db.Date(), nullable=True)  # 종료일시
    locate = db.Column(db.String(20), nullable=True)  # 설치 위치
    active = db.Column(db.Integer(), default=True)  # 활성화
    cst01 = db.Column(db.Float(), nullable=True)  # 상수값
    cst02 = db.Column(db.Float(), nullable=True)  # 상수값
    cst03 = db.Column(db.Float(), nullable=True)  # 상수값
    cst04 = db.Column(db.Float(), nullable=True)  # 상수값
    cst05 = db.Column(db.Float(), nullable=True)  # 상수값
    cst06 = db.Column(db.Float(), nullable=True)  # 상수값
    cst07 = db.Column(db.Float(), nullable=True)  # 상수값
    cst08 = db.Column(db.Float(), nullable=True)  # 상수값
    cst09 = db.Column(db.Float(), nullable=True)  # 상수값
    cst10 = db.Column(db.Float(), nullable=True)  # 상수값
    cst11 = db.Column(db.Float(), nullable=True)  # 상수값
    cst12 = db.Column(db.Float(), nullable=True)  # 상수값
    cst13 = db.Column(db.Float(), nullable=True)  # 상수값
    cst14 = db.Column(db.Float(), nullable=True)  # 상수값
    cst15 = db.Column(db.Float(), nullable=True)  # 상수값
    cst16 = db.Column(db.Float(), nullable=True)  # 최종데이터
    cst17 = db.Column(db.Float(), nullable=True)  # 최종데이터
    cst18 = db.Column(db.Float(), nullable=True)  # 최종데이터
    memo = db.Column(db.Text(), nullable=True)  # 히스토리

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    point_id = db.Column(db.Integer, db.ForeignKey('point.id', ondelete='CASCADE'))
    point = db.relationship('Point', backref=db.backref('data_set'))
    measuringdate = db.Column(db.DateTime(), nullable=True)  # 계측일시
    data01 = db.Column(db.Float(), nullable=True)  # 계측값
    data02 = db.Column(db.Float(), nullable=True)  # 계측값
    data03 = db.Column(db.Float(), nullable=True)  # 계측값
    data04 = db.Column(db.Float(), nullable=True)  # 계측값
    data05 = db.Column(db.Float(), nullable=True)  # 계측값
    data06 = db.Column(db.Float(), nullable=True)  # 계측값
    data07 = db.Column(db.Float(), nullable=True)  # 계측값
    data08 = db.Column(db.Float(), nullable=True)  # 계측값
    data09 = db.Column(db.String(400), nullable=True)  # 계측값
    data10 = db.Column(db.String(20), nullable=True)  # 비고
    data11 = db.Column(db.Float(), nullable=True)  # 계산값_누적일
    data12 = db.Column(db.Float(), nullable=True)  # 계산값_기간일
    data13 = db.Column(db.Float(), nullable=True)  # 계산값_누적변위
    data14 = db.Column(db.Float(), nullable=True)  # 계산값_일간변위
    data15 = db.Column(db.Float(), nullable=True)  # 계산값_기간변위
    remark = db.Column(db.String(10), nullable=True)  # 비고

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    truename = db.Column(db.String(20), nullable=False)
    company = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    power = db.Column(db.String(20), nullable=False)