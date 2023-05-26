# -*- coding: utf-8 -*-

import peewee as pw

db = pw.SqliteDatabase('./donos.db')


class MainModel(pw.Model):
    class Meta:
        database = db


class User(MainModel):
    name = pw.CharField()
    surname = pw.CharField()
    email = pw.CharField()
    login = pw.CharField()
    password = pw.CharField()


class Report(MainModel):
    title = pw.CharField()
    description = pw.CharField()
    photo = pw.CharField()
    status = pw.BooleanField()
    likes = pw.IntegerField()
    address = pw.CharField()
    dt = pw.DateTimeField()
    owner = pw.ForeignKeyField(User)


def create_tables():
    db.create_tables(models=[User, Report])


if __name__ == "__main__":
    create_tables()
