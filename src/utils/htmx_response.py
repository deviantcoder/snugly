import json
from django.http import HttpResponse


def htmx_http_response(status_code: int, message: dict, event: str):
    """
    Creates an HTTP response with HTMX-specific headers.
    Args:
        status_code (int): The HTTP status code for the response.
        message (dict): A dictionary containing the message to be shown.
        event (str): The HTMX event to trigger.
    Returns:
        HttpResponse: An HTTP response object with the specified status code and HTMX headers.
    """
    
    return HttpResponse(
        status=status_code,
        headers={
            'HX-Trigger': json.dumps({
                event: None,
                'showMessage': message,
            })
        }
    )