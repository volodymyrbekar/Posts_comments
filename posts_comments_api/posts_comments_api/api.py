from ninja import NinjaAPI, Schema

from ninja_extra import NinjaExtraAPI
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import NinjaJWTDefaultController
from posts.api import router as posts_router
from users.api import router as users_router
from comments.api import router as comments_router


api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)
api.add_router('/users/', users_router)
api.add_router('/posts/', posts_router)
api.add_router('/comments/', comments_router)


class UserSchema(Schema):
    username: str
    is_authenticated: bool
    email: str = None


@api.get("/hello")
def hello(request):
    print(request)
    return "hello world"

