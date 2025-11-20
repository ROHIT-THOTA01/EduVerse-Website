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

# Initialize Django application (only once, outside handler)
try:
    django_app = get_wsgi_application()
except Exception as e:
    # Log error if Django fails to initialize
    print(f"Error initializing Django: {e}", file=sys.stderr)
    django_app = None

def handler(request):
    """
    Vercel serverless function handler for Django
    Handles requests and routes them through Django WSGI
    """
    try:
        if django_app is None:
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'text/plain'},
                'body': 'Django application failed to initialize'
            }
        
        from io import BytesIO
        from urllib.parse import urlparse, parse_qs
        
        # Get request data from Vercel request object
        method = getattr(request, 'method', 'GET')
        
        # Get URL path
        url = getattr(request, 'url', '')
        path = getattr(request, 'path', url)
        
        # Parse URL
        if not url:
            url = path
        parsed = urlparse(url if url.startswith('http') else f'https://example.com{url}')
        path_info = parsed.path
        query_string = parsed.query
        
        # Get request body
        body = b''
        try:
            if hasattr(request, 'body'):
                body_bytes = request.body
                if isinstance(body_bytes, bytes):
                    body = body_bytes
                elif body_bytes:
                    body = str(body_bytes).encode('utf-8')
            elif hasattr(request, 'read'):
                body = request.read()
            elif hasattr(request, 'get_body'):
                body = request.get_body()
        except Exception:
            body = b''
        
        # Get headers
        headers = {}
        try:
            if hasattr(request, 'headers'):
                req_headers = request.headers
                if isinstance(req_headers, dict):
                    headers = req_headers
                elif hasattr(req_headers, 'items'):
                    headers = dict(req_headers.items())
                elif hasattr(req_headers, 'get'):
                    headers = {k: req_headers.get(k) for k in dir(req_headers) if not k.startswith('_')}
            elif hasattr(request, 'get'):
                # Try to get headers as dict
                headers = request.get('headers', {})
        except Exception:
            headers = {}
        
        # Normalize headers (handle case-insensitive)
        normalized_headers = {}
        for key, value in headers.items():
            normalized_headers[key.lower()] = value
        
        # Build WSGI environ
        host = normalized_headers.get('host', 'localhost')
        server_name = host.split(':')[0] if ':' in host else host
        
        environ = {
            'REQUEST_METHOD': method,
            'PATH_INFO': path_info or '/',
            'QUERY_STRING': query_string,
            'CONTENT_TYPE': normalized_headers.get('content-type', ''),
            'CONTENT_LENGTH': str(len(body)),
            'SERVER_NAME': server_name,
            'SERVER_PORT': normalized_headers.get('x-forwarded-port', '443'),
            'HTTP_HOST': host,
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': normalized_headers.get('x-forwarded-proto', 'https'),
            'wsgi.input': BytesIO(body),
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprocess': True,
            'wsgi.run_once': False,
            'SCRIPT_NAME': '',
        }
        
        # Add all HTTP headers
        for key, value in normalized_headers.items():
            if key not in ('content-type', 'content-length', 'host'):
                http_key = key.upper().replace('-', '_')
                environ[f'HTTP_{http_key}'] = str(value)
        
        # Handle X-Forwarded headers
        for header_key in ['x-forwarded-for', 'x-forwarded-proto', 'x-forwarded-port']:
            if header_key in normalized_headers:
                http_key = header_key.upper().replace('-', '_')
                environ[f'HTTP_{http_key}'] = str(normalized_headers[header_key])
        
        # Response data
        response_status = [200]
        response_headers_list = []
        
        def start_response(status, response_headers):
            """WSGI start_response callback"""
            response_status[0] = int(status.split()[0])
            response_headers_list[:] = response_headers
        
        # Call Django WSGI application
        try:
            response_body_parts = []
            for part in django_app(environ, start_response):
                if isinstance(part, bytes):
                    response_body_parts.append(part)
                else:
                    response_body_parts.append(str(part).encode('utf-8'))
            
            response_body = b''.join(response_body_parts)
            
            # Convert headers list to dict
            response_headers_dict = {}
            for header_name, header_value in response_headers_list:
                response_headers_dict[header_name] = header_value
            
            # Return Vercel response format
            return {
                'statusCode': response_status[0],
                'headers': response_headers_dict,
                'body': response_body.decode('utf-8', errors='ignore'),
            }
        except Exception as e:
            print(f"Error in Django application: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'text/plain'},
                'body': f'Internal Server Error: {str(e)}'
            }
            
    except Exception as e:
        print(f"Error in handler: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/plain'},
            'body': f'Handler Error: {str(e)}'
        }

