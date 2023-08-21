import hashlib
import hmac
import config_reader
from gmssl import sm4


all_salt:dict = config_reader.read_config("all_salt")


def encrypto_str(string: bytes) -> bytes:
    """
    HMAC_SHA256散列计算
    """
    security_key = all_salt["hmac_salt"].encode()
    hmac_obj = hmac.new(security_key, string, hashlib.sha256)
    return hmac_obj.digest()


def encrypto_str_with_local_salt(string: bytes) -> bytes:
    password_key = all_salt["local_password_salt"].encode()
    string = string + password_key
    result = encrypto_str(string)
    return result


def sm4_encode(data:str):
    """
    国密sm4加密
    :param data: 原始数据
    :return: 密文hex
    """
    sm4Alg = sm4.CryptSM4()  # 实例化sm4
    sm4Alg.set_key(all_salt["sm4_salt"].encode(), sm4.SM4_ENCRYPT)  # 设置密钥
    enRes = sm4Alg.crypt_ecb(data.encode())  # 开始加密,bytes类型，ecb模式
    enHexStr = enRes.hex()
    return enHexStr


def sm4_decode(data:str):
    """
    国密sm4解密
    :param data: 密文数据
    :return: 明文hex
    """
    sm4Alg = sm4.CryptSM4()  # 实例化sm4
    sm4Alg.set_key(all_salt["sm4_salt"].encode(), sm4.SM4_DECRYPT)  # 设置密钥
    deRes = sm4Alg.crypt_ecb(bytes.fromhex(data))
    deHexStr = deRes.decode()
    return deHexStr


def gen_captcha_signature(secret_key: str, param_dict: dict) -> str:
    """
    网易易盾签名信息生成
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
