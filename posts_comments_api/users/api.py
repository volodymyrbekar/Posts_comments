from ninja import Router
from django.contrib.auth import get_user_model
from ninja_jwt import JWTAuth

from .schemas import UserRegistrationSchema, UserLoginSchema


User = get_user_model()
auth = JWTAuth()
router = Router()


@router.post("/register")
def register(request, data: UserRegistrationSchema):
    user = User.objects.create_user(**data.dict())
    return {'message': "User registered successfully", 'user': user}


@router.post("/login")
def login(request, user_data: UserLoginSchema):
    user = auth.authenticate(request, username=user_data.username, password=user_data.password)
    if user is None:
        return {'message': "Invalid credentials"}
    tokens = auth.login(request, user)