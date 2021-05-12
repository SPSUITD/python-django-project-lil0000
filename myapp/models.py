from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Message(models.Model):
  text = models.CharField(max_length=300)
  user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='user'
  )
  author = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='author'
  )
  created_at = models.DateTimeField(auto_now_add=True)
