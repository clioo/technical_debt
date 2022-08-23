import asyncio
import json
import timeit
from functools import wraps

from fastapi.responses import Response

from utils.logs import save_logs
from utils.warnings import WARNINGS, clear_warnings


def warnings_decorator(func):
    """Add this decorator to an endpoint to return warnings in the response."""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        res = await func(*args, **kwargs)
        if isinstance(res, Response):
            res_body = json.loads(res.body)
        elif isinstance(res, dict):
            res_body = res
        res_body["warnings"] = WARNINGS.copy()
        clear_warnings()
        if isinstance(res, Response):
            res = Response(
                json.dumps(res_body),
                media_type=res.media_type,
                status_code=res.status_code,
            )
        elif isinstance(res, dict):
            res = res_body
        return res

    return wrapper


def logcemex(database: str, prefix: str = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user_agent = None
            ip = None
            output = None
            input_ = None
            start = timeit.default_timer()
            res = await func(*args, **kwargs)
            if isinstance(res, Response):
                res_body = json.loads(res.body)
            elif isinstance(res, dict):
                res_body = res
            stop = timeit.default_timer()
            execution_time = stop - start
            request = kwargs.get("request")
            if request:
                user_agent = request.headers.get("user-agent")
                ip = request.client.host
                output = res_body
                try:
                    input_ = await request.json()
                except json.decoder.JSONDecodeError:
                    input_ = None
            asyncio.create_task(
                save_logs(
                    prefix=prefix,
                    database=database,
                    execution_time=execution_time,
                    user_agent=user_agent,
                    ip=ip,
                    input=input_,
                    output=output,
                )
            )
            return res

        return wrapper

    return decorator
