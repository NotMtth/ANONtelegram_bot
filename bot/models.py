from peewee import SqliteDatabase
import peewee as pw

import settings

db = SqliteDatabase(settings.DATABASE)


class Funding(pw.Model):
    id = pw.IntegerField()
    feature = pw.TextField(unique=True, null=True)
    amount = pw.FloatField(null=True)
    more_info = pw.TextField(null=True)
    sub_address = pw.TextField(unique=True, null=True)
    address_index = pw.IntegerField(unique=True, null=True)
    time = pw.TimestampField(primary_key=True)

    class Meta:
        database = db


def cleanup(user_id):
    Funding.delete().where(Funding.id == user_id and (Funding.feature == None or Funding.amount == None)).execute()
