# python-login-app
A login module based on Flask/FastAPI and JWT

## 总览
### 技术选择：

1. `Flask+Gunicorn`: 优雅，轻量，成熟。
2. `JWT`: 跨平台，高效。

### 模块：
- register

```sh
curl -X POST -H "Content-Type: application/json" -d '{"username":"admin","password":"123456"}' http://localhost:5000/register
```

- login
```sh
curl -X POST -H "Content-Type: application/json" -d '{"username":"admin","password":"123456"}' http://localhost:5000/login
```

- other

```sh
curl -H "Authorization: Bearer <access_token>" http://localhost:5000/protected
```


## TODO
1. 使用 `FastAPI` 替换 `Flask` 框架，`uvicorn` 替换 `Gunicorn` , 应对高并发等。
2. 增加 `Cache` 模块
3. `Docker` 封装

## 开发和部署

1. 下载代码
2. 创建虚拟环境
3. 启动环境

