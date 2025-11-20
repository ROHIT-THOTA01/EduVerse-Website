"""
Vercel serverless function handler for Django application
"""
import os
import sys
from pathlib import Path

# Add project root to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Coursera.settings')

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application

# Initialize Django application (only once)
django_app = get_wsgi_application()

def handler(request):
    """
    Vercel serverless function handler for Django
    Handles requests and routes them through Django WSGI
    """
    from io import BytesIO
    from urllib.parse import urlparse
    
    # Parse request URL
    url = request.url if hasattr(request, 'url') else request.path
    parsed = urlparse(url)
    path_info = parsed.path
    query_string = parsed.query
    
    # Get request body
    body = b''
    if hasattr(request, 'body'):
        body = request.body if isinstance(request.body, bytes) else str(request.body).encode()
    elif hasattr(request, 'read'):
        body = request.read()
    
    # Get headers
    headers = {}
    if hasattr(request, 'headers'):
        headers = request.headers
    elif hasattr(request, 'get'):
        headers = {k: request.get(k) for k in request.keys()}
    
    # Build WSGI environ
    environ = {
        'REQUEST_METHOD': (request.method if hasattr(request, 'method') else 'GET'),
        'PATH_INFO': path_info,
        'QUERY_STRING': query_string,
        'CONTENT_TYPE': headers.get('content-type', headers.get('Content-Type', '')),
        'CONTENT_LENGTH': str(len(body)),
        'SERVER_NAME': headers.get('host', 'localhost').split(':')[0],
        'SERVER_PORT': headers.get('x-forwarded-port', '443'),
        'HTTP_HOST': headers.get('host', 'localhost'),
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': headers.get('x-forwarded-proto', 'https'),
        'wsgi.input': BytesIO(body),
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': False,
        'wsgi.multiprocess': True,
        'wsgi.run_once': False,
    }
    
    # Add all HTTP headers
    for key, value in headers.items():
        key_upper = key.upper().replace('-', '_')
        if key_upper not in ('CONTENT_TYPE', 'CONTENT_LENGTH', 'HOST'):
            environ[f'HTTP_{key_upper}'] = value
    
    # Handle X-Forwarded headers
    for header in ['x-forwarded-for', 'x-forwarded-proto', 'x-forwarded-port']:
        if header in headers:
            environ[f'HTTP_{header.replace("-", "_").upper()}'] = headers[header]
    
    # Response data
    response_status = 200
    response_headers_dict = {}
    
    def start_response(status, response_headers):
        """WSGI start_response callback"""
        nonlocal response_status, response_headers_dict
        response_status = int(status.split()[0])
        response_headers_dict = dict(response_headers)
    
    # Call Django WSGI application
    response_body_parts = []
    for part in django_app(environ, start_response):
        if isinstance(part, bytes):
            response_body_parts.append(part)
        else:
            response_body_parts.append(str(part).encode('utf-8'))
    
    response_body = b''.join(response_body_parts)
    
    # Return Vercel response format
    return {
        'statusCode': response_status,
        'headers': response_headers_dict,
        'body': response_body.decode('utf-8', errors='ignore'),
    }

