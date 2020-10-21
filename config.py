import os

BASE_DIR = os.path.dirname(__file__) # BASE_DIR 은 프로젝트 루트 디렉터리

# ORM
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'database.db')) # DB 위치와 이름 설정
SQLALCHEMY_TRACK_MODIFICATIONS = False # SQLAlchemy의 이벤트 처리 옵션. 추가적인 메모리를 사용 > 일단 비활성

SECRET_KEY = "harpugunmanmanse"