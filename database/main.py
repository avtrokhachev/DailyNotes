from database.concepts import database


def start():
    database.Repository()  # start engine and establish connection
    database.Base.metadata.create_all(database.Repository.get_engine())


def disable():
    database.Repository.disable_engine()


def start_and_clear_for_test():
    database.Repository()  # start engine and establish connection
    database.Base.metadata.drop_all(database.Repository.get_engine())  # clear from previous tests data
    database.Base.metadata.create_all(database.Repository.get_engine())
