from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import urllib.parse

#params = urllib.parse.quote_plus("Driver={ODBC Driver 13 for SQL Server};Server=tcp:shortened-url-database-server.database.windows.net,1433;Database=shortened-url-database;Uid=roykollensvendsen@shortened-url-database-server;Pwd=ub3gesAK;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
#engine = create_engine("mssql+pymssql:///?odbc_connect=%s" % params)
engine = create_engine('sqlite:///test.db', convert_unicode=True)
#engine = create_engine('mssql+pyodbc://roykollensvendsen:ub3gesAK@shortened-url-database-server.database.windows.nett:1433/shortened-url-database', echo=True)
#engine = create_engine("mssql+pyodbc://roykollensvendsen:ub3gesAK@shortened-url-database-server.database.windows.net:1433/shortened-url-database?driver=ODBC+Driver+13+for+SQL+Server")
#engine = create_engine("mysql+pymysql:///azure:6#vWHD_$@127.0.0.1:50202/localdb")

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import ShortenedUrl.models
    Base.metadata.create_all(bind=engine)
