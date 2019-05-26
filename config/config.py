from utils.coll import Config
from sqlalchemy import create_engine

DB_HOST = Config.get('DB.host')
DB_PASSWORD = Config.get('DB.password')

engine = create_engine(
    'mysql+pymysql://root:{}@{}/nbki_tests'.format(DB_PASSWORD, DB_HOST),
    echo=True
)
