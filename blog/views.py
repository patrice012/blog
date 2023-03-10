import re
import json
from django.contrib.postgres.search import (SearchVector, SearchQuery,SearchRank)
# from django.core import serializers
from django.shortcuts import redirect, render, reverse, get_object_or_404
from django.views.generic import CreateView, UpdateView
# from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from django.core.mail import send_mail
from django.db.models import Count


from taggit.models import Tag


from blog.forms import CommentForm, SharePostForm, SearchForm,NewsLetterForm
from blog.models import Post, Comment
from .utils import notify_subscriber


def index(request):
    posts = Post.publish.all()[:6]
    context = {
        'posts':posts
    }
    return render(request, 'blog/index.html', context)


def about(request):
    return render(request, 'blog/about.html')


class CreatePost(CreateView):
    model = Post
    fields = ['title', 'content', 'image','status', 'author']
    template_name = 'blog/create.html'
    extra_context = {'title': 'create'}


    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            tags = request.POST.get('tags', None)
            post = form.save(commit = True)
            post.author.add(request.user.id)

            # split the current string base on white space or comma
            try:
                s = re.split(r'\s+', tags)
            except:
                s = re.split(r'\W+', tags)
            for tag in s:
                # remove unnecessary comma at the end of the string and add all tags to the current post
                post.tags.add(tag.strip(','))
                post.save()
            notify_subscriber(request, post)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        return super().post(request, *args, **kwargs)


class UpdatePost(UpdateView):
    model = Post
    fields = ['title', 'content', 'image','status', 'author']
    template_name = 'blog/create.html'
    extra_context = {'title': 'update'}



def post_detail(request, slug, id):
    post = Post.publish.prefetch_related('author', 'tags').get(id = id, slug = slug)
    tags = post.tags.all()
    comment_form = CommentForm()
    share_form = SharePostForm()
    send = False

    # retieve 4 similar post base on the same share tags
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.publish.all().filter(tags__in = post_tags_ids).exclude(id = post.id)
    similar_posts_order = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-release')[:4]

    
    if request.method == 'POST' and 'share' in request.POST:
        send = share_post(request, post)

    print(request.is_ajax(),'this is ajax')
    # if request.headers.get('x-requested-with') == 'XMLHttpRequest':
    if request.is_ajax():
        comment = create_comment(request, post)
        if comment:
            # transform the model instance to dict
            post_comment = model_to_dict(comment)
            comment_number = post.comments.all().count()
            response= {
                'post_comment':post_comment,
                'comment_number':comment_number,
            }
            return JsonResponse(response, status=200, safe=False)

    context = {
        'post': post,
        'tags':tags,
        'comment_form':comment_form,
        'share_form':share_form,
        'send':send,
        'similar_posts':similar_posts_order,
        'lts_post_numb':5,
    }
    return render(request, 'blog/post_detail.html', context)



def create_comment(request, post):
    try:
        data = json.load(request)
    except IntegrityError as e:
        return HttpResponse(e)
    comment = Comment.objects.create(post_id=post.id, **data)
    return comment



def share_post(request, post):
    form = SharePostForm(request.POST)
    send = False
    if form.is_valid():
        data = form.cleaned_data
        post_url = request.build_absolute_uri(post.get_absolute_url())
        try:
            subject = f"{data['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n {data['name']}\'s comments: {data['comment']}"
            send_mail(subject, message, 'admin@myblog.com',[data['to']])
            send = not send
        except KeyError as e:
            return HttpResponse(e)
    return send



def delete_post(request,slug, id):
    post = get_object_or_404(Post,id = id, slug = slug)
    if request.user.has_perm('blog.delete_post', obj=post) :
        post = post.delete()
        # send message to notify the current user for the action
        return redirect(reverse('blog:index'))
    else:
        post.status = Post.Status.DRAFT
        post.save()
    return render(request, 'blog/index.html')



def post_by_tag(request, *args, **kwargs):
    try:
        tag = kwargs['tag']
        tag_id = Tag.objects.get(name=tag).id
        tag_posts = Post.publish.all().filter(tags = tag_id)
    except:
        raise Exception()
    context = {
        'tag_posts':tag_posts,
        'tag':tag,
        'post_tag':'tags',
    }
    return render(request, 'blog/post_list.html', context)


def post_list(request):
    posts = Post.publish.all()
    context = {
        'posts':posts,
        'post_list':'list',
    }
    return render(request,  'blog/post_list.html', context)



def search_view(request, *args, **kwargs):
    searchForm = SearchForm(request.GET)
    results, query = '', ''

    if searchForm.is_valid():
        query = searchForm.cleaned_data.get('query')
        search_vector = SearchVector('title', 'content')
        search_query = SearchQuery(query)

        results = Post.publish.annotate(
                    search=search_vector,
                    rank=SearchRank(search_vector, search_query)
            ).filter(search=search_query).order_by('-rank')

    context = {
        'results':results,
        'query':query,
        'searchForm':searchForm,
    }
    return render(request, 'blog/search.html', context)



def subscription(request):
    response = {}
    # if request.headers.get('x-requested-with') == 'XMLHttpRequest':
    if request.is_ajax():
        data = json.load(request)
        form = NewsLetterForm(data or None)
        if form.is_valid():
            form.save()
            response = {'resp':'success'}
    return JsonResponse(response, status=200, safe=False)