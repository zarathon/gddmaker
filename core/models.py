from django.core.urlresolvers import reverse
from django.db.models import *
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models as models
from reversion import admin
import uuid
from ckeditor.fields import RichTextField


def user_directory_path(instance, filename):
    return settings.MEDIAFILES_LOCATION+'/media_{0}/{1}'.format(uuid.uuid4(), filename)


class Game(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    name = models.CharField(max_length=80)
    description = RichTextField()

    # Relationship Fields
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, )

    #Custom Relationship Fields
    def levels(self):
        return  self.level_set

    def characters(self):
        return self.character_set

    def medias(self):
        return self.media_set

    def mechanics(self):
        return self.mechanic_set

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return u'%s' % self.name

    def __unicode__(self):
        return u'%s' % self.name

    def get_absolute_url(self):
        return reverse('core_game_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('core_game_update', args=(self.pk,))


class Level(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Fields
    name = models.CharField(max_length=80)
    description = RichTextField()
    script = RichTextField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    # Relationship Fields
    game = models.ForeignKey('core.Game', on_delete=models.CASCADE)
    characters = models.ManyToManyField('core.Character', blank=True)
    medias = models.ManyToManyField('core.Media', blank=True)
    mechanics = models.ManyToManyField('core.Mechanic', blank=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return u'%s' % self.name

    def __unicode__(self):
        return u'%s' % self.name

    def get_absolute_url(self):
        return reverse('core_level_detail', args=(self.slug,))

    def get_update_url(self):
        return reverse('core_level_update', args=(self.slug,))


class Character(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Fields
    name = models.CharField(max_length=255)
    description = RichTextField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    # Relationship Fields
    game = models.ForeignKey('core.Game', on_delete=models.CASCADE)
    mechanics = models.ManyToManyField('core.Mechanic', blank=True)
    medias = models.ManyToManyField('core.Media', blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return u'%s' % self.name

    def __unicode__(self):
        return u'%s' % self.name

    def get_absolute_url(self):
        return reverse('core_character_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('core_character_update', args=(self.pk,))


class Media(models.Model):
    TYPES_CHOICES = (
        ("AUDIO", "Audio"),
        ("VIDEO", "Video"),
        ("PICTURE", "Picture")
    )
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Fields
    name = models.CharField(max_length=255)
    description = RichTextField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    url = models.URLField(blank=True)
    file = models.FileField(upload_to=user_directory_path, blank=True)
    type = models.CharField(max_length=30, choices=TYPES_CHOICES)

    # Relationship Fields
    game = models.ForeignKey('core.Game', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return u'%s' % self.type+" - "+self.name

    def __unicode__(self):
        return u'%s' % self.type+" - "+self.name

    def get_absolute_url(self):
        return reverse('core_media_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('core_media_update', args=(self.pk,))


class Mechanic(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Fields
    name = models.CharField(max_length=255)
    description = RichTextField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    # Relationship Fields
    game = models.ForeignKey('core.Game', on_delete=models.CASCADE)
    medias = models.ManyToManyField('core.Media', blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return u'%s' % self.name

    def __unicode__(self):
        return u'%s' % self.name

    def get_absolute_url(self):
        return reverse('core_mechanic_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('core_mechanic_update', args=(self.pk,))

admin.register(model=Game)
admin.register(model=Character)
admin.register(model=Level)
admin.register(model=Mechanic)
admin.register(model=Media)