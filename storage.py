from db import DB


def add_score(db: DB, username, name, score):
    db.change_social_credit_score(username, name, score)


def reduce_score(db: DB, username, name, score):
    db.change_social_credit_score(username, name, score * -1)
