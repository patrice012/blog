from django import  forms
from django.utils.translation import gettext_lazy as _


from blog.models import Comment, NewsLetter


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['username','email','body','active']



class SharePostForm(forms.Form):
    name =forms.CharField()
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(widget=forms.Textarea ,required=False)


class SearchForm(forms.Form):
    query= forms.CharField(label='Search', required=False)
    # update the text search fields to match the current css classe and id
    query.widget.attrs.update({'id':'search','type':'text', 'name':'query',
            'placeholder':'Start typing. Press Enter key to search'})



class NewsLetterForm(forms.ModelForm):
    class Meta:
        model = NewsLetter
        fields = ['mail']
