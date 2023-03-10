from django.apps import AppConfig
# from django.db.models.signals import post_save


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    # def ready(self):
    #     from .signals import connect_post_to_subcriber
    #     post_save.connect(connect_post_to_subcriber, sender='blog.Post')
