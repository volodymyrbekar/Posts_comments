from ninja import NinjaAPI, Schema

from ninja_extra import NinjaExtraAPI
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import NinjaJWTDefaultController
from posts.api import router as posts_router
from users.api import router as users_router



api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)
api.add_router("/posts/", posts_router)
api.add_router('/users/', users_router)



class UserSchema(Schema):
    username: str
    is_authenticated: bool
    email: str = None


@api.get("/hello")
def list_posts(request):
    print(request)
    return "List of posts"


@api.get("/user", response=UserSchema, auth=JWTAuth())
def get_user(request):
    return request.user