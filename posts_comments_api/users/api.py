from ninja import Router
from django.contrib.auth import get_user_model, authenticate
from ninja_jwt.authentication import JWTAuth
from rest_framework_simplejwt.tokens import RefreshToken
from .schemas import UserRegistrationSchema, UserLoginSchema


User = get_user_model()
auth = JWTAuth()
router = Router()


def user_to_dict(user):
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
    }


@router.post("/register")
def register(request, data: UserRegistrationSchema):
    if User.objects.filter(username=data.username).exists():
        return {'message': "User with this username already exists"}
    user = User.objects.create_user(**data.dict())
    return {'message': "User registered successfully", 'user': user_to_dict(user)}


@router.post("/login")
def login(request, user_data: UserLoginSchema):
    user = authenticate(request, username=user_data.username, password=user_data.password)
    if user is None:
        return {'message': "Invalid credentials"}
    refresh = RefreshToken.for_user(user)
    tokens = {
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh)
    }
    return {'tokens': tokens}