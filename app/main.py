from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


try:
    conn = psycopg2.connect(host='localhost', database='FastAPI', user='postgres', password='chitresh123', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("database connection was successfull!")
except Exception as error:
    print("Conneting to database failed")
    print("Error was", error)


my_posts = [
    {
        "title": "Hello World",
        "content": "the first program everyone writes",
        "id": 1
    },
    {
        "title": "hey there",
        "content": "nothing",
        "id": 2

    }

]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/")
def get_posts():
    return{"data": "Hello World"}


@app.get("/posts")
def all_posts():
    cursor.execute("""SELECT * FROM table_1""")
    posts = cursor.fetchall
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 10000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/latest")
def latest():
    post = my_posts[len(my_posts)-1]
    return {"latest post": post}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
        return{"message": "Not Found"}
    return{"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
    # find the index in the array that has required ID
    # my_posts.pop(index)
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id:{id} does not exist")
    my_posts.pop(index)
    return {"message": "Your Post was deleted"}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exists")

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}
