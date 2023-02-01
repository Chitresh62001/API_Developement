from app import main
import fastapi
import uvicorn

api = fastapi.FastAPI()

def configure():
    api.include_router(main.router)

configure()
if __name__ == '__main__':
    uvicorn.run(api)