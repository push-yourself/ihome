from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf import CSRFProtect

import redis
# 自定义
from ihome import create_app



# 创建flask的应用对象
app = create_app("develop")





@app.route("/index")
def index():
    return 'index page'

if __name__ == '__main__':
    app.run()
