from django.db import models

# Create your models here.
import uuid as uuid


class Nutrient(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4,
                            editable=False,
                            unique=True)
    name = models.CharField(max_length=256, null=False, blank=False)
    unitName = models.CharField(max_length=1024, null=True, blank=True)
    ingredientId = models.CharField(max_length=256, null=False, blank=False)
    fdcId=models.IntegerField(default=0)
    fdcRank=models.IntegerField(default=0)
    fdcNumber = models.CharField(max_length=1024, null=True, blank=True)
    amount=models.FloatField(default=0)


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if len(self.name) > 256:
            raise ValueError('Name length cant exceed 256 character')
        super(Nutrient, self).save(*args, **kwargs)

    def get_all_objects(self):
        # queryset = Nutrient.objects.all()
        queryset = Nutrient.objects.none()
        return queryset