from sqlalchemy import Column, Integer, String
from ShortenedUrl.database import Base

class UrlEntry(Base):
    __tablename__ = 'url_table'
    id = Column(Integer, primary_key=True)
    url = Column(String(1024), unique=True)

    def __init__(self, url=None):
        self.url = url

