from fastapi import APIRouter
from databases.ticket import ColTicket

TicketPage = APIRouter()


@TicketPage.get("/list")
def ticket_list():
    return ColTicket().list()


@TicketPage.post("/buy")
def ticket_buy():
    return


@TicketPage.post("/transfer")
def ticket_transfer():
    return
