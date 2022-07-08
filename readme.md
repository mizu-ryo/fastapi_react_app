# fastapi_react_app

# はじめに

クローンしたいディレクトリに移動し以下を実行。
```
$ git clone 
```

# 環境構築

まずはビルドする。
```
$ docker compose build
```

ビルドが修了したら、以下を実行しreact-appを作成する。
```
$ docker compose run --rm front sh -c "npm install -g create-react-app && create-react-app react-app"
```
するとforntディレクトリ下にreact-appディレクトリが作成される。

しかし、dockerで自動生成されたファイルやディレクトリは編集権限がないので、権限を与える。

```
$ cd front
$ sudo chown -R <user_name> react-app
```

次に、`docker-compose.yml`とfrontの`Dockerfile`を一部変更。


```
- docker-compose.yml -

< 変更後 >
  front:
    build: ./front
    container_name: "fastapi_react_app_front"
    volumes:
      - ./front:/usr/src/app
      - /usr/src/app/react-app/node_modules # あとで追加　<- コメントアウトを外す
    ports:
      - "3000:3000"
    stdin_open: true
```

```
- fornt/Dockerfile -

< 変更後 >
FROM node:18.4.0-alpine

#WORKDIR /usr/src/app/ <- コメントアウトする
WORKDIR /usr/src/app/react-app <- コメントアウトを外す

# 後で追加
COPY ./react-app . <- コメントアウトを外す

# 後で追加
RUN yarn install <- コメントアウトを外す

CMD [ "yarn", "start" ]
```

もう一度ビルドする。
```
$ docker compose build
```

これで環境構築終了。

# 起動
```
$ docker compose up
```
## back
- `http://localhost:8000`
- `http://localhost:8000/docs`

## front
- `http://localhost:3000`


# npm install
開発を進めていく上で、nodeモジュールが必要になってくる。


たとえば、画面遷移を行う際に必要となる、`react-router-dom`などがある。

その時は以下の手順でモジュールをインストールする。
※`-g`を付けること。
```
$ docker compose run --rm front sh -c "npm install -g react-router-dom"
```

するとfrontの`package.json`にインストールしたものが記載される。
```
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.3.0", <- 追加される
    "react-scripts": "5.0.1",
    "web-vitals": "^2.1.4"
```

ただ、dockerのコンテナ内では使うことが出来ないので、再ビルドし`yarn install`を行う。
```
$ docker compose build
```

これで、reactでimportできるようになる。

(例)
```
import './App.css';
import {} from 'react-router-dom';

function App() {
  return (
```

