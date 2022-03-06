from peewee import DateTimeField, Model, TextField, IntegerField
from playhouse.sqlite_ext import SqliteExtDatabase
import re

px_db = SqliteExtDatabase('pxmart.db', pragmas=(
    ('cache_size', -1024 * 64),  # 64MB page-cache.
    ('journal_mode', 'wal'),  # Use WAL-mode (you should always use this!).
    ('foreign_keys', 1))
)  # Enforce foreign-key constraints.




class Purchase(Model):

    name = TextField()
    count = IntegerField()
    total_price = IntegerField()
    date = DateTimeField()

    class Meta:
        database = px_db


if __name__ == '__main__':
    px_db.create_tables([Purchase])


