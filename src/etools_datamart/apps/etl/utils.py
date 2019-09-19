# def disable_indexes():
#     clause = """UPDATE pg_index
# SET indisready=false
# WHERE indrelid = (
#     SELECT oid
#     FROM pg_class
#     WHERE relname='<TABLE_NAME>'
# );"""
