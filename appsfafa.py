from threading import stack_size
from fastapi import FastAPI, Path, HTTPException, status
from typing import Optional
from httplib2 import Response
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str


my_posts = {
    "name": "sketchbook",
    "price": "239",
    "description": "blank sketchbook",
    "id": 1
}


@app.get("/get-item/{item_id}")
def get_item(item_id: int):
    if item_id not in my_posts:
        return {"ERROR": "Nothing"}
    else:
        return my_posts[item_id]


@app.get("/get-by-name/{item_id}")
def get_item(*, item_id: int = Path(None, description="Enter the test number", gt=0, lt=2), name: Optional[str] = None, test: int):
    for item_id in my_posts:
        if my_posts[item_id]["name"] == name:
            return my_posts[item_id]
    return {"Data": "Not Found"}


@app.post('/posts')
def post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000)
    return {"data": post_dict}
