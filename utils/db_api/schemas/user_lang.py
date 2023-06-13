from sqlalchemy import Column, BigInteger, String, sql, Date, Boolean

from utils.db_api.db_gino import TimedBaseModel


class User_lang(TimedBaseModel):
    __tablename__ = 'users_lang'
    id = Column(BigInteger, primary_key=True)
    language = Column(String(5))

    query: sql.Select