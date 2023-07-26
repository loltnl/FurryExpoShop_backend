from fastapi import APIRouter


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
