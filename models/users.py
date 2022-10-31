# Python
from email.policy import default
from typing import Optional
from uuid import UUID
from datetime import date

# Pydantinc
from pydantic import BaseModel, EmailStr, Field, Required

class UserBase(BaseModel):
    """
    User basic information.
    """
    user_id : UUID = Field(Required) 
    email : EmailStr = Field(Required)
    

class UserLogin(UserBase):
    """ 
    User login.
    """
    password : str = Field(
        Required,
        min_length=8
    ) 

class User(BaseModel):
    """
    User information.
    """
    # Obligatory attr.
    first_name : str = Field(
        Required,
        min_length=1,
        max_length=20
    )    
    last_name : str = Field(
        Required,
        min_length=1,
        max_length=20
    )
    birth_date : Optional[date] = Field(default=None)
    