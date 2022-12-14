import socket, time, json, logging
from datetime import datetime

request_logger = logging.getLogger("api")



class RequestLogMiddleware:
    """Request Logging Middleware."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        now = datetime.now()
        log_data = {
            "remote_address": request.META["REMOTE_ADDR"],
            "server_hostname": socket.gethostname(),
            "request_method": request.method,
            "request_path": request.get_full_path(),
            'client_id': request.headers.get('CLIENT-ID'),
        }
        
        if "/api/" in str(request.get_full_path()):
            req_body = json.loads(request.body.decode("utf-8")) if request.body else {}
            if request.get_full_path() == '/api/v1/user/login':
                req_body['password'] = "xxxxxxx"
            log_data["request_body"] = req_body
            
        response = self.get_response(request)
        if response and response["content-type"] == "application/json":
            response_body = json.loads(response.content.decode("utf-8"))
            log_data["response_body"] = response_body
        log_data["run_time"] = time.time() - start_time
        log_data["x_time"] = now.strftime("%Y-%m-%d %H:%M:%S")
        request_logger.info(log_data)
        
        return response



    # Log unhandled exceptions as well
    def process_exception(self, request, exception):
        try:
            raise exception
        except Exception as e:
            request_logger.exception("Unhandled Exception: " + str(e))
        return exception