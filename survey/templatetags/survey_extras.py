from django import template
from survey.models import Like_Dislike

register = template.Library()

@register.filter(name='like')
def like(value,arg):
    obj = Like_Dislike.objects.get(question = value, user = arg)
    if obj.like == 1:
        string = 'fas'
    else:
        string = 'fal'
    return string

@register.filter(name='not_like')
def not_like(value,arg):
    obj = Like_Dislike.objects.get(question = value, user = arg)
    if obj.like == 0:
        string = 'fas'
    else:
        string = 'fal'
    return string