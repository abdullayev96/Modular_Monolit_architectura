from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Kategoriya nomi:")
    slug = models.SlugField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kategoriya_"

