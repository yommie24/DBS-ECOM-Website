
def dict_factory(cursor, row):
    """Use this as the row factory to replace tuples with dicts for Pydantic validation"""
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}
