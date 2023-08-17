from fastapi import APIRouter
from fastapi import Query

from typing import Annotated

from plugins.gen_jwtdata import generate_jwt
from plugins.gen_jwtdata import check_jwt

from jwt import ExpiredSignatureError

from plugins.gen_servcode import *

from pydantic import BaseModel

from databases.users import ColUsers



UserPage = APIRouter()


@UserPage.post("/register/generate/CAPTCHA")
def GenerateCaptcha():
    return


# @UserPage.post("/register/byphone")
# def RegByphone():
#     return


# @UserPage.post("/register/bywechat")
# def RegByWechat():
#     return

# H5端注册接口
class RegisterByH5(BaseModel):
    username: Annotated[str, Query(title="账号", min_length=3, max_length=16)]
    phone: Annotated[str, Query(title="手机号", min_length=13, max_length=13)]
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
    data = ColUsers().query(params.username)
    if data is None:
        return servicedata(ResQueryNotFound, msg="未找到该用户")
    else:
        return servicedata(ResNormalCheck)
    
    return 

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