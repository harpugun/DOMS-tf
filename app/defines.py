#### 전체 정보 ####
def measuring_types() :
    measuring_types= [
        ('', '-- Type --'),
        ('지표침하계', '지표침하계'), ('지중경사계', '지중경사계'), ('지하수위계', '지하수위계'),
        ('구조물경사계', '구조물경사계'), ('균열측정계', '균열측정계'), ('하중계', '하중계'), ('변형률계', '변형률계'),
        ('', '-- etc.. --'),
        ('지표침하판', '지표침하판'), ('내공변위계', '내공변위계'), ('지중변위계', '지중변위계'),
        ('RB축력계', 'RB축력계'), ('SC응력계', 'SC응력계')
    ]
    return measuring_types

def members_types() :
    members_types = [
        ('admin', '관리자'),
        ('staff', '현장관리자'),
        ('user', '관측자'),
        ('wait', '대기자')
    ]
    return members_types

#### 현장 정보 (현장마다 수정)####

def area_types() :
    area_types = [
        ('흙막이구조물', '흙막이구조물'),
        ('지하구조물', '지하구조물'),
        ('하수관거', '하수관거')
    ]
    return area_types

def point_types() :
    point_types = [
        [
            ['지표침하계', 10],
            ['지중경사계', 5],
            ['지하수위계', 5],
            ['구조물경사계', 3],
            ['균열측정계', 3],
            ['하중계', 15],
            ['변형률계', 20]
        ],
        [
            ['구조물경사계', 5],
            ['균열측정계', 5]
        ],
        [
            ['하중계', 5],
            ['변형률계', 5]
        ]
    ]
    return point_types

def point_types_total() :
    point_types_total = 71
    return point_types_total