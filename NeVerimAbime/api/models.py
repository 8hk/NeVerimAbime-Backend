import uuid as uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    ForeignKey,
    ManyToManyField,
    Model,
    TextField,
)


class User(AbstractUser):
    name = models.CharField(blank=True, max_length=255)
    follower = models.ManyToManyField("self", related_name="followers", symmetrical=False, blank=True)
    profile_image = models.FileField(upload_to="profile_image", blank=True, null=True)
    caloriesLimitation = models.FloatField(default=0, blank=False)
    foodProvider = models.BooleanField(default=False, blank=False)
    following = models.ManyToManyField("self", related_name="followings", symmetrical=False, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4,
                            editable=False,
                            unique=False)

    def __str__(self):
        return self.email

    def get_all_objects(self):
        queryset = User.objects.all()
        return queryset

    def get_user_email(self):
        return self.email
