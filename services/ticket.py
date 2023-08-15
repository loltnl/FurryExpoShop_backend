from fastapi import APIRouter, Query
from databases.ticket import ColTicket
from plugins.gen_servcode import *
from plugins.config_reader import read_config
from typing import Annotated
from math import ceil


TicketPage = APIRouter()

query_limit = read_config("genernal")["query_limit"]
query_limit_minimal = query_limit["minimal"]
query_limit_maxium = query_limit["maxium"]

@TicketPage.get("/list")
def ticket_list(
    limit: Annotated[int , Query(ge=query_limit_minimal, le=query_limit_maxium)] = 50,
    page: Annotated[int, Query(ge=1, le=999999)] = 1
    ):
    print(query_limit)
    cnt = ColTicket().count_total_document()
    print(page)
    total_page = ceil(cnt / page)
    gen_data = {
        "entry_count": cnt,
        "minimal_limit": query_limit_minimal,
        "maxium_limit": query_limit_maxium,
        "limit": limit,
        "total_page": total_page,
        "list": None
    }
    
    print(page, total_page)
    if page > total_page:
        return servicedata(ResQueryOutRangeError, gen_data, "页数超过查询限制")
    else:
        lst = ColTicket().list(limit, page - 1)
        gen_data["list"] = lst
        return servicedata(ResNormalQuery, gen_data)


@TicketPage.post("/buy")
def ticket_buy():
    return


@TicketPage.post("/transfer")
def ticket_transfer():
    return
