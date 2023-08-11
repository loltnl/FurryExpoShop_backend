from typing import Optional

ResNormalGenerial = 20000
ResNormalQuery = 20001
ResNormalWrite = 20011
ResNormalDelete = 20021
ResNormalModify = 20031

ResQueryOutRange = 50001


def servicedata(service_code: int, data: Optional[list | dict] = None, msg: str = "OK"):
    return {
        "code": service_code,
        "data": data,
        "msg": msg
    }