import time
from celery.result import AsyncResult
from django.http import JsonResponse
from celery_tasks._async.tasks import send_code, order_kill, app
from datetime import datetime, timedelta


def async_send_code(request):
    """
    异步处理
    场景说明：用户注册时，需要发注册邮件和注册短信。
    """
    # todo：开启异步短信发送
    task_id = send_code.delay("157322285620", "123456")
    # todo：开启延时任务
    eta = datetime.utcnow() + timedelta(seconds=5)
    task2_id = send_code.apply_async(args=("5s后发送", "12313"), eta=eta)
    print(f"任务ID:{task_id}、{task2_id}")
    return JsonResponse({"msg": "success"})


def order_seconds_kill(request):
    """
    订单秒杀
    场景说明：所有秒杀订单进入消息队列，库存消耗完成之后秒杀失败
    """
    task_id = order_kill.delay()
    time.sleep(1)
    task = AsyncResult(id=str(task_id), app=app)
    if task.successful():
        result = task.get()
        if result:
            print("购买成功")
        else:
            print("购买失败")
    return JsonResponse({"msg": "success"})

