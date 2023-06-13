from sqlalchemy import Column, BigInteger, String, sql, Date, Boolean

from utils.db_api.db_gino import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    fullname = Column(String(100))
    citizenship = Column(String(100))
    country = Column(String(100))
    building = Column(String(100))
    room = Column(BigInteger)
    end_visa = Column(Date)
    payment_notification = Column(Boolean)
    late_payment = Column(Boolean)
    visa_requirement = Column(Boolean)

    query: sql.Select