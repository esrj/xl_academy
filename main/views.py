from django.shortcuts import render,redirect
from django.http import JsonResponse, HttpResponse
import json
from urllib.parse import parse_qs, urlparse
from main.models import Contact,Testimony,Collage,TestQuestion,Ranking
from django.core.paginator import Paginator


def build_youtube_embed_url(video_url):
    if not video_url:
        return ""

    parsed = urlparse(video_url)
    host = parsed.netloc.lower()

    if "youtu.be" in host:
        video_id = parsed.path.strip("/").split("/")[0]
    elif "youtube.com" in host and "/embed/" in parsed.path:
        video_id = parsed.path.split("/embed/")[-1].split("/")[0]
    else:
        video_id = parse_qs(parsed.query).get("v", [""])[0]

    if not video_id:
        return video_url

    return (
        f"https://www.youtube-nocookie.com/embed/{video_id}"
        "?rel=0&modestbranding=1&playsinline=1"
    )

def index(request):
    if request.method == 'GET':
        testimony = Testimony.objects.all().first()
        testimony.video = build_youtube_embed_url(testimony.video)
        language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        print(testimony.video)
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

def school(request):
    if request.method == 'GET':
        language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        if language.split(',')[0] == 'zh-TW'  or language.split(',')[0] == 'zh':
            lang = 'zh'
        else:
            lang = 'en'
        classification = request.GET.get('classification',None)
        if classification == None:
            if lang == 'zh':
                return render(request, 'zh/about.html', locals())
            else :
                return render(request, 'en/about.html', locals())
        # template 下的 consult 是大學介紹
        else:
            collages = Collage.objects.all().values('id','emblem','name','country','continent','classification','en_name')
            pages = Paginator(collages, 24)
            page = request.GET.get('page')
            try:
                objects = pages.page(page)
            except :
                objects = pages.page(1)

            num = (objects.number)
            num_page = (objects.paginator.num_pages)
            all_page = range(1,num_page+1)
            prev = num-1
            next = num+1
            collages = list(objects.object_list)
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
        # courses = Course.objects.all()
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
    navbar_logo = "/static/image/afficient.png"
    navbar_logo_alt = "Afficient Academy logo"
    return render(request,'afficient.html',locals())

def new_consult(request):
    language = request.META.get('HTTP_ACCEPT_LANGUAGE')
    if language.split(',')[0] == 'zh-TW' or language.split(',')[0] == 'zh':
        lang = 'zh'
    else:
        lang = 'en'
    return render(request, 'consult.html', locals())

def robots_txt(request):
    sitemap_url = request.build_absolute_uri('/sitemap.xml')
    content = "\n".join([
        "User-agent: *",
        "Allow: /",
        f"Sitemap: {sitemap_url}",
    ])
    return HttpResponse(content, content_type="text/plain; charset=utf-8")

def sitemap_xml(request):
    pages = [
        ("", "1.0"),
        ("school/", "0.9"),
        ("course/", "0.9"),
        ("service/consult/", "0.9"),
        ("shop/", "0.7"),
        ("afficient/", "0.6"),
    ]
    urls = []
    for path, priority in pages:
        loc = request.build_absolute_uri(f"/{path}" if path else "/")
        urls.append(
            f"<url><loc>{loc}</loc><changefreq>weekly</changefreq><priority>{priority}</priority></url>"
        )

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + "".join(urls) +
        '</urlset>'
    )
    return HttpResponse(xml, content_type="application/xml; charset=utf-8")