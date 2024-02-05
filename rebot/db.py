from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Messages(Base):
    __tablename__ = 'messages'

    message_id = Column(String, primary_key=True)


engine = create_engine('sqlite:///re-bot.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def message_create(message_id):
    with Session() as session:
        message = Messages(message_id=message_id)
        session.add(message)
        session.commit()


def message_exists(message_id):
    with Session() as session:
        return session.query(Messages).filter_by(message_id=message_id).first() is not None
