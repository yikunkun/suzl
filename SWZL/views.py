from django.shortcuts import render, HttpResponse, redirect
# 上传图片
from django.conf import settings
from SWZL.models import Recruit
from SWZL import models
from django.conf import settings
from SWZL.forms import RecruitForm, RegisterForm
from itertools import chain
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views import View
from django.db.models import Q
from utils.pagination import Pagination
import copy


# 定义q查询并返回
class GeySearchContain(object):

    def get_search_contain(self, query_list):
        query = self.request.GET.get('query', '')
        # 生成一个搜索对象
        q = Q()
        # 标记搜索条件为“或”查询
        q.connector = 'OR'
        # 把搜索条件加入到q中
        for i in query_list:
            q.children.append(Q(('{}__contains'.format(i), query)))
        return q


# 用户注册
def register(request):
    form_obj = RegisterForm()
    if request.method == 'POST':
        form_obj = RegisterForm(request.POST)
        if form_obj.is_valid():
            obj = form_obj.save()
            obj.set_password(obj.password)
            obj.save()
            return HttpResponse('注册成功')
    return render(request, 'user/regiser.html', {'form_obj': form_obj})


# 用户登录
def login(request):
    error_message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        obj = auth.authenticate(request, username=username, password=password)
        if obj:
            auth.login(request, obj)
            return redirect('suzl:recruit_list')
        else:
            error_message = '用户名或者密码错误'
    return render(request, 'user/login.html', {'error_message': error_message})


# 失物信息的发布
@login_required()
def recruit(request):
    obj = models.Recruit(announcer=request.user)
    form_obj = RecruitForm(instance=obj)
    if request.method == 'POST':
        form_obj = RecruitForm(request.POST, request.FILES)
        if form_obj.is_valid():
            form_obj.save()
        return HttpResponse('上传完成')
    return render(request, 'user/recruit.html', {'form_obj': form_obj})


# 失物和招领信息的显示
class RecruitList(View, GeySearchContain):
    def get(self, request):
        q = self.get_search_contain(['contact', 'lost_type', 'lost_time', 'lost_place','detailed_description'])
        all_recruit = models.Recruit.objects.filter(q, status='finding', )
        all_recruitment = models.Recruitment.objects.filter(q, status='finding', )
        all_recruits = chain(all_recruit, all_recruitment)

        all_recruits = sorted(all_recruits, key=lambda x: x.pub_time, reverse=True)

        query_params = copy.deepcopy(request.GET)

        # 要想修改querydict对象要设置为True
        query_params._mutable = True
        # 把路径编码从<QueryDict: {'page': ['3']}>到page = 3
        # print(query_parmas.urlencode())
        # print(query_parmas)
        pagination = Pagination(request, len(all_recruits), query_params, 8, 3)

        return render(request, 'user/recruit_list.html', {'all_recruit': all_recruits[pagination.start:pagination.end],
                                                          'pages': pagination.show_li, }

                      )


# 失物与招领信息的分别显示
class LostList(View,GeySearchContain):
    def get(self,request):
        q = self.get_search_contain(['contact', 'lost_type', 'lost_time', 'lost_place', 'detailed_description'])
        message_list = models.Recruit.objects.filter(q,status='finding')
        message_list = sorted(message_list, key=lambda x: x.pub_time, reverse=True)
        query_params = copy.deepcopy(request.GET)

        # 要想修改querydict对象要设置为True
        query_params._mutable = True
        # 把路径编码从<QueryDict: {'page': ['3']}>到page = 3
        # print(query_parmas.urlencode())
        # print(query_parmas)
        pagination = Pagination(request, len(message_list), query_params, 8, 3)
        return render(request, 'user/lost_find.html', {'all_recruit': message_list[pagination.start:pagination.end],
                                                   'pages': pagination.show_li, }
                  )

class FindList(View,GeySearchContain):
    def get(self,request):
        q = self.get_search_contain(['contact', 'lost_type', 'lost_time', 'lost_place', 'detailed_description'])
        message_list = models.Recruitment.objects.filter(q,status='finding')
        message_list = sorted(message_list, key=lambda x: x.pub_time, reverse=True)
        query_params = copy.deepcopy(request.GET)

        # 要想修改querydict对象要设置为True
        query_params._mutable = True
        # 把路径编码从<QueryDict: {'page': ['3']}>到page = 3
        # print(query_parmas.urlencode())
        # print(query_parmas)
        pagination = Pagination(request, len(message_list), query_params, 8, 3)
        return render(request, 'user/lost_find.html', {'all_recruit': message_list[pagination.start:pagination.end],
                                                       'pages': pagination.show_li, }
                      )

# 失物信息的详细查看
def lost_detail_view(request, info_id=None):
    obj = models.Recruit.objects.filter(id=info_id).first()

    return render(request, 'user/detail_recruit.html', {'obj': obj})

# 招领信息的详细查看
def find_detail_view(request, info_id=None):
    obj = models.Recruitment.objects.filter(id=info_id).first()
    return render(request, 'user/detail_recruitment.html', {'obj': obj})
