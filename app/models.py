from pydantic import BaseModel, EmailStr, field_validator
import pycountry

class CreateUser(BaseModel):
    name: str
    email: EmailStr
    country: str 

    @field_validator('country')
    def validate_country(cls, v):
        try:
            pycountry.countries.lookup(v)
        except LookupError:
            raise ValueError(f"{v} is not a valid ISO country code")
        return v