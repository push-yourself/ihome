# 以目录方式定义蓝图

from flask import Blueprint

# 创建蓝图对象
api = Blueprint('api_1_0',__name__)

# 导入蓝图视图
from . import demo
