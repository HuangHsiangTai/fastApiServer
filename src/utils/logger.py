import time
import logging
import json
from fastapi import Request
from fastapi.responses import JSONResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware
from .uuid import generate_uuid
from typing import TypedDict,Optional, Dict, Any,List, Mapping

from pythonjsonlogger import jsonlogger


# 自定义 JsonFormatter 来移除不需要的字段（如 taskName）
class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def process_log_record(self, log_record):
        # 移除 'taskName' 字段
        if 'taskName' in log_record:
            del log_record['taskName']
        return log_record

logger = logging.getLogger()
logHandler = logging.StreamHandler()
# 使用 jsonlogger.JsonFormatter 来格式化 JSON 日志
formatter = CustomJsonFormatter(
    fmt ='%(asctime)s %(levelname)s %(message)s',
    json_indent=4  # 控制 JSON 格式的缩进
)     
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

def format_nested_json(data:Mapping[str,Any]|List[Any]):
    if hasattr(data, "__dict__"):  # 如果是类实例，提取属性字典
        data = vars(data)

    if isinstance(data, dict):
        # 如果是字典，递归地处理每一个值
        return {k: format_nested_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        # 如果是列表，递归地处理列表中的每一个元素
        return [format_nested_json(item) for item in data]
    elif isinstance(data, str):
        try:
            # 如果是字符串，尝试将其解析为JSON，并格式化
            parsed_json = json.loads(data)
            return json.dumps(parsed_json, indent=4)
        except (json.JSONDecodeError, TypeError):
            # 如果无法解析为JSON，则保持原样
            return data
    else:
        return data

def log_info(message:Optional[str]=None, extra:Optional[Mapping[str,Any]]= None):
    nested_json=None
    if extra is not None:
        # 遍历和格式化 extra 中的所有嵌套字段
        nested_json = format_nested_json(extra)
    if(message is None):
        logging.info('',extra=nested_json)
    else:
        logging.info(f"{message}", extra=nested_json)
def log_error(message:Optional[str]=None, extra:Optional[Dict[str,Any]]= None):
    if extra:
        # 遍历和格式化 extra 中的所有嵌套字段
        extra = format_nested_json(extra)
    if(message is None):
        logging.error('',extra=extra)
    else:
        logging.error(f"{message}", extra=extra)        
    
# 自定义中间件
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 记录请求时间
        start_time = time.time()
        request_id = generate_uuid()
        # 记录请求信息
        request_body = await request.body()
        request.state.request_id = request_id
        # log_info(f"Request: {request.method} {request.url}",extra={'request_id':request_id} )
        body =json.loads(request_body.decode('utf-8')) if request_body else None
        log_info('Request',extra={'body': body, 'request_id':request_id, 'method':request.method, 'path':request.url.path})
        # 调用下一个处理程序（处理请求）
        response = await call_next(request)

        # 记录响应信息
        process_time = time.time() - start_time
        response_body = [section async for section in response.body_iterator]
        body =b''.join(response_body).decode('utf-8')
        try:
            # 檢查是否為有效的 JSON
            json_body = json.loads(body)
            log_info('Response Json', {'body': json_body, 'request_id': request_id,'status':response.status_code, "process_time":f"{process_time:.2f}"})
            # 因為body只能讀一次,重新建立JSONResponse
            response = JSONResponse(content=json_body, status_code=response.status_code, headers=dict(response.headers))
        except json.JSONDecodeError:
            log_error('Response is not a valid JSON format', {'body': body, 'request_id': request_id})
            # 因為body只能讀一次,重新建立Response
            response = Response(content=body, status_code=response.status_code, headers=dict(response.headers))
        except Exception as e:
            log_error(f"Response json loads failed with error: {e}")   
        return response