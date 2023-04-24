from sqlalchemy import Column, Float, Integer, Numeric, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ItemDB(Base):
    __tablename__ = 'items'

    nm_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    brand_id = Column(Integer, nullable=False)
    site_brand_id = Column(Integer, nullable=False)
    supplier_id = Column(Integer, nullable=False)
    sale = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    sale_price = Column(Numeric(10, 2), nullable=False)
    rating = Column(Float, nullable=False)
    feedbacks = Column(Integer, nullable=False)
    colors = Column(String)
    quantity = Column(Integer, nullable=False)
