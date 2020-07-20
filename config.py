import redis
#单独放在一个模块中以类封装,也是为了方便不同模式的继承重写
class Config:
    '''配置信息'''
    SECRET_KEY = "SJIRNUFUCN*DHUDNCN13"

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@127.0.0.1:3306/db_ihome"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # REDIS配置
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # flask_session配置
    SESSION_TYPE = "redis"
    # redis实例
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True  # 对cookie中的session_id进行混淆隐藏
    SESSION_PERMANENT = False  # session是否永久有效
    PERMANENT_SESSION_LIFETIME = 3600 * 24# session数据的有效期


class DevelopmentConfig(Config):
    '''开发模式配置'''
    DEBUG = True

class ProductConfig(Config):
    '''生产环境配置'''
    pass


config_map = {
    'develop':DevelopmentConfig,
    'product':ProductConfig
}