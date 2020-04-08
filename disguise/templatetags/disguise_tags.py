from django import template

from disguise.forms import get_disguise_form_class
from disguise.utils import can_disguise

register = template.Library()


@register.filter(name='can_disguise')
def filter_can_disguise(request):
    return can_disguise(request)


@register.inclusion_tag('disguise/form.html', takes_context=True)
def disguise_widget(context):
    request = context['request']
    context.update({
        'can_disguise': can_disguise(request),
        'form': get_disguise_form_class()(),
        'original_user': getattr(request, 'original_user', None),
        'disguise_user': request.user,
    })
    return context
