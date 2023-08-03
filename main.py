from fastapi import FastAPI


shop = FastAPI()

from services.users import UserPage
shop.include_router(UserPage, prefix="/users")

from services.ticket import TicketPage
shop.include_router(TicketPage, prefix="/ticket")