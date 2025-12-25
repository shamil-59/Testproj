from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse, Response
import httpx
import os


PORT = os.getenv("PORT")
if not PORT:
    PORT = 5000

# Database emulator
SERVICES = {
    "users":     "http://users-service:5001",
    "books":     "http://books-service:5002",
    "pictures":  "http://pictures-service:5003",
    "videos":    "http://videos-service:5004"
}


app = FastAPI()

@app.get("/")
async def get_root():
    return SERVICES

@app.get("/{service}/{path:path}")
async def gateway_route(service: str, path: str, request: Request):
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail="Service not found")
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SERVICES[service]}/{path}")

    if not path or service not in ['books', 'videos', 'pictures']:
        return response.json()

    else:
        return StreamingResponse(content=iter([response.content]))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host = "0.0.0.0", port = int(PORT), reload=True)
