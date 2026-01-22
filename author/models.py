from django.db import models


class Authors(models.Model):
    full_name = models.CharField(max_length=200, verbose_name="Author toliq ismi:")
    bio = models.TextField()
    image = models.ImageField(upload_to="media/")

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Yozuvchilar_"
