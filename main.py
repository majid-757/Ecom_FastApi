from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from tortoise.signals import post_save
from typing import List, Optional, Type
from tortoise import BaseDBAsyncClient

from models import *
from authentication import get_hashed_password



app = FastAPI()



@post_save(User)
async def create_business(
    sender: "Type[User]",
    instance: User,
    created: bool,
    using_db: "Optional[BaseDBAsyncClient]",
    update_fields: List[str],
)->None:
    
    if created:
        business_obj = await Business.create(
            business_name = instance.username,
            owner = instance,

        )
        await business_paydantic.from_tortoise_orm(business_obj)
        await business_paydantic.construct()









@app.post("registration/")
async def user_registration(user:user_paydanticIn):
    user_info = user.dict(exclude_unset=True)
    user_info["password"] = get_hashed_password(user_info["password"])
    user_obj = await User.create(**user_info)
    new_user = await user_paydantic.from_tortoise_orm(user_obj)
    return {
        "status":"ok",
        "data": f"Hello {new_user.username}, Thanks for choosing our services. Please check your email inbox and click on the link below to confirm your registration",


    }






@app.get("/")
def index():
    return {"Message": "Hi"}


register_tortoise(
    app,
    db_url="sqlite://database.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,

)



