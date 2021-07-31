from django.db import models
from django.utils import timezone

class Topic(models.Model):

    class Meta:
        db_table = "topic"

    title       = models.CharField(verbose_name="タイトル",max_length=20,default="無題")
    comment     = models.CharField(verbose_name="コメント",max_length=500)
    dt          = models.DateTimeField(verbose_name="投稿日",default=timezone.now)

    #ここの__str__(self)は消してもよい
    def __str__(self):
        return self.comment
