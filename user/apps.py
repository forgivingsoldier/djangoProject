from django.apps import AppConfig

class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'  # 这应该是你的应用的名字

    def ready(self):
        import tools.signals  # 假设你的信号接收函数在 user 应用的 signals.py 文件中

