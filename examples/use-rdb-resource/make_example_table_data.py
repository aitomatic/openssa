from sqlalchemy import Column, Integer, String, Date, create_engine, inspect
from sqlalchemy.orm import sessionmaker, declarative_base
from faker import Faker
import random
import yaml

# ベースモデルを定義
Base = declarative_base()

# sales_data テーブルの定義
class SalesData(Base):
    __tablename__ = 'sales_data'

    sale_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer)
    product_name = Column(String(255))
    sale_date = Column(Date)
    region = Column(String(255))

# データベースクラス
class MySQLDatabase:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = self.load_config()
        self.engine = self.create_engine()
        self.Session = sessionmaker(bind=self.engine)

    def load_config(self):
        with open(self.config_path, 'r') as file:
            return yaml.safe_load(file)['database']['mysql']

    def create_engine(self):
        username = self.config['username']
        password = self.config['password']
        host = self.config['host']
        port = self.config['port']
        database = self.config['database']
        connection_string = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'
        return create_engine(connection_string)

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def drop_table(self, table_class):
        inspector = inspect(self.engine)
        if inspector.has_table(table_class.__tablename__):
            table_class.__table__.drop(self.engine)

    def get_session(self):
        return self.Session()


# Fakeデータ生成用のFakerを初期化
fake = Faker()

# ランダムシードを設定（例: 42）
seed_value = 42
random.seed(seed_value)
Faker.seed(seed_value)

# 製品リストを作成
products = [
    {"id": 101, "name": "Smartwatch", "price": 150.00},
    {"id": 102, "name": "Laptop", "price": 1200.00},
    {"id": 103, "name": "Smartphone", "price": 800.00},
    {"id": 104, "name": "Tablet", "price": 400.00},
    {"id": 105, "name": "Headphones", "price": 100.00}
]

# 地域リストを作成
regions = ["North America", "Europe", "Asia", "South America", "Africa"]

# データを生成して挿入
def generate_sales_data(session, num_records):
    sales_data_list = []
    for _ in range(num_records):
        # ランダムに製品、価格、地域を選択
        product = random.choice(products)
        region = random.choice(regions)

        # ランダムな販売日を生成（過去1年の範囲）
        sale_date = fake.date_between(start_date='-1y', end_date='today')

        # SalesData インスタンスを作成
        sales_data = SalesData(
            product_id=product["id"],
            product_name=product["name"],
            sale_date=sale_date,
            region=region
        )
        sales_data_list.append(sales_data)

    # 一括挿入
    session.bulk_save_objects(sales_data_list)
    session.commit()


# MySQLDatabaseクラスを使用して、テーブル作成とデータ挿入を実行
if __name__ == "__main__":
    # 設定ファイルのパス
    config_path = 'db_config.yaml'

    # MySQLDatabaseインスタンスを初期化
    db = MySQLDatabase(config_path)

    # 既存のsales_dataテーブルを削除
    db.drop_table(SalesData)

    # テーブルを作成
    db.create_tables()

    # セッションを取得
    session = db.get_session()

    # 20000件のデータを生成
    generate_sales_data(session, 20000)

    print("20000件のデータがsales_dataテーブルに作成されました。")
