from utils.db_api.db_gino import TimedBaseModel
from sqlalchemy import Column, BigInteger, String, sql, Date, Boolean, Integer
from sqlalchemy.dialects import postgresql


class Building(TimedBaseModel):
    __tablename__ = 'buildings'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(100))
    list = Column(postgresql.ARRAY(Integer))

    query: sql.Select