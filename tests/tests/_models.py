from django.db import models


class SampleModel(models.Model):
    name = models.CharField(max_length=64)
    password = models.CharField(max_length=128)
    website = models.URLField()

    class Meta:
        app_label = "app"
