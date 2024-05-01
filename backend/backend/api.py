from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_jwt.authentication import JWTAuth

from people.models import User, Profile

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)

@api.get("/add", auth=JWTAuth())
def add(request, a: int, b: int):
    return {"result": a + b}

@api.post("/register")
def register(request, username: str, password: str, date_of_birth: str, address: str, phone_number: str):
    user = None
    try:
        user = User.objects.get(username=username)
        return {"error": "User already exists"}
    except User.DoesNotExist:
        pass

    try:
        user = User.objects.create_user(username=username, password=password)
        Profile.objects.create(user=user, date_of_birth=date_of_birth, address=address, phone_number=phone_number)
        user.save()
    except Exception as e:
        if user:
            user.delete()
        return {"error": str(e)}
    return {"success": "User created"}