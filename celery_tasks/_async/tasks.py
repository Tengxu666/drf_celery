from celery_tasks.main import app
import time
from message.models import CommodityKill


# 调用 app实例对象的task方法, 装饰这个函数任务,可以设置name参数
@app.task(name='send_code')
def send_code(mobile, sms_code):
    time.sleep(2)
    print(f"短信发送中:手机号{mobile},验证码:{sms_code}")


@app.task(name='order_kill')
def order_kill():
    """
    -请求来到后端，提交一个celery任务---》celery任务异步的执行判断数量是否够，如果够，要生成订单（mysql）
    -秒杀是否成功的结果还没有，直接返回了（返回任务id）
    -前端启动一个定时任务，每隔5s，向后台发送一个查询请求，查询秒杀任务是否执行完成（带着任务id查）
    -如果是未执行状态，或者执行中---》返回给前端，前端不处理，定时任务继续执行
    -又隔了5s，发送查询，查询到秒杀成功的结果，返回给前端，秒杀成功
    """
    print(f"订单秒杀中..")
    # todo：数据库查询商品库存
    time.sleep(1)
    comm = CommodityKill.objects.filter(id=1).first()
    if not comm:
        return False
    # todo：有库存，要生成订单
    if comm.count > 0:
        comm.count -= 1
        comm.save()
        print(f"秒杀成功，剩余{comm.count}")
        return True
    # todo：库存为0，商品已被抢完
    else:
        print(f"商品库存不足...")
        return False
