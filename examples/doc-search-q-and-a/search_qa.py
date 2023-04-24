import uvicorn
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware

from datastore.redis_datastore import get_datastore
from models.api import (
    QueryRequest,
    QueryResponse,
)

app = FastAPI()

PORT = 8000

origins = [
    f"http://localhost:{PORT}"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/query", response_model=QueryResponse)
async def query_main(request: QueryRequest = Body(...)):
    try:
        results = await datastore.query(
            request.queries,
        )
        return QueryResponse(results=results)
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal Service Error")


@app.on_event("startup")
async def startup():
    global datastore
    datastore = await get_datastore()


def start():
    uvicorn.run("examples.doc-search-q-and-a.search_qa:app", host="localhost", port=PORT, reload=True)


if __name__ == '__main__':
    start()
