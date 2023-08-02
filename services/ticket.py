from fastapi import APIRouter


TicketPage = APIRouter()


@TicketPage.get("/list")
def ticket_list():
    return


@TicketPage.post("/buy")
def ticket_buy():
    return


@TicketPage.post("/transfer")
def ticket_transfer():
    return
