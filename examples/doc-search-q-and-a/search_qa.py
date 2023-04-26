import tiktoken
import uvicorn
from fastapi import FastAPI, HTTPException, Body, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from component.openai import openai
from datastore.redis_datastore import get_datastore
from models.api import (
    QueryRequest,
    Query,
    QueryResponse,
    QaQueryRequest,
    QaQueryResponse
)

GPT_MODEL = "gpt-3.5-turbo"

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


@app.post("/qa", response_model=QaQueryResponse)
async def q_and_a(request: QaQueryRequest = Body(...)):
    try:
        results = await ask(request)
        return QaQueryResponse(query=request.query, message=results)
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal Service Error")


class Message(BaseModel):
    text: str


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_json()
            prompt = message["text"]
            await ask_stream(QaQueryRequest(query=prompt), websocket)
    except WebSocketDisconnect:
        await websocket.close()


@app.get("/")
async def get():
    html_content = """
    <html>
        <head>
            <title>Chat with AI</title>
        </head>
        <body>
            <h1>Chat with AI</h1>
            <form action="" onsubmit="sendMessage(event)">
                <textarea type="text" rows="5" cols="100"  id="messageText" autocomplete="off" placeholder="Type your message..."></textarea>
                <button>Send</button>
            </form>
            <div id='messages'>
                <span id='message'></span>
            </div>
            <script>
                var ws = new WebSocket("ws://" + window.location.host + "/ws");
                ws.onmessage = function(event) {
                    var message = document.getElementById('message');
                    console.log(event.data);
                    if (event.data) {
                        message.innerText = event.data;
                    }
                    //message.appendChild(content);
                    //messages.appendChild(message);
                };
                function sendMessage(event) {
                    var input = document.getElementById("messageText");
                    ws.send(JSON.stringify({'text': input.value}));
                    //input.value = '';
                    event.preventDefault();
                }
            </script>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


async def ask(request):
    query = request.query

    message = await query_message(query, model=GPT_MODEL, token_budget=4096 - 500)
    messages = [
        {"role": "system", "content": "You answer questions about the Tesla."},
        {"role": "user", "content": message},
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0
    )
    response_message = response["choices"][0]["message"]["content"]
    return response_message


async def ask_stream(request, websocket: WebSocket):
    query = request.query

    message = await query_message(query, model=GPT_MODEL, token_budget=4096 - 500)
    print(f"=====================\n{message}\n")
    messages = [
        {"role": "system", "content": "You answer questions about the Tesla."},
        {"role": "user", "content": message},
    ]
    response_message = ""
    try:
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0,
                stream=True,
        )
        for chunk in response:
            msg = chunk["choices"][0]["delta"]
            print(msg)
            if msg.get("content"):
                response_message += msg.get("content")
                await websocket.send_text(response_message)
    except Exception as e:
        print("Error:", e)
    return response_message


async def strings_ranked_by_relatedness(query):
    results = await datastore.query([Query(query=query)])
    strings = []
    if results:
        result = results[0]
        if result and result.results:
            texts = result.results
            for text in texts:
                strings.append(text.text)
    return strings


async def query_message(query: str, token_budget: int, model: str) -> str:
    """Return a message for GPT, with relevant source texts pulled from a dataframe."""
    strings = await strings_ranked_by_relatedness(query)
    introduction = 'Use the following recent news about Tesla to answer subsequent questions. If you can not find an ' \
                   'answer in the news, please write "I can not find an answer".'
    question = f"\n\nQuestion: {query}"
    message = introduction
    for string in strings:
        next_news = f'\n\nTesla news section:\n"""\n{string}\n"""'
        if (
                num_tokens(message + next_news + question, model=model)
                > token_budget
        ):
            break
        else:
            message += next_news
    return message + question


def num_tokens(text: str, model: str = GPT_MODEL) -> int:
    """Return the number of tokens in a string."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


@app.on_event("startup")
async def startup():
    global datastore
    datastore = await get_datastore()


def start():
    uvicorn.run("examples.doc-search-q-and-a.search_qa:app", host="localhost", port=PORT, reload=True)


if __name__ == '__main__':
    start()
