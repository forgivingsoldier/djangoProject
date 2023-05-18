from django.core.cache import cache
from django.contrib.auth.signals import user_logged_in, user_logged_out

def user_logged_in_handler(sender, user, request, **kwargs):
    online = cache.get('online_users', 0)
    cache.set('online_users', online + 1)

def user_logged_out_handler(sender, user, request, **kwargs):
    online = cache.get('online_users', 0)
    online = online - 1 if online > 0 else 0
    cache.set('online_users', online)

user_logged_in.connect(user_logged_in_handler)
user_logged_out.connect(user_logged_out_handler)
