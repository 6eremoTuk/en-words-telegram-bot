from functools import wraps

idList = ["696288583"]


def checking_status(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        message = args[0]
        ID = message.from_user.id
        print(ID)
        if str(ID) in idList:
            return func(*args, **kwargs)
        return "у вас неподтвержденная учетная запись"
    return wrapper
