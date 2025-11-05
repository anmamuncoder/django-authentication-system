import os
from django.http import HttpResponse

def serve_openapi_yaml(request):
    yaml_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs", "openapi.yml")
    with open(yaml_file, "r", encoding="utf-8") as f:
        content = f.read()
    return HttpResponse(content, content_type="application/x-yaml")
