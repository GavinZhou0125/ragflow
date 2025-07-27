import pymysql
import random
import string
import datetime
import time

# 常用中文姓名
NAMES = ['张三', '李四', '王五', '赵六', '钱七', '孙八', '周九', '吴十', '郑一', '冯二', '黄秀荣', '张天明']
# 常见诊断
DISEASES = ['高血压', '糖尿病', '冠心病', '慢性胃炎', '感冒', '肺炎', '肝炎', '肾结石']
# 常见药物
DRUGS = ['阿司匹林', '二甲双胍', '氯吡格雷', '头孢克肟', '布洛芬', '阿莫西林']
# 常见主诉
COMPLAINTS = ['头痛', '咳嗽', '发热', '腹痛', '乏力', '胸闷', '恶心', '呕吐',
              '患者女性，56岁，主诉“反复头晕伴乏力3月余，加重1周”。患者约于3月前无明显诱因下开始出现间断性头晕，表现为旋转性眩晕，站立或活动时明显，卧床休息可缓解，常伴有乏力感，无恶心、呕吐，无耳鸣及听力下降。近1周来头晕症状明显加重，几乎每日均有发作，严重时需卧床休息，且伴有视物模糊、走路不稳，偶有心悸。否认近期感冒、发热、腹泻等病史，否认耳鸣耳聋等耳源性疾病史。既往有高血压病史10余年，平时服用氨氯地平控制血压不甚规律。无糖尿病、冠心病、脑卒中等病史。无药物过敏史。为求进一步明确病因并对症治疗，遂来我院就诊。',
              '患者男性，65岁，因“活动后胸闷胸痛1年余，近1月加重”前来就诊。患者自1年多前开始出现胸部压迫感，多在体力劳动或快步行走时发作，休息可自行缓解，每次持续数分钟，无明显放射痛。当时未重视，未行系统检查与治疗。近1月来症状明显加重，轻微活动即诱发，甚至在夜间睡眠中也出现胸闷憋气症状，偶有冷汗，需坐起缓解。否认明显心悸、晕厥，无咳嗽咳痰、咯血等症状。既往有高血压病史15年，吸烟史40年（20支/天），目前仍在吸烟，无明确冠心病诊断。为进一步明确病因，排除心绞痛及其他心源性疾病，特来门诊就诊。',
              '患者女性，42岁，主诉“体重增加伴月经紊乱1年余”。患者约于1年半前无明显诱因下开始体重逐渐增加，近半年体重增长约8kg，自述饮食未见明显变化，活动量正常。同期开始月经周期紊乱，表现为周期延长，间隔时间不规律，经量亦时多时少，有时需借助药物才能来潮。近3个月月经基本停止。伴有轻度多毛、痤疮增多、皮肤油腻等表现。否认头痛、视力模糊，无明显乳溢、泌乳，无精神紧张、压力事件。既往体健，否认糖尿病、甲亢、甲减病史，无家族遗传代谢性疾病史。为查明月经紊乱及体重变化原因，故就诊于我院内分泌科。',
              '患者男性，72岁，主诉“记忆力下降伴反应迟钝半年余”。患者家属诉患者于半年前开始出现明显记忆力减退表现，如忘记刚刚发生的事，重复询问相同问题，丢三落四现象逐渐增多，表现为短期记忆受损为主。近3个月来症状加重，逐渐出现计算能力下降、表达能力减退，反应较以往迟缓，需反复提示才能完成日常事务。偶有失眠，情绪波动，行为尚无明显异常。无抽搐、肢体麻木、行走不稳等症状。患者既往有高血压病史20年，规律服药控制尚可，无脑卒中病史，无癫痫史。为进一步诊治，排除阿尔茨海默病等神经系统疾病，遂来神经内科就诊。',
              '患者女性，50岁，主诉“反复咳嗽、咳痰2月，活动后气促加重1周”。患者自2个月前出现咳嗽咳痰症状，痰多为白色黏痰，无明显腥臭味，晨起尤为明显，无咯血。曾在外院就诊，给予抗生素及止咳药物治疗，症状略有缓解，但未完全好转。近1周来患者自觉呼吸费力，特别在上楼或快走时尤甚，伴有轻度胸闷，无发热、盗汗、体重明显下降。否认结核病史，否认哮喘、肺气肿明确诊断。既往吸烟史10余年，已戒烟5年。为明确慢性咳嗽原因及气促加重病因，特来我院呼吸内科进一步就诊。'
              ]
COMPLAINTS_short = ['头痛', '咳嗽', '发热', '腹痛', '乏力', '胸闷', '恶心', '呕吐']
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
    birth = datetime.date.today() - datetime.timedelta(days=random.randint(18 * 365, 80 * 365))
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
        host='10.100.52.37',
        user='root',
        port=3306,
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
            random_cardno(),  # SERIALNUM_ID
            random_cardno(),  # TASK_ID
            random_cardno(),  # BATCH_NUM
            random_cardno(),  # LOCAL_ID
            random_business_id(),  # BUSINESS_ID
            random_business_id(),  # BASIC_ACTIVE_ID
            str(random.randint(1000, 9999)),  # DOMAIN_CODE
            random.choice(ORG_NAMES),  # ORGANIZATION_NAME
            random_cardno(),  # RESOURCE_ID
            random.choice(['0', '1']),  # OP_EM_MARK
            random_cardno(),  # OP_EM_NO
            random_datetime(),  # SEE_DOC_DT
            random_cardno(),  # CARDNO
            name,  # NAME
            random.choice(['M', 'F']),  # SEX
            random_date(),  # BIRTHDAY
            random_mobile(),  # MOBILE
            random.choice(COMPLAINTS).encode('utf-8'),  # SUBJ_COMPLAINT
            '青霉素',  # ALLE_NAME_1
            random.choice(COMPLAINTS_short),  # MAIN_SYMP
            random.choice(COMPLAINTS_short).encode('utf-8'),  # PRES_ILLN
            random.randint(36, 40),  # TEMP
            random.randint(90, 140),  # SBP
            random.randint(60, 90),  # DBP
            random.randint(60, 100),  # PR
            random.randint(12, 20),  # BREATGE
            disease1,  # MD_DIS_NAME
            disease2,  # DIS_NAME_1
            disease1 + ',' + disease2,  # DISE_DESC
            drugs,  # PRES_DRUGS
            random.choice(['0', '1']),  # IF_TEST
            random.choice(TREATMENTS).encode('utf-8'),  # TR_MEAS
            random.choice(ORG_NAMES),  # ORGAN_NAME
            random.choice(DEPARTMENTS),  # DPT_NAME
            random_idcard(),  # DOC_IDCARD
            random.choice(DOCTOR_NAMES),  # DOC_NAME
            random.choice(['0', '1']),  # IF_OBS_DEATH
            random.choice(['0', '1']),  # IF_EM_DEATH
            random_patient_id(),  # PATIENT_ID
            now_ts,  # create_time
            now_ts,  # update_time
            now_dt,  # create_date
            now_dt  # update_date
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
    insert_medicalrecord_to_vector(total_count=20000, batch_size=1000)
