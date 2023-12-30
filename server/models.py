import os
import shutil

from django.db import models
from django.conf import settings
from django.dispatch import receiver
from rest_framework.generics import get_object_or_404


def category_icon_upload_path(instance, filename):
    # return f"category/{instance.id}/category_icons/{filename}"

    return f"category/category_icons/{instance.id} - {instance.name}/{filename}"

class Category(models.Model):
    name = models.CharField(max_length = 100)
    description = models.TextField(blank = True, null = True)
    icon = models.FileField(upload_to = category_icon_upload_path, null = True, blank = True)
    # ImageField does not support svg

    def save(self, *arg, **kwargs):
        self.name = self.name.lower()
        if self.id:
            existing = get_object_or_404(Category, id = self.id)
            if existing.icon != self.icon:
                existing.icon.delete(save = False)
        super(Category, self).save(*arg, **kwargs)

    @receiver(models.signals.pre_delete, sender="server.Category")
    def category_delete_files(sender, instance, **kwargs):
        icon_field = instance._meta.get_field("icon")

        if isinstance(icon_field, (models.ImageField, models.FileField)):
            file = getattr(instance, "icon", None)
            if file and file.storage.exists(file.name):
                #! Remove just file
                # file.storage.delete(file.name)

                #? Remove entire files inc folder
                folder_path = os.path.join(settings.MEDIA_ROOT, os.path.dirname(file.name))
                shutil.rmtree(folder_path, ignore_errors=True)


    def __str__(self):
        return self.name


class Server(models.Model):
    name = models.CharField(max_length = 100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'server_owner')
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name = 'server_category')
    description = models.CharField(max_length = 250, blank = True, null = True)
    member = models.ManyToManyField(settings.AUTH_USER_MODEL,)


    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.name = self.name.lower()
        super(Server, self).save()

    def __str__(self):
        return f"{self.name} / {self.id}"

class Channel(models.Model):
    name = models.CharField(max_length = 100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'channel_owner')
    topic = models.CharField(max_length = 100)
    server = models.ForeignKey(Server, on_delete = models.CASCADE, related_name = 'channel_server')

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.name = self.name.lower()
        super(Channel, self).save()

    def __str__(self):
        return self.name