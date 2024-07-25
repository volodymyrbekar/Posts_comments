from ninja import Schema


class UserRegistrationSchema(Schema):
    username: str
    password: str
    email: str


class UserLoginSchema(Schema):
    username: str
    password: str