from django.shortcuts import render,redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate
from django.contrib import auth
import json
from main.models import Profile,Contact,Testimony,Collage,TestQuestion
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


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



# 試題上傳
@login_required(login_url='/management/')
def upload(request):
    if request.method == 'GET':
        return render(request,'upload.html')
    if request.method == 'POST':
        # pdf = request.FILES.get('pdf')
        image = request.FILES.get('image')
        details = request.POST.get('details')
        details_en = request.POST.get('details_en')
        title = request.POST.get('title')
        title_en = request.POST.get('title_en')
        price = request.POST.get('price')
        introduce = request.POST.get('introduce')
        introduce_en = request.POST.get('introduce_en')
        classification = request.POST.get('classification')
        testQuestion = TestQuestion.objects.create(title=title,price=price,introduce=introduce,classification=classification,title_en = title_en,introduce_en= introduce_en,image=image,details=details,details_en = details_en)
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









