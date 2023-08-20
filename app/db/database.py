from sqlalchemy import create_engine, Column, Integer, String, BOOLEAN, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://postgres:5525@localhost/postgres"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False)


class Task(Base):
    __tablename__ = "Tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    completed = Column(BOOLEAN, nullable=False)
    user_id = Column(Integer, ForeignKey("Users.id"))
    user = relationship("User", back_populates="tasks")


Base.metadata.create_all(bind=engine)
