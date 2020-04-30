import os

# Get a session to the database to make queries

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 

db_url = os.environ["DB_URL"]
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()


# Actually query the database

from sqlalchemy.sql import func
from forum.models import Post, Comment

comments = (
    session.query(Comment.post_id, func.count("*").label("comments"))
    .group_by(Comment.post_id)
    .subquery()
)

positive_comments = (
    session.query(Comment.post_id, func.count("*").label("positive_comments"))
    .filter(Comment.sentiment == "positive")
    .group_by(Comment.post_id)
    .subquery()
)

negative_comments = (
    session.query(Comment.post_id, func.count("*").label("negative_comments"))
    .filter(Comment.sentiment == "negative")
    .group_by(Comment.post_id)
    .subquery()
)

final_query = (
    session.query(
        Post,
        comments.c.comments,
        negative_comments.c.negative_comments,
        positive_comments.c.positive_comments,
    )
    .outerjoin(comments, Post.id == comments.c.post_id)
    .outerjoin(negative_comments, Post.id == negative_comments.c.post_id)
    .outerjoin(positive_comments, Post.id == positive_comments.c.post_id)
)


# JSON example
# [
#     {
#         "id": 1,
#         "body": "This is a great tool",
#         "author_name": "Kevin Bacon",
#         "created_on": "2019-07-04",
#         "comments": 10,
#         "positive_comments": 8,
#         "negative_comments": 2
#     },
#     // ... more JSON objects
# ]

import json

items = []

for post, comments, negative_comments, positive_comments in final_query:
    items.append({
        "id": post.id,
        "body": post.body,
        "author_name": post.author_name,
        "created_on": post.created_on.date(), # timestamp transformed in actual date
        "comments": comments or 0,
        "positive_comments": positive_comments or 0,
        "negative_comments": negative_comments or 0
    })

with open("forum_export.json", mode="w") as f:
    json.dump(items, f)