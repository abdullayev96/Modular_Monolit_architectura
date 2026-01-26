from django.db import models
from baseapp.models import BaseModel


class Authors(BaseModel):
    full_name = models.CharField(max_length=200, verbose_name="Author toliq ismi:")
    bio = models.TextField()
    image = models.ImageField(upload_to="media/", null=True, blank=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Yozuvchilar_"
