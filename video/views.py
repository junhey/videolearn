from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from .models import *

# Create your views here.
# 分页代码
def getPage(request, video_list):
    paginator = Paginator(video_list, 12)
    try:
        page = int(request.GET.get('page', 1))
        video_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        video_list = paginator.page(1)
    return video_list

# 首页
def index(request):
    # 获取电影分类作为菜单数据
    menu_list = Cate.objects.all()
    # 返回最新的3条数据
    new_list = Video.objects.all().order_by('-create_time')[:3]
    # 返回最热的4条数据
    hot_list = Video.objects.all().order_by('-views')[:4]
    # 返回Python基础的最新8条数据
    python_list = Video.objects.filter(cate=Cate.objects.get(name='Python基础')).order_by('-create_time')[:8]
    # # 返回数据分析的最新4条数据
    # analysis_list_1 = Video.objects.filter(cate=Cate.objects.get(name='数据分析')).order_by('-create_time')[:4]
    # # 返回数据分析的最新4条数据
    # analysis_list_2 = Video.objects.filter(cate=Cate.objects.get(name='数据分析')).order_by('-create_time')[4:8]
    # # 返回数据分析的最新4条数据
    # analysis_list_3 = Video.objects.filter(cate=Cate.objects.get(name='数据分析')).order_by('-create_time')[8:12]
    # # 返回GUI开发的最新4条数据
    # gui_list = Video.objects.filter(cate=Cate.objects.get(name='GUI编程')).order_by('-create_time')[:4]
    # # 返回Web开发的最新4条数据
    # web_list = Video.objects.filter(cate=Cate.objects.get(name='Web开发')).order_by('-create_time')[:4]
    # # return HttpResponse(locals())
    return render(request,'index.html',locals())

# 电影详情页
def videoDetail(request,vid):
    # 获取电影分类作为菜单数据
    menu_list = Cate.objects.all()
    # 获取电影数据
    id = int(vid)
    video = Video.objects.get(id=vid)
    # 获取电影专辑
    try:
        set_name = Set.objects.get(video=id).name
        video_set = Set.objects.filter(name = set_name)
    except:
        random_video = Video.objects.order_by('?')[:5]
    # 增加访问人数
    try:
        video.views += 1
        video.save()
    except Exception as e:
        print(e)
    # 获取点赞人数
    try:
        likes = Likes.objects.filter(video=video).count()
    except:
        likes = 0
    # 添加观看记录
    try:
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user.username)
            history = History.objects.create(user=user,video=video)
            history.save()
    except Exception as e:
        print(e)
    return render(request,'single.html',locals())

# 观看历史页
@login_required()
def viewHistory(request):
    # 获取电影分类作为菜单数据
    menu_list = Cate.objects.all()
    # 获取用户
    user = User.objects.get(username=request.user.username)
    # 获取用户的观看历史记录
    history_list = History.objects.filter(user=user)
    # 分页
    cate_video_list = getPage(request,history_list)
    return render(request,'history.html',locals())
    # return HttpResponse("这是观看历史页")

# 电影分类页
def videoCate(request,cateid):
    # 获取电影分类作为菜单数据
    menu_list = Cate.objects.all()
    # 获取分类电影
    catename = Cate.objects.get(id=cateid)
    video_list = Video.objects.filter(cate = catename)
    # 分页
    cate_video_list = getPage(request,video_list)
    return render(request,'cate.html',locals())

# 验证码
def check_code(request):
    import io
    from . import check_code as CheckCode

    stream = io.BytesIO()
    # img图片对象,code在图像中写的内容
    img, code = CheckCode.create_validate_code()
    img.save(stream, "png")
    # 图片页面中显示,立即把session中的CheckCode更改为目前的随机字符串值
    request.session["CheckCode"] = code
    return HttpResponse(stream.getvalue())

# 登录页面
def logIn(request):
    # 判断是否已经登录
    if request.user.is_authenticated:
        return redirect(request.META.get('HTTP_REFERER','/'))
    else:
        if request.method == 'GET':
            request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
            return render(request,'login.html',locals())
        elif request.method == 'POST':
            username = request.POST.get("username",'')
            password = request.POST.get("password",'')
            if username != '' and password != '':
                user = authenticate(username=username, password=password)
                print(user)
                if user is not None:
                    login(request,user)
                    print("登录成功！")
                    return redirect(request.session['login_from'])
                else:
                    print(username,password,user)
                    errormsg = '用户名或密码错误！'
                    return render(request,'login.html',locals())
            else:
                return JsonResponse({"e":"chucuo"})
    # return HttpResponse("这是登录页")

# 注册页面
def register(request):
    if request.method == 'GET':
        request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
        return render(request,'register.html',locals())
    elif request.method == 'POST':
        # 接收表单数据
        username = request.POST.get("email", '')
        password = request.POST.get("password", '')
        email = request.POST.get("email", '')
        checkcode = request.POST.get("check_code")
        # 判断数据是否正确
        if username != '' and password != '' and checkcode == request.session['CheckCode'].lower():
            # 判断用户是否存在
            if User.objects.filter(username=username).exists() == False:
                # 注册
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()
                # 登录
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request,user)
                # 重定向跳转
                return redirect(request.session["login_from"],'/')
                
            else:
                errormsg = '用户名已存在！'
                return render(request,'register.html',locals())
        else:
            return JsonResponse({"success": False, "msg": "信息填写错误:{0},{1},{2},{3}".format(username,password,checkcode,request.session['CheckCode'].lower())})
    # return HttpResponse("这是注册页")

# 注销
def logOut(request):
    try:
        logout(request)
    except Exception as e:
        print(e)
    return redirect(request.META['HTTP_REFERER'])

# 电影点赞功能
@login_required
def like(request):
    if request.method == 'POST':
        videoid = request.POST.get("vid")
        video = Video.objects.get(id=videoid)
        user = request.user
        try:
            Likes.objects.get_or_create(
                    user=user,
                    video=video,
                )
            # InfoKeep.save()
            return JsonResponse({"success":True})
        except Exception as e:
            return JsonResponse({"success":False})
    else:
        return JsonResponse({"success":False})


