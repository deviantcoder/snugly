import json
from django.http import HttpResponse


def htmx_http_response(status_code: int, message: dict, event: str):
    return HttpResponse(
        status=status_code,
        headers={
            'HX-Trigger': json.dumps({
                event: None,
                'showMessage': message,
            })
        }
    )