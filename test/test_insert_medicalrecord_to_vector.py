import pymysql
import random
import string
import datetime
import time

# 常用中文姓名
NAMES = ['张三', '李四', '王五', '赵六', '钱七', '孙八', '周九', '吴十', '郑一', '冯二']
# 常见诊断
DISEASES = ['高血压', '糖尿病', '冠心病', '慢性胃炎', '感冒', '肺炎', '肝炎', '肾结石']
# 常见药物
DRUGS = ['阿司匹林', '二甲双胍', '氯吡格雷', '头孢克肟', '布洛芬', '阿莫西林']
# 常见主诉
COMPLAINTS = ['头痛', '咳嗽', '发热', '腹痛', '乏力', '胸闷', '恶心', '呕吐']
# 常见处理措施
TREATMENTS = ['输液', '口服药物', '住院观察', '手术治疗', '物理降温']
# 常见科室
DEPARTMENTS = ['内科', '外科', '儿科', '妇产科', '急诊科', '骨科']
# 常见医生姓名
DOCTOR_NAMES = ['李医生', '王医生', '赵医生', '钱医生', '孙医生']
# 常见机构
ORG_NAMES = ['北京协和医院', '上海瑞金医院', '广州中山医院', '四川华西医院', '测试医院']


def random_chinese_name():
    return random.choice(NAMES)

def random_idcard():
    # 简单生成18位身份证号（不校验真实合法性）
    area = str(random.randint(110000, 659004))
    birth = datetime.date.today() - datetime.timedelta(days=random.randint(18*365, 80*365))
    birth_str = birth.strftime('%Y%m%d')
    seq = str(random.randint(100, 299))
    last = str(random.randint(0, 9))
    return area + birth_str + seq + last

def random_mobile():
    return random.choice(['13', '15', '18', '19']) + ''.join(random.choices(string.digits, k=9))

def random_cardno():
    return 'C' + ''.join(random.choices(string.digits, k=9))

def random_business_id():
    return 'BIZ' + ''.join(random.choices(string.digits, k=10))

def random_patient_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=36))

def random_date(start_year=1970, end_year=2020):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    return start + datetime.timedelta(days=random.randint(0, (end - start).days))

def random_datetime():
    return datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 3650))

def insert_medicalrecord_to_vector(total_count=10000, batch_size=20):
    # 请根据实际情况修改以下数据库连接参数
    conn = pymysql.connect(
        host='localhost',
        user='root',
        port=5455,
        password='infini_rag_flow',
        database='rag_flow',
        charset='utf8mb4'
    )
    cursor = conn.cursor()

    sql = '''
    INSERT INTO MEDICALRECORD_to_vector (
      id, SERIALNUM_ID, TASK_ID, BATCH_NUM, LOCAL_ID, BUSINESS_ID, BASIC_ACTIVE_ID, DOMAIN_CODE, ORGANIZATION_NAME, RESOURCE_ID,
      OP_EM_MARK, OP_EM_NO, SEE_DOC_DT, CARDNO, NAME, SEX, BIRTHDAY, MOBILE, SUBJ_COMPLAINT, ALLE_NAME_1, MAIN_SYMP, PRES_ILLN, TEMP, SBP, DBP, PR, BREATGE,
      MD_DIS_NAME, DIS_NAME_1, DISE_DESC, PRES_DRUGS, IF_TEST, TR_MEAS, ORGAN_NAME, DPT_NAME, DOC_IDCARD, DOC_NAME, IF_OBS_DEATH, IF_EM_DEATH, PATIENT_ID,
      create_time, update_time, create_date, update_date, status
    ) VALUES (
      %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
      %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
      %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
      %s, %s, %s, %s, 0
    )
    '''

    def generate_row():
        name = random_chinese_name()
        disease1 = random.choice(DISEASES)
        disease2 = random.choice([d for d in DISEASES if d != disease1])
        drugs = ','.join(random.sample(DRUGS, k=random.randint(1, 3)))
        now_dt = datetime.datetime.now()
        now_ts = int(time.time())  # 秒级时间戳
        return (
            random_business_id(),  # ROW_ID
            random_cardno(),       # SERIALNUM_ID
            random_cardno(),       # TASK_ID
            random_cardno(),       # BATCH_NUM
            random_cardno(),       # LOCAL_ID
            random_business_id(),  # BUSINESS_ID
            random_business_id(),  # BASIC_ACTIVE_ID
            str(random.randint(1000, 9999)),  # DOMAIN_CODE
            random.choice(ORG_NAMES),         # ORGANIZATION_NAME
            random_cardno(),       # RESOURCE_ID
            random.choice(['0', '1']),  # OP_EM_MARK
            random_cardno(),       # OP_EM_NO
            random_datetime(),     # SEE_DOC_DT
            random_cardno(),       # CARDNO
            name,                  # NAME
            random.choice(['M', 'F']),  # SEX
            random_date(),         # BIRTHDAY
            random_mobile(),       # MOBILE
            random.choice(COMPLAINTS).encode('utf-8'),  # SUBJ_COMPLAINT
            '青霉素',                # ALLE_NAME_1
            random.choice(COMPLAINTS),  # MAIN_SYMP
            random.choice(COMPLAINTS).encode('utf-8'),  # PRES_ILLN
            random.randint(36, 40),  # TEMP
            random.randint(90, 140), # SBP
            random.randint(60, 90),  # DBP
            random.randint(60, 100), # PR
            random.randint(12, 20),  # BREATGE
            disease1,                # MD_DIS_NAME
            disease2,                # DIS_NAME_1
            disease1 + ',' + disease2,  # DISE_DESC
            drugs,                   # PRES_DRUGS
            random.choice(['0', '1']),  # IF_TEST
            random.choice(TREATMENTS).encode('utf-8'),  # TR_MEAS
            random.choice(ORG_NAMES),  # ORGAN_NAME
            random.choice(DEPARTMENTS), # DPT_NAME
            random_idcard(),           # DOC_IDCARD
            random.choice(DOCTOR_NAMES), # DOC_NAME
            random.choice(['0', '1']),  # IF_OBS_DEATH
            random.choice(['0', '1']),  # IF_EM_DEATH
            random_patient_id(),        # PATIENT_ID
            now_ts,      # create_time
            now_ts,      # update_time
            now_dt,      # create_date
            now_dt       # update_date
        )

    batches = total_count // batch_size
    remain = total_count % batch_size
    for _ in range(batches):
        rows = [generate_row() for _ in range(batch_size)]
        cursor.executemany(sql, rows)
        conn.commit()
    if remain:
        rows = [generate_row() for _ in range(remain)]
        cursor.executemany(sql, rows)
        conn.commit()
    print(f'插入完成，共{total_count}条')
    cursor.close()
    conn.close()

if __name__ == '__main__':
    insert_medicalrecord_to_vector(total_count=10000, batch_size=20) 
