from smtplib import SMTPRecipientsRefused

from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from GXMHAPP import models
from django.core import mail
import random
from .forms import MH_PersonalDetail_AdminForm

# Create your views here.

def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    if request.method == 'POST':
        login_account = request.POST.get('login_account')
        login_password = request.POST.get('login_password')
        try:
            user = models.UserInfo.objects.get(account=login_account)
        except models.UserInfo.DoesNotExist:
            messages.error(request, '用户不存在')
            return render(request, 'index.html')
        user_password = user.password
        if login_password != user_password:
            messages.error(request, '密码错误')
            return render(request, 'index.html')
        else:
            request.session['user_name'] = user.user_name
            request.session['account'] = user.account
            request.session.set_expiry(0)
            messages.error(request, '登录成功')
            return render(request, 'index.html')
def flush(request):
    request.session.flush()
    messages.error(request, '已登出')
    return HttpResponseRedirect('/')
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        account = request.POST.get('register_account')
        mailbox = request.POST.get('register_mailbox')
        password = request.POST.get('register_password')
        re_password = request.POST.get('register_re_password')
        verification_code_input = request.POST.get('register_verification_code_input')
        verification_code = request.session.get('verification_code')
        if re_password != password:
            messages.error(request, '密码不一致')
            return render(request, 'register.html')
        elif verification_code == '':
            messages.error(request, '验证码已过期')
            return render(request, 'register.html')
        elif verification_code_input != verification_code:
            messages.error(request, '请输入正确的验证码')
            return render(request, 'register.html')
        else:
            try:
                models_account = models.UserInfo.objects.get(account=account).account
            except models.UserInfo.DoesNotExist:
                models_account = ''
            if models_account == account:
                messages.error(request, '用户名已存在')
                return render(request, 'register.html')
            else:
                models.UserInfo.objects.create(user_name=account, account=account, password=password)
                models.Mailbox.objects.create(userinfo=models.UserInfo.objects.get(account=account), mailbox=mailbox)
                messages.error(request, '注册成功')
            return HttpResponseRedirect('/')
def retrieve_password(request):
    if request.method == 'GET':
        return render(request, 'retrieve_password.html')
    if request.method == 'POST':
        account = request.POST.get('account_input')
        mailbox = request.POST.get('mailbox_input')
        password = request.POST.get('password_input')
        re_password = request.POST.get('re_password_input')
        verification_code_input = request.POST.get('verification_code_input')
        verification_code = request.session.get('verification_code')
        try:
            models_userinfo = models.UserInfo.objects.get(account=account)
        except models.UserInfo.DoesNotExist:
            messages.error(request, '用户名不存在')
            return render(request, 'retrieve_password.html')
        try:
            models.Mailbox.objects.get(userinfo=models_userinfo, mailbox=mailbox)
        except models.UserInfo.DoesNotExist:
            messages.error(request, '用户名与邮箱对应不上')
            return render(request, 'retrieve_password.html')
        if re_password != password:
            messages.error(request, '密码不一致')
            return render(request, 'retrieve_password.html')
        elif verification_code == '':
            messages.error(request, '验证码已过期')
            return render(request, 'retrieve_password.html')
        elif verification_code_input != verification_code:
            messages.error(request, '请输入正确的验证码')
            return render(request, 'retrieve_password.html')
        else:
            models_userinfo.password = password
            models_userinfo.save()
            messages.error(request, '修改成功')
            return HttpResponseRedirect('/')
@csrf_exempt
def mailbox(request):
    chars = 'abcdefghijklmnopqrstuvwsyzABCDEFGHIJKLMNOPQRSTUVWSYZ'
    verification_code = ''
    mailbox = request.POST.get('mailbox')
    for x in range(4):
        verification_code += random.choice(chars)
    try:
        mail.send_mail(
            subject='你的验证码',  # 题目
            message='欢迎使用盲盒，为保证您的正常使用，请输入下面的验证码\n' + verification_code + '\n注意：验证码的有效期为30分钟',
            # 消息内容
            from_email='2228795091@qq.com',  # 发送者[当前配置邮箱]
            recipient_list=[mailbox],  # 接收者邮件列表
        )
    except SMTPRecipientsRefused:
        messages.error(request, '邮箱不存在')
        return render(request, 'mailbox.html')
    request.session['verification_code'] = verification_code
    request.session.set_expiry(1800)
    messages.error(request, '已发送')
    return render(request, 'mailbox.html')
