from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

# create table posts (
#     id SERIAL PRIMARY KEY,
#     body TEXT NOT NULL,
#     author_name VARCHAR(50) NOT NULL,
#     created_on TIMESTAMP NOT NULL DEFAULT NOW()
# );

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    body = Column(Text, nullable=False)
    author_name = Column(String(50), nullable=False)
    created_on = Column(TIMESTAMP)

    comments = relationship("Comment", back_populates="post")

# create table comments (
#     id SERIAL PRIMARY KEY,
#     post_id INTEGER REFERENCES posts(id),
#     comment TEXT NOT NULL,
#     sentiment VARCHAR(10) NOT NULL,
#     commenter_name VARCHAR(50) NOT NULL,
#     created_on TIMESTAMP NOT NULL DEFAULT NOW()
# );

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    comment = Column(Text, nullable=False)
    sentiment = Column(String(10), nullable=False)
    commenter_name = Column(String(50), nullable=False)
    created_on = Column(TIMESTAMP)

    post = relationship("Post", back_populates="comments")