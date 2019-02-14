from django import template

from disguise.forms import DisguiseForm
from disguise.utils import can_disguise

register = template.Library()


@register.inclusion_tag('disguise/form.html', takes_context=True)
def disguise_widget(context):
    request = context['request']
    context.update({
        'can_disguise': can_disguise(request),
        'form': DisguiseForm(),
        'original_user': getattr(request, 'original_user', None),
        'disguise_user': request.user,
    })
    return context
