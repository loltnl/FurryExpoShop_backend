import jwt
from plugins import config_reader
import math
import time

salt = config_reader.read_config("all_salt")["jwt_salt"]


def generate_jwt(data: dict, expire_seconds: int = 600) -> str:
    headers: dict[str, str] = {
        "alg": "HS256",
        "typ": "JWT"
    }
    iat = math.ceil(time.time())
    exp = int(iat + expire_seconds)
    
    payload = {
        "data": data,
        "iat": iat,
        "exp": exp
    }
    
    token = jwt.encode(
        payload=payload,
        headers=headers,
        key=salt,
        algorithm="HS256"
        )
    
    return token

def check_jwt(jwt_token: str) -> dict:
    res = jwt.decode(jwt=jwt_token, key=salt, verify=True, algorithms=["HS256"])
    return res