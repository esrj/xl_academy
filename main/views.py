from django.shortcuts import render,redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate
from django.contrib import auth
import json
from django.views.decorators.csrf import csrf_exempt
from main.models import Profile,Contact,Testimony,Collage,TestQuestion,Order,Course,Ranking
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



# Create your views here.
def index(request):
    if request.method == 'GET':
        testimony = Testimony.objects.all().first()
        language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        if language.split(',')[0] == 'zh-TW'  or language.split(',')[0] == 'zh':
            return render(request,'zh/index.html',locals())
        else:
            return render(request,'en/index.html',locals())
    if request.method == 'POST':
        req = json.loads(request.body)
        username = req['username']
        email = req['email']
        phone = req['phone']
        content = req['content']
        if (phone is None or phone.strip() == '' or phone == 'none'):
            contact = Contact.objects.create(name = username,email = email,content = content)
        else:
            contact = Contact.objects.create(name = username,email = email,phone=phone,content = content)
        contact.save()
        return JsonResponse({'errno':0})
    if request.method == 'PUT':
        testimony = Testimony.objects.all().first()
        print(testimony.video)
        return  JsonResponse({'video':str(testimony.video)})


def consult(request):
    if request.method == 'GET':
        language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        if language.split(',')[0] == 'zh-TW'  or language.split(',')[0] == 'zh':
            lang = 'zh'
        else:
            lang = 'en'
        classification = request.GET.get('classification',None)
        if classification == None:
        # zh , en 下的 consult 是 11 點介紹，無串接資料庫
            if lang == 'zh':
                return render(request,'zh/consult.html',locals())
            else :
                return render(request,'en/consult.html',locals())
        # template 下的 consult 是大學介紹，有串接資料苦
        else:
            collages = Collage.objects.all().values('id','emblem','name','country','continent','classification','en_name')
            pages = Paginator(collages, 24)
            page = request.GET.get('page')
            try:
                objects = pages.page(page)
            except PageNotAnInteger:
                objects = pages.page(1)
            except EmptyPage:
                objects = pages.page(paginator.num_pages)
            num = (objects.number)
            num_page = (objects.paginator.num_pages)
            all_page = range(1,num_page+1)
            prev = num-1
            next = num+1
            collages = list(collages)[4*(num-1):24*(num)]
            for collage in collages:
                if collage['classification'] == '公立大學':
                   collage['classification'] = 'pub'
                elif collage['classification'] == '私立大學':
                   collage['classification'] = 'pri'
                elif '技術學院' in collage['classification'] :
                   collage['classification'] = 'tech'
                else:
                   collage['classification'] = 'lang'
            return render(request, 'school.html', locals())

def shop(request):
    if request.method == 'GET':
        language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        if language.split(',')[0] == 'zh-TW'  or language.split(',')[0] == 'zh':
            lang = 'zh'
        else:
            lang = 'en'
        testQuestions = list(TestQuestion.objects.all())
        return render(request,'shop.html',locals())
    if request.method == 'POST':
        req = json.loads(request.body)
        order = Order.objects.create(username =  req['username'],email = req['email'],phone = req['phone'],account = req['account'],price = req['price'],page_id = req['id'])
        order.save()
        return JsonResponse({'errno':0})

def detail(request,id):
    language = request.META.get('HTTP_ACCEPT_LANGUAGE')
    if language.split(',')[0] == 'zh-TW'  or language.split(',')[0] == 'zh':
            lang = 'zh'
    else:
            lang = 'en'
    collage = Collage.objects.filter(id=id).values('id','image','name','en_name','info','country','city','continent','address','classification','links','introduction','achievement','reason','popular_departments','achievement_en','popular_departments_en','reason_en','introduction_en','city_en','country_en')
    collage = collage[0]
    popular_departments = collage['popular_departments'].split('\n')
    popular_departments_en = collage['popular_departments_en'].split('\n')
    achievements = collage['achievement'].split('\n')
    achievements_en = collage['achievement_en'].split('\n')
    return render(request,'detail.html',locals())

def product(request,id):
    if request.method == 'GET':
        language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        if language.split(',')[0] == 'zh-TW'  or language.split(',')[0] == 'zh':
            lang = 'zh'
        else:
            lang = 'en'
        testQuestion = TestQuestion.objects.filter(id=id).first()
        testQuestions = TestQuestion.objects.all()
        return render(request,'product.html',locals())

def course(request):
    language = request.META.get('HTTP_ACCEPT_LANGUAGE')
    if language.split(',')[0] == 'zh-TW'  or language.split(',')[0] == 'zh':
        lang = 'zh'
    else:
        lang = 'en'

    rankings = Ranking.objects.all()
    if  request.GET.get('type') == 'tutor':
        return render(request,'tutor.html',locals())
    else:
        courses = Course.objects.all()
        return render(request,'course.html',locals())

def error_view(request, exception=None, template_name='error.html'):
    language = request.META.get('HTTP_ACCEPT_LANGUAGE')
    if language.split(',')[0] == 'zh-TW'  or language.split(',')[0] == 'zh':
        return render(request,'zh/error.html',locals())
    else:
        return render(request,'en/error.html',locals())


def afficient(request):
    language = request.META.get('HTTP_ACCEPT_LANGUAGE')
    if language.split(',')[0] == 'zh-TW' or language.split(',')[0] == 'zh':
        lang = 'zh'
    else:
        lang = 'en'
    return render(request,'afficient.html',locals())


