from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Database:
    def __init__(self, db_uri):
        self.engine = create_engine(db_uri, echo=False)
        self.Base = declarative_base()

        class User(self.Base):
            __tablename__ = 'Users'
            id = Column(Integer, primary_key=True)
            name = Column(String)
            age = Column(Integer)

        self.Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.db = self.Session()

    def create_user(self, name, age):
        user = self.db.User(name=name, age=age)
        self.db.add(user)
        self.db.commit()

    def read_user(self, user_id):
        user = self.db.query(self.Base.User).filter_by(id=user_id).first()
        print(user.name, user.age)
        return user

    def update_user(self, user_id, name=None, age=None):
        user = self.db.query(self.Base.User).get(user_id)
        if name:
            user.name = name
        if age:
            user.age = age
        self.db.commit()

    def delete_user(self, user_id):
        user = self.db.query(self.Base.User).get(user_id)
        self.db.delete(user)
        self.db.commit()