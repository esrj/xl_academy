from django.shortcuts import render,redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate
from django.contrib import auth
import json
from main.models import Profile,Contact,Testimony,Collage,TestQuestion,Order,Token,Course
from django.contrib.auth.decorators import login_required
import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from django.shortcuts import render
from django.http import HttpResponse
import os.path
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from .mail import write_message
from google.oauth2 import service_account
from django.core.mail import send_mail

SCOPES = ['https://mail.google.com/']

def login(request):
    if request.method == 'GET':
        if request.user.id != None:
            return redirect('/management/contact/')
        else:
            return render(request, 'login.html',locals())
    if request.method == 'POST':
        req = json.loads(request.body)
        username = req['username']
        password = req['password']
        if username and password:
            user=authenticate(username=username,password=password)
            if user is not None:
                if user.is_active :
                    auth.login(request, user)
                    return JsonResponse({'errno':0})
                else:
                    return JsonResponse({'errno': 1})
            else:
                return JsonResponse({'errno':1})
        else:
            return JsonResponse({'errno': 2})

@login_required(login_url='/management/')
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return JsonResponse({'errno':0})

# 聯絡人資訊表
@login_required(login_url='/management/')
def contact(request):
    if request.method == 'GET':
        return render(request,'contact.html')
    if request.method == 'POST':  # 獲取資料
        contact = Contact.objects.order_by('-date').all().values('id','name','email','phone','date','content','reply')
        contact = list(contact)
        for ele in contact:
            ele['date'] = ele['date'].strftime('%m-%d %H:%M')
        return JsonResponse({'errno':0,'contact':contact})
    if request.method == 'PATCH':
        req = json.loads(request.body)
        contact = Contact.objects.filter(id= req['id']).first()
        if contact.reply == True:
            contact.reply = False
        else:
            contact.reply = True
        contact.save()
        print(contact.reply)
        return JsonResponse({'errno':0})

# 聯絡人單獨資訊
@login_required(login_url='/management/')
def single(request,id):
    if request.method == 'GET':
        contact = Contact.objects.filter(id = id).first()
        return render(request,'single.html',locals())
    if request.method == 'POST':
        contact = Contact.objects.filter(id = id).first()
        contact.delete()
        return JsonResponse({'errno':0})

# 感言影片上傳
@login_required(login_url='/management/')
def testimony(request):
    if request.method == 'GET':
        return render(request,'testimony.html')
    if request.method == 'POST':
        previous = Testimony.objects.all()
        for prev in previous:
            try:
                os.remove( os.path.join(os.path.dirname(os.path.dirname(__file__)),'media',str(prev.video)))
                os.remove( os.path.join(os.path.dirname(os.path.dirname(__file__)),'media',str(prev.picture)))
                prev.delete()
            except:
                pass
        video = request.FILES.get('video')
        picture = request.FILES.get('picture')
        title = request.POST.get('title')
        student_name = request.POST.get('student_name')
        content = request.POST.get('content')
        content_en = request.POST.get('content_en')
        title_en = request.POST.get('title_en')
        student_name_en = request.POST.get('student_name_en')
        testimony = Testimony.objects.create(title = title,video = video,picture = picture,student_name = student_name ,content = content , content_en = content_en,title_en = title_en ,student_name_en = student_name_en)
        testimony.save()
        return JsonResponse({'errno':0})

# 試題上傳
@login_required(login_url='/management/')
def upload(request):
    if request.method == 'GET':
        return render(request,'upload.html')
    if request.method == 'POST':
        pdf = request.FILES.get('pdf')
        title = request.POST.get('title')
        title_en = request.POST.get('title_en')
        price = request.POST.get('price')
        introduce = request.POST.get('introduce')
        introduce_en = request.POST.get('introduce_en')
        classification = request.POST.get('classification')
        testQuestion = TestQuestion.objects.create(pdf=pdf,title=title,price=price,introduce=introduce,classification=classification,title_en = title_en,introduce_en= introduce_en)
        testQuestion.save()
        return JsonResponse({'errno':0})

