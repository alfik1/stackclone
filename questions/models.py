from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.db.models import Count
# Create your models here.

class MyUser(AbstractUser):
    phone=models.CharField(max_length=10)
    profilepic=models.ImageField(upload_to='profilepic',null=True,blank=True)


class Questions(models.Model):
    description=models.CharField(max_length=200)
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='images', null=True,blank=True)
    created_on=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)

    
    @property
    def fetch_answers(self):
        answer=self.answers_set.all().annotate(usr_count=Count('upvote')).order_by=("-usr_count")
        return answer

    def __str__(self):
        return self.description
class Answers(models.Model):
    question=models.ForeignKey(Questions,on_delete=models.CASCADE)
    answer=models.CharField(max_length=200)
    user=models.ForeignKey(MyUser, on_delete=models.CASCADE)
    upvote=models.ManyToManyField(MyUser,related_name='upvotes')
    posted_date=models.DateTimeField(auto_now_add=True)

