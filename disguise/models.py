from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, post_syncdb

def create_perms(sender, **kwargs):
    perms = (
        ('can_disguise', 'Can disguise'),
    )

    # create a content type for the app if it doesn't already exist
    content_type, created = ContentType.objects.get_or_create(
        model     = '',
        app_label = 'disguise',
        defaults  = {'name': 'disguise'})
    
    for codename, title in perms:
        # create a permission if it doesn't already exist
        Permission.objects.get_or_create(
             codename         = codename,
             content_type__pk = content_type.id,
             defaults         = {'name': title,
                                 'content_type': content_type,})

post_save.connect(create_perms, Permission)
post_syncdb.connect(create_perms, sender=__import__('disguise'))
