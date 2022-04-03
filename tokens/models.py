from django.db import models


class Token(models.Model):

    unique_hash = models.CharField(max_length=20)
    tx_hash = models.CharField(max_length=66)
    media_url = models.URLField(max_length=200)
    owner = models.CharField(max_length=42)

    def __str__(self):
        return self.unique_hash
