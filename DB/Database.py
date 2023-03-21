import logging

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class UserDB:
    def __init__(self, db_uri):
        self.engine = create_engine(db_uri, echo=False)
        self.Base = declarative_base()

        class User(self.Base):
            __tablename__ = 'Users'
            id = Column(Integer, primary_key=True)
            name = Column(String)
            password = Column(String)
            age = Column(Integer)

        self.User = User
        self.Base.metadata.create_all(self.engine)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create_user(self, name, password, age):
        user = self.User(name=name, password=password, age=age)
        self.session.add(user)
        self.session.commit()
        logging.info("User created successfully")

    def read_user(self, user_id):
        user = self.session.query(self.User).filter_by(id=user_id).first()
        print(user.name, user.password, user.age) if user else print("User not found")
        return user

    def update_user(self, user_id, name=None, password=None, age=None):
        user = self.session.query(self.User).get(user_id)
        print("User not found") if not user else (
            setattr(user, 'name', name) if name else None,
            setattr(user, 'age', age) if age else None,
            setattr(user, 'password', password) if password else None,
            self.session.commit())

    def delete_user(self, user_id):
        user = self.read_user(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()
        else:
            print("User not found")

    def check_user(self, user_id=None, name=None, age=None, password=None):
        user = self.session.query(self.User).get(user_id) if user_id else self.session.query(
            self.User).filter_by(name=name).filter_by(age=age).filter_by(
            password=password).all() if name and age and password else \
            self.session.query(self.User).filter_by(name=name).filter_by(
                password=password).all() if name and password else \
                self.session.query(self.User).filter_by(age=age).filter_by(
                    password=password).all() if age and password else \
                    self.session.query(self.User).filter_by(name=name).all() if name else self.session.query(
                        self.User).filter_by(
                        age=age).all() if age else None
        print("User not found") if not user else \
            (print(user.name, user.age) if isinstance(user, self.User) else [print(u.name, u.age) for u in user], user)[
                1] if user else None
        return user

    def get_user(self, name, password):
        user = self.session.query(self.User).filter_by(name=name).filter_by(
            password=password).all() if name and password else None
        print("User not found") if not user else \
            (print(user.name, user.age) if isinstance(user, self.User) else [print(u.name, u.age) for u in user], user)[
                1] if user else None
        return user
