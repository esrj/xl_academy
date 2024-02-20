from django.shortcuts import render,redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate
from django.contrib import auth
import json
from main.models import Profile,Contact,Testimony,Collage,TestQuestion,Order
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

@login_required(login_url='/management/')
def single(request,id):
    if request.method == 'GET':
        contact = Contact.objects.filter(id = id).first()
        return render(request,'single.html',locals())
    if request.method == 'POST':
        contact = Contact.objects.filter(id = id).first()
        contact.delete()
        return JsonResponse({'errno':0})

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
        testimony = Testimony.objects.create(title = title,video = video,picture = picture,student_name = student_name ,content = content)
        testimony.save()
        return JsonResponse({'errno':0})

@login_required(login_url='/management/')
def upload(request):
    if request.method == 'GET':
        return render(request,'upload.html')
    if request.method == 'POST':
        pdf = request.FILES.get('pdf')
        title = request.POST.get('title')
        price = request.POST.get('price')
        introduce = request.POST.get('introduce')
        classification = request.POST.get('classification')
        testQuestion = TestQuestion.objects.create(pdf=pdf,title=title,price=price,introduce=introduce,classification=classification)
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
        country = request.POST.get('country')
        city = request.POST.get('city')
        continent = request.POST.get('continent')
        address = request.POST.get('address')
        classification = request.POST.get('classification')
        links = request.POST.get('link')
        introduction = request.POST.get('introduction')
        achievement = request.POST.get('achievement')
        reason = request.POST.get('reason')
        c = ['公立大學','私立大學','公立技術學院','私立技術學院','大學附設語言學校','技術學院附設語言學校','私立語言學校']
        classification_ = c[int(classification)-1]
        popular_departments = request.POST.get('popular_departments')
        collage = Collage.objects.create(emblem = emblem,image = image,name = name,en_name = en_name ,info = info,country=country,city=city,continent=continent,address=address,classification=classification_,links=links,introduction=introduction,achievement=achievement,reason=reason,popular_departments=popular_departments)
        collage.save()
        return JsonResponse({'errno':0})

@login_required(login_url='/management/')
def mail(request):
    orders = Order.objects.all()
    return render(request,'mail.html',locals())

from google.oauth2 import service_account
from django.core.mail import send_mail
def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes())
    raw_message = raw_message.decode()
    return {'raw': raw_message}



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
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES, access_type='offline')
                creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        service = build('gmail', 'v1', credentials=creds)
        message = MIMEMultipart()
        message['to'] = req['email']
        message['subject'] = 'XL Academy 試題購買'
        html_filename = 'media/mail_template/mail.html'
        with open(html_filename, 'r') as html_file:
            html_body = html_file.read()
        image_filename = 'static/picture/footer-logo.png'
        with open(image_filename, 'rb') as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        html_body = html_body.replace('<!-- INSERT_IMAGE_HERE -->',f'<img style="height:38px" src="data:image/jpeg;base64,{image_data}" alt="Image">')
        html_body = html_body.replace('<!-- INSERT_NAME -->', req['name'])
        html_msg = MIMEText(html_body, 'html')
        message.attach(html_msg)
        for id in list(req['checkedValue']):
                testQuestion = TestQuestion.objects.filter(id= id).first()
                pdf_filename = f'media/{testQuestion.pdf}'
                with open(pdf_filename, 'rb') as pdf_file:
                        pdf_attachment = MIMEBase('application', 'octet-stream')
                        pdf_attachment.set_payload(pdf_file.read())
                        encoders.encode_base64(pdf_attachment)
                        pdf_attachment.add_header('Content-Disposition', f'attachment; filename={pdf_filename}')
                        message.attach(pdf_attachment)

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
        try:
            message = service.users().messages().send(userId="me", body={"raw": raw_message}).execute()
            return HttpResponse('Email sent successfully!')
        except Exception as error:
            return HttpResponse('Error sending email.')




'''
@login_required(login_url='/management/')
def sendmail(request, id):
    if request.method == 'GET':
            order = Order.objects.filter(id=id).first()
            testQuestions = TestQuestion.objects.all()
            return render(request, 'sendmail.html', locals())
    if request.method == 'POST':
        req = json.loads(request.body)
        creds = Credentials.from_authorized_user_file('/var/www/xl_academy/token.json', SCOPES)
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                flow = InstalledAppFlow.from_client_secrets_file('/var/www/xl_academy/credentials.json', SCOPES, access_type='offline')
                creds = flow.run_local_server(port=0)
        with open('/var/www/xl_academy/token.json', 'w') as token:
            token.write(creds.to_json())
        service = build('gmail', 'v1', credentials=creds)
        message = MIMEMultipart()
        message['to'] = req['email']
        message['subject'] = 'XL Academy 試題購買'
        html_filename = '/var/www/xl_academy/media/mail_template/mail.html'
        with open(html_filename, 'r',encoding='utf-8') as html_file:
            html_body = html_file.read()
        image_filename = '/var/www/staticfiles/static/picture/footer-logo.png'
        with open(image_filename, 'rb') as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        html_body = html_body.replace('<!-- INSERT_IMAGE_HERE -->', f'<img style="height:38px" src="data:image/jpeg;base64,{image_data}" alt="Image">')
        html_body = html_body.replace('<!-- INSERT_NAME -->', req['name'])
        html_msg = MIMEText(html_body, 'html')
        message.attach(html_msg)
        for id in list(req['checkedValue']):
                testQuestion = TestQuestion.objects.filter(id= id).first()
                if testQuestion:
                    pdf_filename = f'/var/www/xl_academy/media/{testQuestion.pdf}'
                    with open(pdf_filename, 'rb') as pdf_file:
                        pdf_attachment = MIMEBase('application', 'octet-stream')
                        pdf_attachment.set_payload(pdf_file.read())
                        encoders.encode_base64(pdf_attachment)
                        pdf_attachment.add_header('Content-Disposition', f'attachment; filename={pdf_filename}')
                        message.attach(pdf_attachment)

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
        try:
            message = service.users().messages().send(userId="me", body={"raw": raw_message}).execute()
            return HttpResponse('Email sent successfully!')
        except Exception as error:
            return HttpResponse('Error sending email.')
'''