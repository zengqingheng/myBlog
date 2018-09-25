# -*- coding : utf-8 -*-
from django.shortcuts import render
from apps.blog.models import Article,Category,Tag
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.http import Http404
from django.conf import settings
import logging
# Create your views here.

logger = logging.getLogger('blog.views')
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
        logger.error(PageNotAnInteger)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request,'home.html',{'post_list':post_list,'category_list':categories,'tag_list':tags})

def detail(request,id):
    try:
        post = Article.objects.get(id=str(id))
        tags = post.tags.all()
        next_post = post.nextArticle()
        prev_post = post.prevArticle()
    except Article.DoesNotExist:
        raise Http404
    return render(request,'post.html',
                  {'post':post,
                   'tags':tags,
                   'category_list':categories,
                   'next_post':next_post,
                   'prev_post':prev_post,
                   })

categories = Category.objects.all() # 获取全部分类对象
tags = Tag.objects.all() # 获取全部标签对象
months=Article.objects.datetimes('pub_time','month',order='DESC')

def search_category(request,id): # 分类搜索
    posts = Article.objects.filter(category_id=str(id))
    category = categories.get(id=str(id))
    paginator = Paginator(posts,settings.PAGE_NUM)
    try:
        page = request.GET.get('page')
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return  render(request,'category.html',
                   {'post_list':post_list,
                    'category_list':categories,
                    'category':category,
                    'months':months,
                    })

def search_tag(request,tag):
    #posts = Article.objects.filter(tags__name__contains=tag)# contains是将相似的数据提取出来，比如设置标签C,会把所有带C字母的标签全部查询出来
    posts = Article.objects.filter(tags__name__contains=tag)
    tag = tags.get(name=tag)
    paginator = Paginator(posts,settings.PAGE_NUM)
    try:
        page = request.GET.get('page')
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request,'tag.html',
                  {'post_list':post_list,
                   'category_list':categories,
                   'tag':tag,
                   'months':months,
                   })

def archives(request,year,month):
    posts = Article.objects.filter(pub_time__year=year,pub_time__month=month).order_by('-pub_time')
    paginator = Paginator(posts,settings.PAGE_NUM)
    try:
        page = request.GET.get('page')
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request,'archives.html',{
        'post_list':post_list,
        'year_month':year+'年'+month+"月",
        'category_list':categories,
        'months':months,
    })