import base64
import random
import string
from captcha.image import ImageCaptcha
from io import BytesIO


def generate_captcha() -> tuple:
    """
    :return
    :char_6 六位数验证码
    :base64_image base64验证码图片 
    """
    char_all = string.ascii_letters + string.digits
    char_6 = "".join(random.sample(char_all, 6))
    image = ImageCaptcha().generate_image(char_6)
    buffered = BytesIO()
    image.save(buffered, format="jpg")
    base64_image = b"data:image/jpg;base64," + base64.b64encode(buffered.getvalue())
    return (char_6, str(base64_image))