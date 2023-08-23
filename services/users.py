from fastapi import APIRouter
from fastapi import Query

from typing import Annotated

from plugins.gen_jwtdata import generate_jwt
from plugins.gen_jwtdata import check_jwt

from jwt import ExpiredSignatureError

from plugins.gen_servcode import *

from pydantic import BaseModel

from databases.users import ColUsers

from plugins.shop_captcha import generate_captcha

from plugins.gen_jwtdata import generate_jwt, check_jwt

from plugins.shoppub_crypto import sm4_encode, sm4_decode

from plugins.shop_captcha import generate_random_code


UserPage = APIRouter()

# 注册页面CAPTCHA生成接口
class rgCaptcha(BaseModel):
    username: Annotated[str, Query(title="账号", min_length=3, max_length=16)]
    phone: Annotated[str, Query(title="手机号", min_length=13, max_length=13)]

@UserPage.post("/register/generate/CAPTCHA")
def RegGenerateCaptcha(params: rgCaptcha):
    captcha_user_filter = {
        "_id": 0,
        "username": 1,
        "phone": 1
    }
    
    query = {"$or":[
        {"username":params.username},
        {"phone": params.phone}
        ]}

    data = ColUsers().query(query, captcha_user_filter)
    if data is not None:
        return servicedata(ResCheckInvaild, msg="用户已被注册")
    
    captcha_string, captcha_base64 = generate_captcha()
    data = {
        "captcha_token": sm4_encode(captcha_string),
        "username": params.username,
        "phone": params.phone
    }
    jwt_data = generate_jwt(data)
    result = {
        "jwt": jwt_data,
        "image": captcha_base64
    }
    return servicedata(ResNormalGenerial, result)


@UserPage.post("/register/send_sms")
def RegSendSMS(jwt: str, captcha_string: str):
    try:
        data = check_jwt(jwt)
    except:
        return servicedata(ResCheckExpired, msg="验证码已过期，请刷新页面")
    
    data = data["data"]
    
    jwt_captcha_data = sm4_decode(data["captcha_token"])
    
    if jwt_captcha_data != captcha_string:
        return servicedata(ResCheckInvaild, msg="验证码错误")
    
    captcha_user_filter = {
        "_id": 0,
        "username": 1,
        "phone": 1
    }
    
    query = {"$or":[
        {"username":data["username"]},
        {"phone": data["phone"]}
        ]}

    db_data = ColUsers().query(query, captcha_user_filter)
    
    if db_data is not None:
        return servicedata(ResCheckInvaild, msg="用户已被注册")
    
    sms_code = generate_random_code()
    ## TODO：调用SMS接口
    
    jwt_data = {
        "username": data["username"],
        "phone": data["phone"],
        "sms_code": sm4_encode(sms_code)
    }
    
    result = {
        "jwt": jwt_data
    }
    
    return servicedata(ResNormalGenerial, result, "验证码发送成功")

# @UserPage.post("/register/byphone")
# def RegByphone():
#     return


# @UserPage.post("/register/bywechat")
# def RegByWechat():
#     return

# H5端注册接口
class RegisterByH5(BaseModel):
    jwt: Annotated
    sms_captcha: Annotated[str, Query(title="手机号验证码", min_length=6, max_length=6)]
    password: Annotated[str, Query(title="密码", min_length=8, max_length=20)]
    retype_password: Annotated[str, Query(title="确认密码", min_length=8, max_length=20)]
    captcha_jwt: Annotated[str, Query(title="人机验证码", min_length=6, max_length=6)]
    


# 登录接口
class Login(BaseModel):
    username: Annotated[str, Query(title="账号", min_length=3, max_length=16)]
    password: Annotated[str, Query(title="密码", min_length=8, max_length=20)]
    captcha: Annotated[str, Query(title="人机验证码", min_length=6, max_length=6)]

@UserPage.post("/login")
def UserLogin(params: Login):
    login_filter = {
        "_id": 0,
        "username": 1,
        "password": 1
    }
    data = ColUsers().query({"username":params.username}, login_filter)
    if data is None:
        return servicedata(ResQueryNotFound, msg="未找到该用户")
    if data["password"] != params.password:
        return servicedata(ResCheckInvaild, msg="用户名或密码错误")
    return servicedata(ResNormalCheck, msg="登陆成功")
    


### !!!!调试接口用!!!! 生产环境请注释掉该段代码
@UserPage.post("/login/direct_password_check")
def DirectPasswordCheck():
    return

# JWT测试
@UserPage.get("/testjwt/gen")
def TestJwtGen():
    test = generate_jwt({"user": "test", "privilege": "admin"}, 600)
    return test


@UserPage.get("/testjwt/check")
def TestJwtCheck(jwt_str: str):
    try:
        a = check_jwt(jwt_token=jwt_str)
    except ExpiredSignatureError as e:
        return servicedata(ResCheckInvaild, msg=str(e))
    return servicedata(ResNormalCheck, a, "Check OK")