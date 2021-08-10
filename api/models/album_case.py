from api.models.photo import Photo
from api.models.user import User, get_deleted_user
from django.contrib.postgres.fields import JSONField
from django.db import models


class AlbumCase(models.Model):
    title = models.CharField(max_length=512, default=None)
    created_on = models.DateTimeField(auto_now=True, db_index=True)
    photos = models.ManyToManyField(Photo)
    description = models.CharField(max_length=1024, default=None)
    favorited = models.BooleanField(default=False, db_index=True)
    owner = models.ForeignKey(
        User, on_delete=models.SET(get_deleted_user), default=None)

    shared_to = models.ManyToManyField(
        User, related_name='album_case_shared_to')

    public = models.BooleanField(default=False, db_index=True)

    class Meta:
        unique_together = ('title', 'owner')

    @property
    def cover_photos(self):
        return self.photos.filter(hidden=False)[:4]
