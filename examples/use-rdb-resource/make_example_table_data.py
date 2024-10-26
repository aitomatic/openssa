import os
import random

from dotenv import load_dotenv
from faker import Faker
from sqlalchemy import Column, Integer, String, Date, inspect, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from myvanna import train_vanna_for_sales_data

load_dotenv()

Base = declarative_base()


class SalesData(Base):
    __tablename__ = 'sales_data'
    sale_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer)
    product_name = Column(String(255))
    sale_date = Column(Date)
    region = Column(String(255))


class MySQLDatabase:
    def __init__(self):
        self.engine = self.create_engine()
        self.Session = sessionmaker(bind=self.engine)

    def create_engine(self):
        username = os.getenv('DB_USERNAME')
        password = os.getenv('DB_PASSWORD')
        host = os.getenv('DB_HOST')
        port = os.getenv('DB_PORT')
        database = os.getenv('DB_NAME')
        connection_string = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'
        return create_engine(connection_string)

    def get_session(self):
        return self.Session()

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def drop_table(self, table_class):
        inspector = inspect(self.engine)
        if inspector.has_table(table_class.__tablename__):
            table_class.__table__.drop(self.engine)


fake = Faker()
seed_value = 42
random.seed(seed_value)
Faker.seed(seed_value)

products = [
    {"id": 101, "name": "Smartwatch", "price": 150.00},
    {"id": 102, "name": "Laptop", "price": 1200.00},
    {"id": 103, "name": "Smartphone", "price": 800.00},
    {"id": 104, "name": "Tablet", "price": 400.00},
    {"id": 105, "name": "Headphones", "price": 100.00}
]

regions = ["North America", "Europe", "Asia", "South America", "Africa"]


def generate_sales_data(session, num_records):
    sales_data_list = []
    for _ in range(num_records):
        product = random.choice(products)
        region = random.choice(regions)
        sale_date = fake.date_between(start_date='-1y', end_date='today')
        sales_data = SalesData(
            product_id=product["id"],
            product_name=product["name"],
            sale_date=sale_date,
            region=region
        )
        sales_data_list.append(sales_data)
    session.bulk_save_objects(sales_data_list)
    session.commit()


if __name__ == "__main__":
    db = MySQLDatabase()

    db.drop_table(SalesData)
    db.create_tables()

    session = db.get_session()

    generate_sales_data(session, 20000)

    train_vanna_for_sales_data("""
        CREATE TABLE sales_data (
            sale_id INT PRIMARY KEY AUTO_INCREMENT,
            product_id INT,
            product_name VARCHAR(255),
            sale_date DATE,
            region VARCHAR(255)
        )
    """)
