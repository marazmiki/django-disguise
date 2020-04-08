from django.contrib import messages


def on_disguise_applied(*args, **kwargs):
    original_user = kwargs['original_user']
    request = kwargs['request']
    old_user = kwargs['old_user']
    new_user = kwargs['new_user']

    messages.success(request, (
        '[Disguising]: {original_user} removed the disguising '
        'of "{old_user}" and disguised into "{new_user}"'
    ).format(
        original_user=original_user,
        new_user=new_user,
        old_user=old_user
    ))


def on_disguise_removed(*args, **kwargs):
    original_user = kwargs['original_user']
    disguised_in_user = kwargs['disguised_in_user']
    request = kwargs['request']

    messages.success(request, (
        '[Removing disguise] {original_user} dropped '
        'the {disguised_in_user}\'s mask'
    ).format(original_user=original_user,
             disguised_in_user=disguised_in_user)
    )
