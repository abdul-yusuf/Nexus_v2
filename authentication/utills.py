from django.apps import apps
from django.conf import settings

# def (user, field, *args):

#     if not field:
#         return
#     User = apps.get_model(settings.AUTH_USER_MODEL, require_body=False)

from .models import User
def send_mail(user, pin):
    user_instance = User.objects.get(username=user.username, email=user.email)
    if user_instance.is_active:
        user_instance.is_active = False
    
    print('sending email','pin: ', pin)
    print(user.username)
    print()

def send_msg(user, pin):
    user_instance = User.objects.get(username=user.username, email=user.email)
    if user_instance.is_active:
        user_instance.is_active = False
    
    print('sending massage')
