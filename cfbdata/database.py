from pymongo import MongoClient


def get_database():
    CONN_STR = "mongodb+srv://user:pass@127.0.0.1:27017/db"
    client = MongoClient(CONN_STR)
    return client['new_db']


def init_db():
    # get all fbs teams, create db entry
    # add current records, schedules, defaults
    # add SP+
    # add ELO
    pass
