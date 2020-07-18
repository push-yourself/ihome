import redis
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

# 自定义模块
from manage import app
from config import config_map, Config

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
    return app


# 数据库配置,生成数据库对象
db = SQLAlchemy()


# 利用flask-session,将session数据保存到redis中
Session(app)

# 为flask补充csrf防护,在请求钩子上进行防护机制
CSRFProtect(app)

# 创建redis链接对象
redis_store = redis.StrictRedis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT
)

