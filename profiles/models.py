from django.db import models


class Profile(models.Model):
    user_id = models.PositiveIntegerField(unique=True, db_index=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    full_name = models.CharField(max_length=255, verbose_name="F.I.O")
    number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon")
    avatar = models.ImageField(upload_to='profiles/avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    # ManyToManyField o'rniga JSONField yoki alohida bog'lovchi jadval
    purchased_book_ids = models.JSONField(default=list)

    def __str__(self):
        return f"User ID: {self.user_id} - Balance: {self.balance}"

    class Meta:
        verbose_name = "Profile_"


