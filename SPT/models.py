from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Members(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=25)    
    def __str__(self):
        return self.name

class Spendings(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    detail=models.CharField(blank=False,max_length=45)
    total=models.IntegerField()
    date=models.DateField(null=True,blank=False)
    add_date=models.DateField(auto_now_add=True,blank=True)
    def __str__(self):
        return self.detail[:10]

class Shares(models.Model):    
    spends=models.ForeignKey(Spendings,on_delete=models.CASCADE,blank=True,null=True)
    name=models.ForeignKey(Members,on_delete=models.CASCADE,blank=False)
    amount=models.IntegerField(blank=False)
    def __str__(self):
        return "{}={}".format(self.name,self.amount)