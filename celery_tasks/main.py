# 需先导入工程配置文件
#  作用: 比如 获取 Django项目的 redis 配置?!
import os

if not os.getenv('DJANGO_SETTINGS_MODULE'):
    # 设置 添加 Django项目 的 setting 路径 到 os 环境变量
    os.environ['DJANGO_SETTINGS_MODULE'] = 'drf_celery.settings'  # 要对应 自己的 Django 项目名

# 创建celery实例
# main 其实 就是 给celery设置一个名字, 这个名字唯一就可以
# 推荐使用 文件路径
from celery import Celery

app = Celery(main='celery_tasks')

# 加载 config.py 配置文件(设置broker任务队列)
# 配置见下文
app.config_from_object('celery_tasks.config')

# 实现 celery实例对象 自动检测任务
# 参数: 列表需要填写任务的包路径
app.autodiscover_tasks(['celery_tasks._async'])


"""
启动周期任务: celery -A celery_tasks.main beat
启动worker节点，运行任务: celery -A celery_tasks.main worker -l info
"""