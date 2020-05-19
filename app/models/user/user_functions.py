from sqlalchemy.orm.exc import NoResultFound


def get_user_by_username(ses, user_model, username):
    try:
        data = ses.query(user_model).filter_by(username=username).one()
    except NoResultFound:
        return False, None
    dict_user = data.to_dict()

    if len(dict_user) > 0:
        return True, dict_user
    else:
        return False, None
