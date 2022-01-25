import functools


@functools.total_ordering
class User:
    def __init__(self, user_id, balance):
        self.id = user_id
        self.balance = balance

    def __lt__(self, other):
        return self.balance < other.balance

    def __eq__(self, other):
        return self.balance == other.balance
