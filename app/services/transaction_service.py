

class TransactionService:

    def __init__(self, repo):
        self.repo = repo

    def create_transaction(self, payload):
        return self.repo.create(payload)

    def list_transactions(self, user_id: int):
        return self.repo.get_all(user_id)