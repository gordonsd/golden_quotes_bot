from peewee import PostgresqlDatabase, Model, DateTimeField, CharField
from datetime import datetime

psql_db = PostgresqlDatabase('postgres',
                             user='goldbot',
                             password='goldbot',
                             host='localhost',
                             port=5432)


class BaseModel(Model):
    class Meta:
        database = psql_db


class Quote(BaseModel):
    created = DateTimeField(default=datetime.now())
    chat_quote = CharField(max_length=200)
    chat_id = CharField(max_length=20)
    chat_name = CharField(max_length=50)
    user_id = CharField(max_length=20)
    user_firstname = CharField(max_length=50)
    user_lastname = CharField(max_length=50)
    user_username = CharField(max_length=50)
    quote_fromuser_id = CharField(max_length=20)
    quote_fromuser_firstname = CharField(max_length=50)
    quote_fromuser_lastname = CharField(max_length=50)
    quote_fromuser_username = CharField(max_length=50)

    class Meta:
        table_name = 's_gold_quotes'


# class Chat(BaseModel):
#     created = DateTimeField(default=datetime.now())
#     chat_id = CharField(max_length=20)
#     chat_name = CharField(max_length=50)
#     chat_type = CharField(max_length=20)
#
#     class Meta:
#         table_name = 's_gold_chats'
