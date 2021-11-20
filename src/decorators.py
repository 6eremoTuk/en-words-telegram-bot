from functools import wraps
import config

idList = config.ADMIN_ID_LIST


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
