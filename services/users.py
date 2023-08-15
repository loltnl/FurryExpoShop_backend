from fastapi import APIRouter

from plugins.gen_jwtdata import generate_jwt
from plugins.gen_jwtdata import check_jwt

from jwt import ExpiredSignatureError

from plugins.gen_servcode import *
UserPage = APIRouter()

@UserPage.post("/register/generate/CAPTCHA")
def GenerateCaptcha():
    return


@UserPage.post("/register/byphone")
def RegByphone():
    return


@UserPage.post("/register/bywechat")
def RegByWechat():
    return


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