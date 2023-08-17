import hashlib
import hmac
import config_reader

all_salt = config_reader.read_config("all_salt")

def encrypto_str(string: bytes) -> bytes:
    security_key = all_salt["hmac_salt"].encode()
    hmac_obj = hmac.new(security_key, string, hashlib.sha256)
    return hmac_obj.digest()

def encrypto_str_with_local_salt(string: bytes) -> bytes:
    password_key = all_salt["local_password_salt"].encode()
    string = string + password_key
    result = encrypto_str(string)
    return result

def gen_captcha_signature(secret_key: str, param_dict: dict) -> str:
    """ 网易易盾签名信息生成
        Args:
        secret_key 产品私钥
        param_dict 接口请求参数，不包括signature参数
    """
    param_str = ''.join([
    str(name) + str(param_dict[name] or '')
    for name
    in sorted(param_dict.keys())
    ])

    param_str += secret_key

    return hashlib.md5(param_str.encode("utf-8")).hexdigest()
