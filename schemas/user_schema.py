#transforma un archivo json a un diccionario
def user_schema (user) -> dict:
    return {"id": str(user["_id"]),
            "username": user["username"],
            "email": user["email"]}

def users_schema (users) -> list:
    return [user_schema(user) for user in users]