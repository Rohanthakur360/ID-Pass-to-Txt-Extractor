from online.Config import *


def one(user_id):
    if user_id in sudo_users:
        return True
    return False


def two(user_id):
    if user_id in owner_users:
        return True
    return False
