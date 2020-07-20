from logging.handlers import RotatingFileHandler

import redis
import logging
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from ihome.utils.commons import ReConverter
# 自定义模块
from config import config_map


# 数据库配置,生成数据库对象
db = SQLAlchemy()

# 创建redis链接对象
redis_store = None

# 设置日志的记录等级
logging.basicConfig(level=logging.DEBUG)
# 创建日志记录器,指明日志保存的路径,每个日志文件的最大大小,保存的日志文件个数上限
file_log_handler = RotatingFileHandler('logs/log',maxBytes=1024*1024*100,backupCount=10)
# 创建日志记录的格式
formatter = logging.Formatter('%(levelname)s%(filename)s:%(lineno)d%(message)s')
# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象(flask app使用的)添加日志记录器
logging.getLogger().addHandler(file_log_handler)


# 以工厂模式
def create_app(config_name):
    """
    创建flask应用对象
    :param config_name: str 配置模式的名字('develop','product')
    :return: app对象
    """
    app = Flask(__name__)
    # 根据配置模式的名字获取配置参数的类
    config_class = config_map.get(config_name)
    # 导入配置信息
    app.config.from_object(config_class)
    # 在创建app时与数据库进行绑定(初始化db信息)

    db.init_app(app)

    # 初始化redis工具
    global redis_store
    redis_store = redis.StrictRedis(host=config_class.REDIS_HOST,port=config_class.REDIS_PORT)
    # 利用flask-session,将session数据保存到redis中
    Session(app)
    # 为flask补充csrf防护,在请求钩子上进行防护机制
    CSRFProtect(app)

    # 为flask添加自定义的转换器
    app.url_map.converters['re'] = ReConverter


    # 解决循环导包问题
    from ihome import api_v1_0
    # 注册蓝图
    app.register_blueprint(api_v1_0.api,url_prefix='/api/v1.0')

    # 注册静态文件蓝图
    from ihome import web_html
    app.register_blueprint(web_html.html)

    return app




