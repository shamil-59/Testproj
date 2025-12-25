from fastapi import FastAPI
from fastapi.responses import Response
import aiofiles
import os


# Database emulator
book_db = {
    1: "./book/LFS-BOOK-10.0.pdf",
    2: "./book/Advanced-Linux-Programming.pdf"
}

PORT = os.getenv('PORT')
if not PORT:
    PORT = 5002


app = FastAPI()

@app.get("/")
async def list_products():
    return {"health": "Books Service running"}, {"content": book_db}

@app.get("/{book_id}")
async def get_product(book_id: int):
    try:
        path_to_file = book_db[book_id]
        async with aiofiles.open(path_to_file, 'rb') as book:
            resp = await book.read()
        return Response(resp)

    except Exception as e:
        return book_db.get(book_id, {"error": "Product not found"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(PORT), reload=True)