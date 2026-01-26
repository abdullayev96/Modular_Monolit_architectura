from django.db import models
from baseapp.models import BaseModel


class Book(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Kitob nomi")
    title = models.CharField(max_length=255, verbose_name="Kitob haqida")
    image = models.ImageField(upload_to="media/", null=True, blank=True)
    author_id = models.PositiveIntegerField()
    category_id = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Kitoblar_"
