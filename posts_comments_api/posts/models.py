from django.db import models
from users.models import User

# Create your models here.


class PostEntry(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_blocked = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False)

    def __str__(self):
        return self.title
