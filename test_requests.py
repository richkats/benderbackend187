# -*- coding: utf-8 -*-
import json
import random
from pprint import pprint

import requests as req
from faker import Faker
from faker.providers import lorem, address, date_time


SERVER = "http://127.0.0.1:5000/"


def make_request(server, method, payload):
    if method == 'get':
        r = req.get(server)
    elif method == 'post':
        r = req.post(server, json=payload)
    elif method == 'delete':
        r = req.delete(server, json=payload)
    return r.text


def generate_fake_users(number):
    fake = Faker()
    fake_users = []
    for i in range(number):
        fake_user = {
            "name": fake.first_name(),
            "surname": fake.last_name(),
            "login": fake.user_name(),
            "email": fake.free_email(),
            "password": fake.password(length=12)
        }
        fake_users.append(fake_user)
    return fake_users


def generate_fake_reports(number):
    fake = Faker()
    fake.add_provider(lorem)
    fake.add_provider(address)
    fake.add_provider(date_time)
    fake_reports = []
    for i in range(number):
        fake_report = {
            "title": fake.user_name(),
            "description": fake.paragraph(nb_sentences=1),
            "photo": fake.image_url(),
            "status": random.choice([True, False]),
            "likes": 0,
            "address": fake.address(),
            "dt": fake.unix_time(),
            "owner": random.randint(1, 16)
        }
        fake_reports.append(fake_report)
    return fake_reports


if __name__ == "__main__":
    # for user in generate_fake_users(4):
    #     pprint(make_request(SERVER+"users/", "post", payload=user))

    # for report in generate_fake_reports(4):
    #     pprint(make_request(SERVER+"reports/", "post", payload=report))
    pprint(make_request(SERVER+"like_report/", "post", payload={"report_id": 1}))