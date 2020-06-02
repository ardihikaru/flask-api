from app import Base
from sqlalchemy import text, Column, Integer, String, TIMESTAMP


class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    username = Column(String(50))
    password = Column(String(150))
    create_time = Column(TIMESTAMP, server_default=text('(now())'))

    def to_dict(self, show_passwd):
        user_info = {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'create_time': self.create_time
        }
        if show_passwd:
            user_info["password"] = self.password
        return user_info

    def insert(self, ses, data):
        ses.add(
            UserModel(
                name=data["name"],
                username=data["username"],
                password=data["password"]
            )
        )

