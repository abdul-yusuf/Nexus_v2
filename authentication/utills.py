from django.apps import apps
from django.conf import settings

# def (user, field, *args):

#     if not field:
#         return
#     User = apps.get_model(settings.AUTH_USER_MODEL, require_body=False)

def send_mail(user, pin):
    print('sending email')
    pass

def send_msg(user, pin):
    print