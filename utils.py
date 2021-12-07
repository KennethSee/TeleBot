from db import DB


def add_score(db: DB, userid, name, score):
    db.change_social_credit_score(userid, name, score)


def reduce_score(db: DB, userid, name, score):
    db.change_social_credit_score(userid, name, score * -1)

def get_ranking(db: DB, chat_id):
    members = db.get_chat_members(chat_id)
    if len(members) == 0:
        return None
    scores = []
    for member in members:
        member_name = db.get_user_id(member)
        if member_name is not None:
            member_score = db.get_social_credit_score(member)
            scores.append((member_name, member_score))
    scores.sort(key=lambda x: x[1], reverse=True)
    # generate formated output rank
    output = 'Department of Social Credit report:\n'
    for name, score in scores:
        output += f'{name}: {score}\n'

    return output

def add_to_group(db, chat_id, chat_name, userid):
    members = db.get_chat_members(chat_id)
    if userid not in members:
        members.append(userid)
        db.update_chat_members(chat_id, chat_name, members)
