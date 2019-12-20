from django.db import models

# Create your models here.

class RecommendedBook(models.Model):
    author = models.CharField(max_length=100)
    bookTitle = models.CharField(max_length=50)
    content = models.TextField()
    bookImage=models.ImageField(upload_to="")
    genre = models.CharField(max_length=200, null=True, blank=True, default="")
    good = models.IntegerField(null=True, blank=True,default=0)
    goodtext = models.CharField(max_length=500,null=True,blank=True, default="")
    notGood = models.IntegerField(null=True, blank=True,default=0)
    notGoodtext = models.CharField(max_length=500,null=True,blank=True, default="")


class comment(models.Model):
    target = models.ForeignKey(RecommendedBook, on_delete=models.CASCADE,default="")
    title = models.CharField(max_length=100, default="名無し")
    content = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

# class SubComment(models.Model):
#     text = models.CharField('コメント', max_length=300)
#     target = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name="紐づくコメント")
#     created_at = models.DateTimeField(auto_now_add=True)