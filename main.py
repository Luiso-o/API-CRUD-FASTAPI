from fastapi import FastAPI
from routers import users_peticiones

app = FastAPI(
    title = "REST API whit fastAPI and MongoDB",
    description= "This is a simple API using fastAPI and MongoDB",
    version="0.0.1",
)

#instanciar routers
app.include_router(users_peticiones.router)