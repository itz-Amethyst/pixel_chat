from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length = 100)
    description = models.TextField(blank = True, null = True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.name = self.name.lower()
        super(Category, self).save()

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
        return self.name

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