from fastapi import APIRouter,HTTPException, status, Path, Form
from db.client import conexion
from models.user_entity import User
from schemas.user_schema import user_schema,users_schema
from bson import ObjectId

router = APIRouter (
    prefix="/userdb",
    tags=["userdb"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})


#solicitud GETALL
@router.get("/", response_model=list[User])
async def get_users():
    try:
        users = conexion.find()
        return users_schema(users)
    except Exception as e:
        raise HTTPException(
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener usuarios: {str(e)}"
        )


#solicitud GET
@router.get("/{id}")
async def get_by_id(id: str):
    try:
        user_found = search_user("_id", ObjectId(id))
        if user_found:
            return user_found
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail = f"Ususario no encontrado con el id proporcionado: {id}"
            )   
    except Exception as e:
         raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail = f"Error al obtener usuario: {str(e)}"
            )


#solicitud POST
@router.post("/",response_model = User, status_code = status.HTTP_201_CREATED)
async def create_user(username: str, email: str):
   
   try:
       existing_user = search_user("email", email)
       if existing_user:
           raise HTTPException(
               status_code = status.HTTP_400_BAD_REQUEST,
               detail = "El usuario ya existe"
           )
       
       user_dict = {
           "username" : username,
           "email" : email
       }

       inserted_id = conexion.insert_one(user_dict).inserted_id

       new_user = user_schema(conexion.find_one({"_id" : inserted_id}))

       return User(**new_user)
   except Exception as e:
       raise HTTPException(
           status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail = f"Error al crear el usuario: {str(e)}"
       )


#solicitud PUT
@router.put("/{id}", response_model = User,status_code = status.HTTP_200_OK)
async def update_user(
    id: str = Path(..., title = "ID del usuario a actualizar", min_length=1), 
    username: str = Form(None, title = "Nuevo nombre del usuario", min_length=1),
    email: str = Form(None, title = "Nuevo correo electrónico", min_length=1)
    ):

    try:
        existing_user = search_user("_id", ObjectId(id))
        if existing_user:
            update_fields = {}
            if username is not None:
                update_fields["username"] = username
            if email is not None:
                update_fields["email"] = email
            
            result = conexion.find_one_and_update(
                {"_id":ObjectId(id)},
                {"$set":update_fields},
                return_document=True,
            )

            if result:
                return User(**user_schema(result))
            else:
                return {"error":"No se ha actualizado el usuario"}
        
        else:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"Usuario no encontrado con el id proporcionado: {id}" 
            )
    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"Error al actualizar el usuario: {str(e)}"
        )
            

#solicitud DELETE
@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_user(id : str):

    user_to_delete = conexion.find_one({"_id": ObjectId(id)})

    if user_to_delete:
        deleted_user = conexion.find_one_and_delete({"_id": ObjectId(id)})
        return {"message" : f"Usuario con ID {id} eliminado correctamente."}
    else:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Usuario no encontrado con el ID proporcionado: {id}"
        )

#funcion generica para encontrar un usuario
def search_user(field: str, key):
    try:
        user_data = conexion.find_one({field: key})
        if user_data:
            return User(**user_schema(user_data))
        else:
            return None
    except Exception as e:
        print(f"Error al buscar usuario: {str(e)}")
        return None