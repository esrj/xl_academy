from django.shortcuts import render,redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate
from django.contrib import auth
import json
from django.views.decorators.csrf import csrf_exempt
from main.models import Profile,Contact,Testimony,Collage,TestQuestion,Order
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



# Create your views here.
def index(request):
    if request.method == 'GET':
        testimony = Testimony.objects.all().first()
        return render(request,'index.html',locals())
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
        collages = Collage.objects.all().values('id','emblem','name','country','continent','classification')
        pages = Paginator(collages, 24)


        page = request.GET.get('page')
        type = request.GET.get('type')

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
        if type == 'classification':
            for collage in collages:
                if collage['classification'] == '公立大學':
                    collage['classification'] = 'pub'
                elif collage['classification'] == '私立大學':
                    collage['classification'] = 'pri'
                elif '技術學院' in collage['classification'] :
                    collage['classification'] = 'tech'
                else:
                    collage['classification'] = 'lang'
            return render(request,'consult2.html',locals())
        else:
            return render(request,'consult.html',locals())

def shop(request):
    if request.method == 'GET':
        testQuestions = list(TestQuestion.objects.all())
        return render(request,'shop.html',locals())
    if request.method == 'POST':
        req = json.loads(request.body)
        order = Order.objects.create(username =  req['username'],email = req['email'],phone = req['phone'],account = req['account'],price = req['price'],page_id = req['id'])
        order.save()
        return JsonResponse({'errno':0})

def detail(request,id):
    collage = Collage.objects.filter(id=id).values('id','image','name','en_name','info','country','city','continent','address','classification','links','introduction','achievement','reason','popular_departments')
    collage = collage[0]
    popular_departments = collage['popular_departments'].split('\n')
    achievements = collage['achievement'].split('\n')
    return render(request,'detail.html',locals())

def product(request,id):
    if request.method == 'GET':
        testQuestion = TestQuestion.objects.filter(id=id).first()
        testQuestions = TestQuestion.objects.all()
        return render(request,'product.html',locals())


def error_view(request, exception=None, template_name='error.html'):
    status_code = 404
    title = '很抱歉，此頁面不存在或不提供瀏覽'
    if exception:
        status_code = getattr(exception, 'status_code', 404)
    return render(request, 'error.html', locals())