import yaml
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

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

    def get_session(self):
        return self.Session()

    def get_events(self):
        session = self.get_session()
        result = session.execute(text("SELECT * FROM items")) # TODO: use vanna ai later for the query
        return result

if __name__ == '__main__':
    config_path = 'db_config.yaml'
    db = MySQLDatabase(config_path)
    result = db.get_events()
    for row in result:
        print(type(row), str(row))
