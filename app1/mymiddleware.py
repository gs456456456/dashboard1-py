import threading
from apscheduler.schedulers.background import BackgroundScheduler
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
from app1.models import lightStatus
import os


# try:
#     from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
# except ImportError:
#     MiddlewareMixin = object

class StartupMiddleware(object):
    def __init__(self):
        #启动后台任务APScheduler
        init_scheduler()

        from django.core.exceptions import  MiddlewareNotUsed
        raise MiddlewareNotUsed #TIP 抛出此异常，则Django将从 middleware 栈中移出该 middleware，请求就不会经过此middleware

    def process_request(self, request):
        print("*****enter startup middleware")



def colorcount():
    lightcolor = list(lightStatus.objects.all().values_list('nid'))
    lightcolorlist = []
    red = 0
    yellow = 0
    blue = 0
    green = 0
    for x in lightcolor:
        for y in x:
            lightcolorlist.append(y)
    for item in lightcolorlist:
        if item == 1:
            red += 1
        elif item == 2:
            yellow += 1
        elif item == 3:
            blue +=1
        elif item == 4:
            green +=1
        else:
            print('color wrong!')
    print(lightcolorlist)
    return [red,yellow,blue,green]


scheduler = None
def init_scheduler():
    global scheduler
    lock = threading.Lock()  # TIP 多线程同步代码
    with lock:
        if scheduler and scheduler.running:
            print('*****APScheduler is already started, pid:{}, tid:{}'.format(os.getpid(), threading.current_thread().getName()))
            return scheduler
        executors = {
            'default': ThreadPoolExecutor(5),#线程模式下进程池大小
            'processpool': ProcessPoolExecutor(5),#进程模式下进程池大小
        }
        job_defaults = {
            'coalesce': True, #如果有几次未执行，条件可以时是否只执行一次
            'max_instances': 1, #同一个job同一时间最多有几个实例再跑
        }

        scheduler = BackgroundScheduler(executors=executors, job_defaults=job_defaults)
        scheduler.add_job(colorcount, 'interval', seconds=5)
        scheduler.start()

        return scheduler