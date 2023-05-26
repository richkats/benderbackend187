import models


# User CRUD


def user_json(user):
    user_dict = {
        "id": user.id,
        "name": user.name,
        "surname": user.surname,
        "email": user.email,
        "login": user.login,
        "password": user.password
    }
    return user_dict


def get_user(user_id):
    try:
        user = list(models.User.select().where(models.User.id == user_id))[0]
        user_dict = user_json(user)
    except IndexError:
        return {"status": "No such item"}
    return user_dict


def get_users():
    users = models.User.select()
    user_dicts = []
    for user in users:
        user_dict = user_json(user)
        user_dicts.append(user_dict)
    return user_dicts


def create_user(user_dict):
    user = models.User.create(**user_dict)
    return user_json(user)


def delete_user(user_id):
    user = get_user(user_id)
    q = user.delete()
    return q.execute()


# Report CRUD


def report_json(report):
    report_dict = {
        "id": report.id,
        "title": report.title,
        "description": report.description,
        "photo": report.photo,
        "status": report.status,
        "likes": report.likes,
        "address": report.address,
        "dt": report.dt,
        "owner": report.owner.id
    }
    return report_dict


def get_report(report_id):
    try:
        report = list(models.Report.select().where(models.Report.id == report_id))[0]
        report_dict = report_json(report)
    except IndexError:
        return {"status": "No such item"}
    return report_dict


def get_reports():
    reports = models.Report.select()
    report_dicts = []
    for report in reports:
        report_dict = report_json(report)
        report_dicts.append(report_dict)
    return report_dicts


def create_report(report_dict):
    report = models.Report.create(**report_dict)
    return report_json(report)


def delete_report(report_id):
    report = get_report(report_id)
    q = report.delete()
    return q.execute()


def like_report(report_id):
    report = get_report(report_id)
    q = models.Report.update({models.Report.likes: report['likes'] + 1}).where(models.Report.id == report_id)
    return q.execute()
