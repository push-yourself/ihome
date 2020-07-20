from datetime import datetime
# from ihome import constants
from . import db


class BaseModel:
    '''创建模型基类,为各个模型类所共有属性'''
    create_time = db.Column(db.DateTime,default=datetime.now)
    update_time = db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now)

class User(BaseModel,db.Model):
    '''用户表'''
    __tablename__ = 'ih_user_profile'

    id = db.Column(db.Integer,primary_key=True)#用户编号
    name = db.Column(db.String(32),unique=True,nullable=False)# 用户昵称
    password_hash = db.Column(db.String(128),nullable=False)# 加密密码
    mobile = db.Column(db.String(11),unique=True,nullable=False)# 手机号
    real_name = db.Column(db.String(20))# 真实姓名
    id_card = db.Column(db.String(20))
    avatar_url = db.Column(db.String(128))# 用户头像路径
    # 外键关联
    houses = db.relationship('House',backref='user')# 用户发布的房屋
    orders = db.relationship('Order',backref='user')# 关联订单表

house_facility = db.Table(
    'ih_house_facility',
    db.Column('house_id',db.Integer,db.ForeignKey('ih_house_info.id'),primary_key=True),# 房屋编号
    db.Column('facility_id',db.Integer,db.ForeignKey('ih_facility_info.id'),primary_key=True)# 设置编号
)

class House(BaseModel,db.Model):
    '''房屋信息表'''
    __tablename__ = 'ih_house_info'

    id = db.Column(db.Integer,primary_key=True)# 房屋编号
    title = db.Column(db.String(64),nullable=False)# 标题
    price = db.Column(db.Integer,default=0)# 房子单价
    address = db.Column(db.String(512),default='')# 房屋地址
    room_count = db.Column(db.Integer,default=1)# 房间数目
    acreage = db.Column(db.Integer,default=0)# 房屋面积
    unit = db.Column(db.String(32),default='')# 房屋单元
    capacity = db.Column(db.Integer,default=1)# 房屋容纳的人数
    beds = db.Column(db.String(64),default='')# 房屋床铺的配置
    deposit = db.Column(db.Integer,default=0)# 房屋押金
    min_days = db.Column(db.Integer,default=0)# 最少入住天数
    max_days = db.Column(db.Integer,default=0)# 最多入职天数,0表示不限制
    order_count = db.Column(db.Integer,default=0)# 预订完成的该房屋的订单数
    index_image_url = db.Column(db.String(256),default='')# 房屋主图片路径

    user_id = db.Column(db.Integer,db.ForeignKey('ih_user_profile.id'),nullable=False)# 房屋主人的用户
    area_id = db.Column(db.Integer,db.ForeignKey('ih_area_info.id'),nullable=False)
    # 多对多关联
    facilities = db.relationship('Facility',secondary=house_facility)# 房屋的设置关联
    images = db.relationship('HouseImage')# 房屋的图片
    orders = db.relationship('Order',backref='house')#房屋的订单

class Facility(BaseModel, db.Model):
    '''设施信息'''
    __tablename__ = 'ih_facility_info'

    id = db.Column(db.Integer, primary_key=True)  # 设施编号
    name = db.Column(db.String(32), nullable=False)  # 设施名字


class Area(BaseModel, db.Model):
    '''城区信息表'''
    __tablename__ = 'ih_area_info'

    id = db.Column(db.Integer, primary_key=True)  # 区域编号
    name = db.Column(db.String(32), nullable=False)  # 区域名称
    # 关联房屋表
    houses = db.relationship('House', backref='area')

class HouseImage(BaseModel,db.Model):
    '''房屋图片'''
    __tablename__ = 'ih_house_image'

    id = db.Column(db.Integer,primary_key=True)
    url = db.Column(db.String(256),nullable=False)# 图片的路径
    # 关联房屋信息表
    house_id = db.Column(db.Integer,db.ForeignKey('ih_house_info.id'))

class Order(BaseModel,db.Model):
    '''订单'''
    __tablename__ = 'ih_order_info'

    id = db.Column(db.Integer,primary_key=True)# 订单编号
    begin_date = db.Column(db.DateTime,nullable=False)# 预订起始时间
    end_date = db.Column(db.DateTime,nullable=False)# 预订的结束时间
    days = db.Column(db.Integer,nullable=False)# 预订的总天数
    house_price = db.Column(db.Integer,nullable=False)# 房屋的单价
    amount = db.Column(db.Integer,nullable=False)# 订单的总金额
    status = db.Column(
        db.Enum(
            "WAIT_ACCEPT",  # 待接单,
            "WAIT_PAYMENT",  # 待支付
            "PAID",  # 已支付
            "WAIT_COMMENT",  # 待评价
            "COMPLETE",  # 已完成
            "CANCELED",  # 已取消
            "REJECTED"  # 已拒单
        ),
        default="WAIT_ACCEPT",index=True)
    comment = db.Column(db.Text)# 订单的评论信息或者拒单原因

    # 外键关联信息
    user_id = db.Column(db.Integer, db.ForeignKey("ih_user_profile.id"), nullable=False)  # 下订单的用户编号
    house_id = db.Column(db.Integer, db.ForeignKey("ih_house_info.id"), nullable=False)  # 预订的房间编号


