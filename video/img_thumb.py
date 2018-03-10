# coding:utf-8
import subprocess
import re
import sys
import os
from django.core.wsgi import get_wsgi_application
sys.path.extend(['/Users/hejun/Documents/project/django_env/videolearn',])
os.environ.setdefault("DJANGO_SETTINGS_MODULE","videolearn.settings")
application = get_wsgi_application()
import django
django.setup()
from video.models import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.join(BASE_DIR,'media')

def get_duration(filename):
    s = subprocess.Popen('ffmpeg -i "{0}"'.format(filename),shell=True,stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    ss = s.stdout.read()
    print( 'ss:%s :ss' %ss)
    duration = re.findall(r'Duration:(.*?),',str(ss))[0]
    print(filename,duration)
    return (filename,duration)

def get_video_img(filename):
    s = subprocess.Popen('ffmpeg -i "{0}" -y -f mjpeg -ss 0.5 -t 0.001 -s 320x240 "{1}.jpg"'.format(filename,filename.split('.')[0]),shell=True,stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    return True

file_dir = "video/Python基础"

root_dir = os.path.join(BASE_DIR,file_dir)
print(root_dir)
for i in os.listdir(root_dir):
    print(file_dir,i)
    video_duration = get_duration(os.path.join(root_dir,i))
    img_name = get_video_img(os.path.join(root_dir,i))
    # 插入视频数据
    v = Video.objects.get_or_create(
        name = i.split('.')[0],
        link = os.path.join(file_dir,i),
        img = os.path.join('video_img',file_dir,str(i.split('.')[0])+'.jpg'),
        # passwd = “”
        introduce = "Python基础",
        cate = Cate.objects.get(name='Python基础'),
        hour = video_duration[1]
    )
    print("》》》插入视频成功！")
    # 插入专辑数据
    vv = Video.objects.get(
        name = i.split('.')[0],
        link = os.path.join(file_dir,i),
        img = os.path.join('video_img',file_dir,str(i.split('.')[0])+".jpg"),
        # passwd = models.CharField(verbose_name='播放密码',max_length=10,null=True,blank=True)
        introduce = "Python基础",
        cate = Cate.objects.get(name='Python基础'),
        hour = video_duration[1]
    )
    sets = Set.objects.create(
        name = 'Python基础',
        video = vv
    )
    print("》》》插入专辑成功")
