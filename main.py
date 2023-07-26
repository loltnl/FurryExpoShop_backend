from fastapi import FastAPI


shop = FastAPI()

from services.users import UserPage
shop.include_router(UserPage, prefix="/users")