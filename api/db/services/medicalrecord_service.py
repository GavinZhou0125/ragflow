from datetime import datetime


from api.db.db_models import DB, API4Conversation, APIToken, Dialog, MedicalRecordToVector, \
    InHospitalRecordToVector
from api.db.services.common_service import CommonService
from api.utils import current_timestamp, datetime_format


class MDRService(CommonService):
    model = APIToken

    @classmethod
    @DB.connection_context()
    def used(cls, token):
        return cls.model.update({
            "update_time": current_timestamp(),
            "update_date": datetime_format(datetime.now()),
        }).where(
            cls.model.token == token
        )


class MedicalRecordService(CommonService):
    model = MedicalRecordToVector

    @classmethod
    @DB.connection_context()
    def get_list(cls,see_doc_dt,status, limit = 100):

        sessions = cls.model.select()
        # 只抽指定日期之后的
        if see_doc_dt:
            sessions = sessions.where(cls.model.SEE_DOC_DT >= see_doc_dt)

        # 只抽没抽过的
        if status:
            sessions = sessions.where(cls.model.status == status)
        else:
            sessions = sessions.where(cls.model.status == 0)

        sessions = sessions.limit(limit)

        return list(sessions.dicts())


    @classmethod
    @DB.connection_context()
    def get_list_all(cls,see_doc_dt,status):

        sessions = cls.model.select()
        # 只抽指定日期之后的
        if see_doc_dt:
            sessions = sessions.where(cls.model.SEE_DOC_DT >= see_doc_dt)

        # 只抽没抽过的
        if status:
            sessions = sessions.where(cls.model.status == status)
        else:
            sessions = sessions.where(cls.model.status == 0)

        return list(sessions.dicts())

    @classmethod
    @DB.connection_context()
    def update_status_batch(cls, records, new_status):
        """
        批量将records列表中的status字段设置为new_status，并更新到数据库。
        :param records: get_list返回的记录列表
        :param new_status: 要设置的新status值
        :return: 修改后的记录列表
        """
        ids = [record['id'] for record in records if 'id' in record]
        if ids:
            cls.model.update({cls.model.status: new_status}).where(cls.model.id.in_(ids)).execute()
            # 更新内存中的records
            for record in records:
                record['status'] = new_status
        return records


class InHospitalRecordService(CommonService):
    model = InHospitalRecordToVector

    @classmethod
    @DB.connection_context()
    def get_list(cls,see_doc_dt,status, limit = 100):

        sessions = cls.model.select()
        # 只抽指定日期之后的
        if see_doc_dt:
            sessions = sessions.where(cls.model.HP_DATE >= see_doc_dt)

        # 只抽没抽过的
        if status:
            sessions = sessions.where(cls.model.status == status)
        else:
            sessions = sessions.where(cls.model.status == 0)

        sessions = sessions.limit(limit)

        return list(sessions.dicts())


    @classmethod
    @DB.connection_context()
    def get_list_all(cls,see_doc_dt,status):

        sessions = cls.model.select()
        # 只抽指定日期之后的
        if see_doc_dt:
            sessions = sessions.where(cls.model.HP_DATE >= see_doc_dt)

        # 只抽没抽过的
        if status:
            sessions = sessions.where(cls.model.status == status)
        else:
            sessions = sessions.where(cls.model.status == 0)

        return list(sessions.dicts())

    @classmethod
    @DB.connection_context()
    def update_status_batch(cls, records, new_status):
        """
        批量将records列表中的status字段设置为new_status，并更新到数据库。
        :param records: get_list返回的记录列表
        :param new_status: 要设置的新status值
        :return: 修改后的记录列表
        """
        ids = [record['id'] for record in records if 'id' in record]
        if ids:
            cls.model.update({cls.model.status: new_status}).where(cls.model.id.in_(ids)).execute()
            # 更新内存中的records
            for record in records:
                record['status'] = new_status
        return records