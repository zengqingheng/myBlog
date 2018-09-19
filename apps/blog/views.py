from django.shortcuts import render
from apps.blog.models import Article
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage
from django.http import Http404
from django.conf import settings

# Create your views here.

def home(request):
    """
    :paginator 分页程序
    """
    posts = Article.objects.all()
    paginator = Paginator(posts,settings.PAGE_NUM) #每页显示数量，对应settings.py中的PAGENUM
    page = request.GET.get('page') # 获取url中的page参数
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request,'home.html',{'post_list':post_list})

def detail(request,id):
    try:
        post = Article.objects.get(id=str(id))
        post.viewed()
        tags = post.tags.all()
    except Article.DoesNotExist:
        raise Http404
    return render(request,'post.html',{'post':post,'tags':tags})