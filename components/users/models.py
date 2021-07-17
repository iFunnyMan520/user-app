import uuid
from hashlib import md5

import sqlalchemy as sa

from components.users import exc
from utils.pg import Base, db_session


class User(Base):
    __tablename__ = 'users'

    id: int = sa.Column(sa.Integer, primary_key=True)
    email: str = sa.Column(sa.String, unique=True)
    password: str = sa.Column(sa.String)

    first_name: str = sa.Column(sa.String)
    last_name: str = sa.Column(sa.String)

    # user session token
    token: str = sa.Column(sa.String)

    # superuser with full privileges (create, edit, delete)
    superuser: bool = sa.Column(sa.Boolean, nullable=False,
                                server_default='False')

    def __repr__(self):
        return f'User ({self.id})'

    @staticmethod
    def create_token() -> str:
        """
        Creates session token for authorized user
        :return:
        """
        new_token = str(uuid.uuid4()).upper()
        new_token.replace('O', '')
        new_token.replace('0', '')
        return new_token.replace('-', '')

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Password hashing
        :param password:
        :return:
        """
        return md5(password.encode()).hexdigest()

    @classmethod
    def create(cls,
               email: str,
               password: str,
               first_name: str,
               last_name: str,
               superuser: bool = False) -> 'User':
        if db_session.query(cls).filter_by(email=email).first():
            raise exc.EmailAlreadyExisted

        new_user = cls()
        new_user.email = email
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.password = cls.hash_password(password)
        new_user.superuser = superuser

        db_session.add(new_user)
        db_session.commit()

        return new_user

    @classmethod
    def register(cls,
                 email: str,
                 password: str,
                 first_name: str,
                 last_name: str,
                 superuser: bool = False) -> 'User':
        if db_session.query(cls).filter_by(email=email).first():
            raise exc.EmailAlreadyExisted

        new_user = cls()
        new_user.email = email
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.password = cls.hash_password(password)
        new_user.superuser = superuser
        new_user.token = cls.create_token()

        db_session.add(new_user)
        db_session.commit()

        return new_user

    @classmethod
    def login(cls, email: str, password: str) -> 'User':

        user = db_session.query(cls).filter_by(
            email=email, password=cls.hash_password(password)
        ).first()

        if not user:
            raise exc.AuthUserNotFound

        user.token = cls.create_token()
        db_session.add(user)
        db_session.commit()

        return user

    @classmethod
    def get_user(cls,
                 user_id: int = None,
                 email: str = None,
                 token: str = None) -> 'User':

        query = db_session.query(cls)

        if user_id:
            query = query.filter_by(id=user_id)
        if email:
            query = query.filter_by(email=email)
        if token:
            query = query.filter_by(token=token)

        return query.first()

    @classmethod
    def get_all_users(cls):
        return db_session.query(cls).order_by(User.id.desc()).all()

    @staticmethod
    def edit(user_id: int,
             email: str,
             first_name: str,
             last_name: str,
             superuser: bool = False):

        edited_user = User.get_user(user_id=user_id)

        if not edited_user:
            return

        user = User.get_user(email=email)
        if user and user.id != edited_user.id:
            raise exc.EmailAlreadyExisted

        edited_user.email = email
        edited_user.first_name = first_name
        edited_user.last_name = last_name
        edited_user.superuser = superuser

        db_session.add(edited_user)
        db_session.commit()

        return edited_user

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def logout(self):
        self.token = None

        db_session.add(self)
        db_session.commit()

    def serialize(self) -> dict:
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'superuser': self.superuser,
        }