@login_required(login_url='/management/')
def collage(request):
    if request.method == 'GET':
        return render(request,'collage.html')
    if request.method == 'POST':
        emblem = request.FILES.get('emblem')
        image = request.FILES.get('image')
        name = request.POST.get('name')
        en_name = request.POST.get('en_name')
        info = request.POST.get('info')
        info_en = request.POST.get('info_en')
        country = request.POST.get('country')
        country_en = request.POST.get('country_en')
        city = request.POST.get('city')
        city_en = request.POST.get('city_en')
        continent = request.POST.get('continent')
        address = request.POST.get('address')
        classification = request.POST.get('classification')
        links = request.POST.get('link')
        introduction = request.POST.get('introduction')
        introduction_en = request.POST.get('introduction_en')
        achievement = request.POST.get('achievement')
        achievement_en = request.POST.get('achievement_en')
        reason = request.POST.get('reason')
        reason_en = request.POST.get('reason_en')
        c = ['公立大學','私立大學','公立技術學院','私立技術學院','大學附設語言學校','技術學院附設語言學校','私立語言學校']
        classification_ = c[int(classification)-1]
        popular_departments = request.POST.get('popular_departments')
        popular_departments_en = request.POST.get('popular_departments_en')
        collage = Collage.objects.create(emblem = emblem,image = image,name = name,en_name = en_name ,info = info,country=country,city=city,continent=continent,address=address,classification=classification_,links=links,introduction=introduction,achievement=achievement,reason=reason,popular_departments=popular_departments,info_en = info_en,city_en = city_en,country_en = country_en,introduction_en =introduction_en, achievement_en=achievement_en, reason_en = reason_en, popular_departments_en = popular_departments_en)
        collage.save()
        return JsonResponse({'errno':0})

@login_required(login_url='/management/')
def mail(request):
    orders = Order.objects.all()
    return render(request,'mail.html',locals())

@login_required(login_url='/management/')
def course(request):
    if request.method == 'GET':
        return render(request,'course_.html')
    else:
        picture = request.FILES.get('picture')
        title = request.POST.get('title')
        date = request.POST.get('date')
        text = request.POST.get('text')
        text_en = request.POST.get('text_en')
        title_en = request.POST.get('title_en')
        course = Course.objects.create(picture = picture,title = title,date = date,text = text,title_en = title_en,text_en = text_en)
        course.save()
        return JsonResponse({'errno':0})


@login_required(login_url='/management/')
def sendmail(request, id):
    if request.method == 'GET':
        order = Order.objects.filter(id=id).first()
        testQuestions = TestQuestion.objects.all()
        return render(request, 'sendmail.html', locals())
    if request.method == 'POST':
        req = json.loads(request.body)
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                #引入新 token
                data = Token.objects.all().values('access_token','scope','token_type','expires_in','refresh_token','client_id','client_secret')
                data = list(data)[0]
                json_data = json.dumps(data, indent=4)
                with open('token.json', 'w') as token:
                    token.write(json_data)
                creds = Credentials.from_authorized_user_file('token.json', SCOPES)
                if creds and creds.expired and creds.refresh_token:
                    return HttpResponse('reset email token')
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        service = build('gmail', 'v1', credentials=creds)
        # 測試環境
        raw_message = write_message(req['email'],'media/mail_template/mail.html','static/picture/footer-logo.png',req['checkedValue'],req['name'],'media')
        # 伺服器環境
#         raw_message = write_message(req['email'],'/var/www/xl_academy/media/mail_template/mail.html','/var/www/staticfiles/static/picture/footer-logo.png',req['checkedValue'],req['name'],'/var/www/xl_academy/media')
        try:
            message = service.users().messages().send(userId="me", body={"raw": raw_message}).execute()
            return HttpResponse('Email sent successfully!')
        except Exception as error:
            return HttpResponse('Error sending email.')



