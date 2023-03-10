from django.core.mail import send_mail
from django.contrib.sites.models import Site

from .models import Post


def notify_subscriber(request, post):
    url = request.build_absolute_uri(post.get_absolute_url())
    try:
        subject = f"New post"
        message = f"Read {post.title} at {url}\n "
        send_mail(subject, message, 'admin@myblog.com',['hello@gmail.com','one@gmail.com','demo@gmail.com'])
    except:
        pass



