from django.db import models


class User(models.Model):
    uwnetid = models.SlugField(max_length=16,
                               db_index=True,
                               unique=True)

    uwregid = models.CharField(max_length=32,
                               null=True,
                               db_index=True,
                               unique=True)

    display_name = models.CharField(max_length=250, null=True)
    email = models.CharField(max_length=255, null=True)