def user_detail(request):
    user = models.UserInfo.objects.get(account=request.session.get('account'))
    if request.method == 'POST':
        way = request.POST.get('way')
        if way == 'region_change_finish':
            user_region = request.POST.get('region')
            if user_region == '':
                messages.error(request, '不能为空')
                return render(request, 'user_detail.html', {'user': user})
            user.region = user_region
            user.save()
        elif way == 'name_change_finish':
            user_name = request.POST.get('name')
            if user_name == '':
                messages.error(request, '不能为空')
                return render(request, 'user_detail.html', {'user': user})
            user.user_name = user_name
            user.save()
            request.session['user_name'] = user_name
        elif way == 'portrait_change':
            user_portrait = request.FILES.get('portrait')
            user.portrait = user_portrait
            user.save()
            return render(request, 'user_detail.html', {'user': user})
        return render(request, 'user_detail.html', {'user': user, 'way': way})
    return render(request, 'user_detail.html', {'user': user})
#待优化
def user_collection(request):
    user = models.UserInfo.objects.get(account=request.session.get('account'))
    if request.method == 'POST':
        mh = models.MH_PersonalDetail.objects.get(id=request.POST.get('id'))
        try:
            mh.user_collection
        except models.MH_PersonalDetail.DoesNotExist:
            mh.user_collection.add(user)
    try:
        user_collection = user.mh_personal_detail.all()
    except models.MH_PersonalDetail.DoesNotExist:
        return render(request, 'user_collection.html')
    return render(request, 'user_collection.html', {'user_collection': user_collection})
def place(request):

    mh_personaldetail_form = MH_PersonalDetail_AdminForm()


    school = models.School.objects.all()
    if request.method == 'POST':
        cover = request.FILES.get('cover')
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        region = request.POST.get('region')
        school = models.School.objects.get(school=request.POST.get('school'))
        contact = request.POST.get('contact')
        introduction = request.POST.get('introduction')
        if name == '' or gender == '' or age == '' or region == '' \
                or school == '' or introduction == '' or contact == '':
            messages.error(request, '请输入完整信息')
            return HttpResponseRedirect("/place/")
        else:
            user = models.UserInfo.objects.get(user=request.session.get("user"))
            box_detail = models.MH_PersonalDetail.objects.create(cover=cover, name=name, gender=gender, age=age
                                                                 , region=region, school=school,
                                                                 contact=contact, introduction=introduction)
            try:
                box_detail.user_collection
            except models.MH_PersonalDetail.DoesNotExist:
                box_detail.user_collection.add(user)
    return render(request, 'place.html', {'mh_personaldetail_form': mh_personaldetail_form})
def extract(request):
    school = models.School.objects.all()
    if request.method == 'GET':
        return render(request, 'extract.html', {'school': school})
    if request.method == 'POST':
        select_school = request.POST.get('select_school')
        select_gender = request.POST.get('select_gender')
        if select_school == '0':
            if select_gender == '0':
                mh_personal_detail = models.MH_PersonalDetail.objects.all().order_by("?").first()
            else:
                mh_personal_detail = models.MH_PersonalDetail.objects.filter(select_gender=select_gender).order_by(
                    "?").first()
        else:
            if select_gender == '0':
                mh_personal_detail = models.MH_PersonalDetail.objects.filter(school=select_school).order_by("?").first()
            else:
                mh_personal_detail = models.MH_PersonalDetail.objects.filter(school=select_school,
                                                                             gender=select_gender).order_by(
                    "?").first()
            try:
                user = models.UserInfo.objects.get(account=request.session.get("account"))
            except models.UserInfo.DoesNotExist:
                user = ''
            if user != '' and mh_personal_detail is not None:
                try:
                    user.mh_personal_detail.get(mh_personal_detail=mh_personal_detail)
                except models.UserInfo.DoesNotExist:
                    user.mh_personal_detail.create(mh_personal_detail=mh_personal_detail)
            personal_detail_comment = models.Comment.objects.filter(post=mh_personal_detail)
            return render(request, 'extract.html', {'mh_personal_detail': mh_personal_detail, 'school': school})





"""盲盒"""
def mh(request):
    return render(request, 'mh.html')
def mh_detail(request):
    return render(request, 'user_detail.html')
def mh_forum(request):
    user = models.UserInfo.objects.get(account=request.session.get("account"))
    try:
        mh_list = user.mh_personal_detail.all()
    except models.UserInfo.DoesNotExist:
        return render(request, 'mh_forum.html')
    # 取出当前用户页码
    current_page = int(request.GET.get("page", 1))
    paginator = Paginator(mh_list, 8)
    page = paginator.page(current_page)
    # 大于11页时
    if paginator.num_pages > 11:
        # 当前页码的后5页数超过最大页码时，显示最后10项
        if current_page + 5 > paginator.num_pages:
            page_range = range(paginator.num_pages - 10, paginator.num_pages + 1)
        # 当前页码的前5页数为负数时，显示开始的10项
        elif current_page - 5 < 1:
            page_range = range(1, 12)
        else:
            # 显示左5页到右5页的页码
            page_range = range(current_page - 5, current_page + 5 + 1)
    # 小于11页时显示所有页码
    else:
        page_range = paginator.page_range
    return render(request, 'mh_forum.html', {"page": page, "paginator": paginator,
                                             "current_page": current_page, "page_range": page_range})