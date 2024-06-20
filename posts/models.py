from django.db import models

from users.models import Employee

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    creator = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="posts"
    )
    possible_sellers = models.ManyToManyField(
        Employee, related_name="potential_sales", blank=True
    )
    is_sold = models.BooleanField(default=False)
    chosen_seller = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="chosen_sales",
    )

    def __str__(self):
        return self.title
