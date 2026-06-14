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
    video = models.TextField()
    student_name = models.TextField()
    content = models.TextField()
    title_en = models.TextField(default="")
    content_en = models.TextField(default="")
    student_name_en = models.TextField(default="")



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
    yt_links = models.CharField(max_length=500,default = "/#")
    fb_links =  models.CharField(max_length=500 ,default = "/#")
    introduction = models.TextField()
    achievement = models.TextField()
    reason  = models.TextField()
    popular_departments = models.TextField()

    info_en = models.CharField(max_length=200,default="")
    city_en =  models.CharField(max_length=50,default="")
    country_en = models.CharField(max_length=50,default="")
    introduction_en = models.TextField(default="")
    achievement_en = models.TextField(default="")
    reason_en  = models.TextField(default="")
    popular_departments_en = models.TextField(default="")

class TestQuestion(models.Model):
    # pdf = models.FileField(upload_to='file/')
    title = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200,default="")
    price = models.CharField(max_length=15)
    introduce = models.TextField()
    introduce_en = models.TextField(default="")
    details = models.TextField(default="")
    details_en = models.TextField(default="")
    image = models.FileField(upload_to='image/')
    classification = models.CharField(max_length=15)


# class BankAccount(models.Model):
#     bank_id = models.CharField(max_length=15)
#     account = models.CharField(max_length=25)


# class Order(models.Model):
#     date =  models.DateTimeField(auto_now_add = True)
#     username = models.CharField(max_length=50)
#     email = models.CharField(max_length=50)
#     phone = models.CharField(max_length=25)
#     bookid  = models.CharField(max_length=50)
#     content = models.TextField(default="")



# class Course(models.Model):
#     title =  models.CharField(max_length = 300)
#     picture = models.FileField(upload_to = 'picture/')
#     text = models.TextField()
#     date = models.CharField(max_length = 100)
#     title_en =  models.CharField(max_length = 300,default="")
#     text_en = models.TextField(default="")

class Ranking(models.Model):
    title =   models.CharField(max_length = 300)
    title_en =   models.CharField(max_length = 300,default="")
