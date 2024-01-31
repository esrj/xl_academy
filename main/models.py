from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)


class Contact(models.Model):
    name = models.TextField()
    email = models.TextField()
    phone = models.TextField(default = "不公開")
    content = models.TextField()
    date = models.DateTimeField(auto_now_add = True)
    reply = models.BooleanField(default=False)


class Testimony(models.Model):
    title = models.TextField()
    video = models.FileField(upload_to='image/')
    picture = models.FileField(upload_to = 'picture/')
    student_name = models.TextField()
    content = models.TextField()


class Collage(models.Model):
    emblem = models.FileField(upload_to='collage/emblem/')
    image =  models.FileField(upload_to='collage/image/')
    name = models.CharField(max_length=100)
    en_name = models.CharField(max_length=100)
    info = models.CharField(max_length=200)
    country = models.CharField(max_length=50)
    city =  models.CharField(max_length=50)
    continent = models.CharField(max_length=15)
    address = models.CharField(max_length=200)
    classification = models.CharField(max_length=50)
    links = models.CharField(max_length=500)
    introduction = models.TextField()
    achievement = models.TextField()
    reason  = models.TextField()
    popular_departments = models.TextField()

class TestQuestion(models.Model):
    pdf = models.FileField(upload_to='file/')
    title = models.CharField(max_length=200)
    price = models.CharField(max_length=15)
    introduce = models.TextField()
    classification = models.CharField(max_length=15)




class BankAccount(models.Model):
    bank_id = models.CharField(max_length=15)
    account = models.CharField(max_length=25)


class Order(models.Model):
    date =  models.DateTimeField(auto_now_add = True)
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=25)
    account = models.CharField(max_length = 50)
    price = models.CharField(max_length = 25)
    page_id  = models.CharField(max_length=50)
    is_send = models.BooleanField(default = False)
