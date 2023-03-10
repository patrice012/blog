from django import template

from blog.models import Post
from blog.forms import SearchForm

register = template.Library()

# @register.inclusion_tag('tags_snippet/_latest_posts.html')
# def show_latest_posts(count=5):
#     latest_posts = Post.publish.order_by('-release')[:count]
#     return {'latest_posts': latest_posts}



@register.inclusion_tag('tags_snippet/_latest_posts.html', takes_context=True)
def show_latest_posts(context):
    try:
        lts_number = context.get('lts_post_numb')
        post_id = context.get('post').id
        latest_posts = Post.publish.all().exclude(id=post_id).order_by('-release')[:lts_number]
    except:
        lts_number = 3
        latest_posts = Post.publish.order_by('-release')[:lts_number]
    return {
        "latest_posts": latest_posts,
    }




@register.simple_tag()
def posts_number():
    return Post.publish.all().count()

