import firebase_admin
from firebase_admin import credentials, firestore


class DB:
    def __init__(self, credential_path):
        if not firebase_admin._apps:
            cd = credentials.Certificate(credential_path)
            firebase_admin.initialize_app(cd)
        self.db = firestore.client()
        self.social_credit = self.db.collection(u'social_credit')
        self.chats = self.db.collection(u'chats')

    def change_social_credit_score(self, username, name, score_change):
        ref = self.social_credit.document(username)
        doc = ref.get()
        if doc.exists:
            new_score = doc.to_dict()['score'] + score_change
            ref.update({'score': new_score})
        else:
            self.social_credit.document(username).create({
                'name': name,
                'score': score_change
            })

        return self.get_social_credit_score(username)

    def get_social_credit_score(self, username) -> int:
        ref = self.social_credit.document(username)
        if ref.get().exists:
            score = ref.get().to_dict()['score']
            return score
        else:
            return 0

    def get_user_name(self, username):
        ref = self.social_credit.document(username)
        doc = ref.get()
        if doc.exists:
            name = ref.get().to_dict()['name']
            return name
        else:
            return None

    def get_chat_members(self, chat_id) -> list:
        ref = self.chats.document(str(chat_id))
        doc = ref.get()
        if doc.exists:
            members = list(doc.to_dict()['members'])
            return members
        else:
            return []
