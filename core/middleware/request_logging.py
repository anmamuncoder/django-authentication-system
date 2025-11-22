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

        api_logger.info(
            json.dumps({
                "method": request.method,
                "path": request.path,
                "user": str(user),
                "headers": dict(request.headers),
                "body": request.body.decode("utf-8", errors="ignore"),
            })
        )

        response = self.get_response(request)

        # ----- After View ----
        api_logger.info(
            json.dumps({
                "response_status": response.status_code,
                "response_data": getattr(response, "data", None),
            })
        )

        return response
