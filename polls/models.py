from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=64, verbose_name = 'username')
    user_password = models.CharField(max_length=300, verbose_name = 'user_password')
    user_id = models.CharField(max_length=64, verbose_name = 'user_id')

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'polls'




# Create your models here.
# 게시글(Post)엔 제목(postname), 내용(contents)이 존재합니다
class Post(models.Model):

    contents = models.TextField(max_length=5)

    # 게시글의 제목(postname)이 Post object 대신하기
    def __str__(self):
        return self.contents
    

    