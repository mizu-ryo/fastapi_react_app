from fastapi import FastAPI
from db import session
from starlette.middleware.cors import CORSMiddleware

from model import UserTable, User

app = FastAPI()

# cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# hello, world(localhost:8000)
@app.get("/")
def hello_world():
    return({"comment": "hello, world!"})

#　ユーザー情報一覧取得
@app.get("/users")
def get_user_list():
    users = session.query(UserTable).all()
    return users

# ユーザー情報取得(id指定)
@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = session.query(UserTable).filter(UserTable.id == user_id).first()
    return user

# ユーザ情報登録
@app.post("/users")
def post_user(user: User):
    db_user = UserTable(name=user.name, email=user.email, password=user.password)
    session.add(db_user)
    session.commit()
    return user

# ユーザ情報更新
@app.put("/users/{user_id}")
def put_users(user: User, user_id: int):
    target_user = session.query(UserTable).filter(UserTable.id == user_id).first()
    target_user.name = user.name
    target_user.email = user.email
    session.commit()

# ユーザ削除
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    user = session.query(UserTable).filter(UserTable.id == user_id).first()
    session.delete(user)
    session.commit()