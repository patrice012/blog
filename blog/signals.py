# from django.db.models.signals import post_save
# from django.dispatch import receiver

# from .models import Post
# from .utils import notify_subscriber

# @receiver(post_save, sender=Post)
# def connect_post_to_subcriber(sender, **kwargs):
#     print(kwargs)
#     if 'created' in kwargs :
#         post = kwargs['instance']
#         notify_subscriber(post=post)

