import time
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

# 配置日志
logging.basicConfig(level=logging.INFO)

# 自定义中间件
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 记录请求时间
        start_time = time.time()

        # 记录请求信息
        request_body = await request.body()
        logging.info(f"Request: {request.method} {request.url}")
        logging.info(f"Request Body: {request_body.decode('utf-8') if request_body else None}")
        # 调用下一个处理程序（处理请求）
        response = await call_next(request)

        # 记录响应信息
        process_time = time.time() - start_time
        logging.info(f"Response status: {response.status_code}")
        logging.info(f"Response Headers: {response.headers}")
        response_body = [section async for section in response.body_iterator]
        body =b''.join(response_body).decode('utf-8')
        logging.info(f"Response Body: {body}")
        
        # 重新构造响应，因为 body 只能读取一次
        response = JSONResponse(content=body, status_code=response.status_code)

        logging.info(f"Process time: {process_time:.2f}s")
        
        return response