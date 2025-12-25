from fastapi import FastAPI
from fastapi.responses import Response
import os
import aiofiles


# Database emulator
picture_db = {
    1: "./pct/jet.jpg",
    2: "./pct/jet2.jpg"
}

PORT = os.getenv('PORT')
if not PORT:
    PORT = 5003


app = FastAPI()

@app.get("/")
async def get_root():
    return {"health": "Pictures Service running"}, {"content": picture_db}

# @app.get("/pictures")
# async def list_pictures():
#     return picture_db

@app.get("/{item}")
async def get_picture(item: int):
    try:
        path_to_file = picture_db[item]
        async with aiofiles.open(path_to_file, "br") as pct:
            cont = await pct.read()
        return Response(content=cont, media_type="image/jpg")

    except Exception as e:
        return {
            "error": 404,
            "message": "file not found"
            }
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(PORT), reload=True) 