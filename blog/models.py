from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse

from taggit.managers import TaggableManager

from blog.helper import object_directory_path
from blog.manager import PublishedManager

# Create your models here.

User = settings.AUTH_USER_MODEL

class Post(models.Model):
    class Status(models.TextChoices):
        PUBLISH = 'publish', 'Publish'
        DRAFT = 'draft', 'Draft'

    author = models.ManyToManyField(User, verbose_name =_('Add another author'))
    title = models.CharField(_('Title'), max_length=255)
    slug = models.SlugField()
    content = models.TextField(_('Content'))
    image = models.ImageField(_('Main Image'), blank=True, null = True, upload_to=object_directory_path)
    status = models.CharField(_('Post status'), choices=Status.choices, max_length=25, default=Status.PUBLISH)
    created = models.DateTimeField(_('create'), auto_now_add=True, editable=False)
    release = models.DateTimeField(_('release'), auto_now=True)
    updated = models.DateTimeField(_('update'), auto_now=True, editable=True)

    objects = models.Manager()
    publish= PublishedManager()
    tags = TaggableManager()

    class Meta:
        verbose_name='Post'
        verbose_name_plural='Posts'

    def __str__(self):
        return str(self.title)

    def save(self):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save()

    def is_publish(self):
        return self.status == Post.Status.PUBLISH

    def get_absolute_url(self):
        kwargs={"slug":self.slug,'id':self.id}
        return reverse("blog:post_detail", kwargs=kwargs)
    
    @property
    def number_of_comments(self):
        return self.comments.all().count()


    @property
    def all_comments(self):
        comments = self.comments.all() 
        return comments

    @property
    def get_image_url(self):
        try:
            url = self.image.url
        except:
            url = None
        return url



class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    username = models.CharField(_('Username'), max_length=50)
    email = models.EmailField(blank=True, null=True)
    body = models.TextField()
    active = models.BooleanField(default=True)
    created = models.DateTimeField(_('create'), auto_now_add=True, editable=False)
    updated = models.DateTimeField(_('release'), auto_now=True)

    def __str__(self):
        return f'{self.username} comment the post {self.post}'

    class Meta:
        ordering = ('created',)



class NewsLetter(models.Model):
    mail = models.EmailField()
    joined = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.mail

    



