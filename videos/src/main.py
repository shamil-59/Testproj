from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import os
import aiofiles

# Database emulator
video_db = {
    1: "./video/sale_ship.mp4",
    2: "./video/liner.mp4"
}

PORT = os.getenv('PORT')
if not PORT:
    PORT = 5004


app = FastAPI()

@app.get("/")
async def get_root():
    return {"health": "Videos Service running"}, {"content": video_db}

@app.get("/{item}", response_class=StreamingResponse)
async def get_video(item: int):
    path_to_file = video_db[item]

    async def stream():
        async with aiofiles.open(path_to_file, "br") as pct:
            while chunk := await pct.read(8*1024):
                yield chunk
    
    try:        
        return StreamingResponse(content=stream())
    except Exception as e:
        return {
            "error": 404,
            "message": "file not found"
            }
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(PORT), reload=True) 