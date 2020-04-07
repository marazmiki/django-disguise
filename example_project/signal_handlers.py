def on_disguise_applied(*args, **kwargs):
    original_user = kwargs['original_user']
    old_user = kwargs['old_user']
    new_user = kwargs['new_user']
    print(
        f'[Disguising]: {original_user} removed the disguising '
        f'of "{old_user}" and disguised into "{new_user}"'
    )


def on_disguise_removed(*args, **kwargs):
    original_user = kwargs['original_user']
    disguised_in_user = kwargs['disguised_in_user']

    print(
        f'[Removing disguise] {original_user} dropped '
        f'the {disguised_in_user}\'s mask'
    )
