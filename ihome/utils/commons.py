
# 定义正则表达式
from werkzeug.routing import BaseConverter


class ReConverter(BaseConverter):

    def __init__(self,url_map,regex):
        # 调用父类的初始化方法
        super().__init__(url_map)
        # 保存正则
        self.regex = regex