from db import DB


def add_score(db: DB, username, name, score):
    db.change_social_credit_score(username, name, score)


def reduce_score(db: DB, username, name, score):
    db.change_social_credit_score(username, name, score * -1)

def get_ranking(db: DB, chat_id):
    members = db.get_chat_members(chat_id)
    if len(members) == 0:
        return None
    scores = []
    for member in members:
        member_name = db.get_user_name(member)
        if member_name is not None:
            member_score = db.get_social_credit_score(member)
            scores.append((member_name, member_score))
    scores.sort(key=lambda x: x[1], reverse=True)
    # generate formated output rank
    output = 'Leaderboard:\n'
    for name, score in scores:
        output += f'{name}: {score}\n'

    return output
