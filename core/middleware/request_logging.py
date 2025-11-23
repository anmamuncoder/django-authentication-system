import logging
import json

api_logger = logging.getLogger("api_logger")
# DEBUG, INFO, WARNING, ERROR, CRITICAL

class APILoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # ---- Before View -----
        user = request.user if request.user.is_authenticated else "Anonymous"

        request_data = {
            "method": request.method,
            "path": request.path,
            "user": str(user),
            "headers": dict(request.headers),
            "body": request.body.decode("utf-8", errors="ignore"),
        }

        api_logger.info(json.dumps(request_data, default=str))

        response = self.get_response(request)

        # ----- After View ----
        response_data = {
            "response_status": response.status_code,
            "response_data": getattr(response, "data", None),
        }

        api_logger.info(json.dumps(response_data, default=str))

        return response
