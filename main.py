from fastapi import FastAPI, HTTPException, status


app = FastAPI()

posts:list[dict] = [
    {
        "id":1,
        "title":"First blog",
        "description":"this is my first blog"
    },
    {
        "id":2,
        "title":"Second blog",
        "description":"this is my second blog"
    },
    {
        "id":3,
        "title":"Third blog",
        "description":"this is my third blog"
    },
    {
        "id":4,
        "title":"Fourth blog",
        "description":"this is my fourth blog"
    },
    {
        "id":5,
        "title":"Fifth blog",
        "description":"this is my fifth blog"
    }
]

@app.get('/')
def get_message():
    return {"message":"hello"}

@app.get('/api/posts')
def get_posts():
    return posts

@app.get('/api/post/{post_id}')
def get_one_post(post_id:int):
    for post in posts:
        if post["id"] == post_id:
            return post
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="post not found"
    )
