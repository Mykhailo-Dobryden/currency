from time import time
from .models import RequestResponseLog


class RequestResponseTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time()
        response = self.get_response(request)
        end = time()
        response_time = end - start
        method = request.method
        path = request.path
        RequestResponseLog.objects.create(
            path=path,
            request_method=method,
            time=response_time
        )

        return response
