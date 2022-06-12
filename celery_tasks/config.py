# celery_tasks/config.py
# 配置一个 config.py, 存储配置信息, 实现 配置信息 存在于 单独的配置文件中
# 之后在main.py, 让实例对象 app 加载其中的配置

# 配置 broker 存储在 redis:14号 库
"""
broker: 是一个消息传输的中间件，可以理解为一个邮箱。每当应用程序调用celery的异步任务的时候，
会向broker传递消息，而后celery的worker将会取到消息，进行对于的程序执行。好吧，这个邮箱可以看成是一个消息队列。
"""

broker_url = 'redis://127.0.0.1/14'
# 配置 backend 存储在 redis:15号 库
"""
backend: 通常程序发送的消息，发完就完了，可能都不知道对方时候接受了。为此，celery实现了一个backend，
用于存储这些消息以及celery执行的一些消息和结果。对于 brokers，官方推荐是rabbitmq和redis，
至于backend，就是数据库啦。为了简单起见，我们都用redis。
"""
result_backend = 'redis://127.0.0.1/15'

# --------- 定时任务设置 -----------

# 指定任务序列化方式
task_serializer = 'json'
# 指定结果序列化方式
result_serializer = 'json'
# 指定任务接受的序列化类型.
accept_content = ['json']
timezone = "Asia/Shanghai"  # 时区设置
worker_hijack_root_logger = False  # celery默认开启自己的日志，可关闭自定义日志，不关闭自定义日志输出为空
result_expires = 60 * 60 * 24  # 存储结果过期时间（默认1天）

# 导入任务所在文件
imports = [
    "celery_tasks._async.tasks"
]


# 需要执行任务的配置
beat_schedule = {
    "task1": {
        "task": "send_code",
        "schedule": 3.0,
        "args": (1, 1)  # # 任务函数参数
    }
}

# "schedule": crontab（）与crontab的语法基本一致
# "schedule": crontab(minute="*/10",  # 每十分钟执行
# "schedule": crontab(minute="*/1"),   # 每分钟执行
# "schedule": crontab(minute=0, hour="*/1"),  # 每小时执行
