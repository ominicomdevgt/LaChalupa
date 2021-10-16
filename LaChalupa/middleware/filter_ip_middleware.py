from django.core.exceptions import PermissionDenied    

class FilterIPMiddleware(object):
    # Check if client IP address is allowed
    def process_request(self, request):
        allowed_ips = ['190.106.221.35', '168.234.49.74', '186.32.88.216 '] # Authorized ip's
        ip = request.META.get('REMOTE_ADDR') # Get client IP address
        if ip not in allowed_ips:
            raise PermissionDenied # If user is not allowed raise Error
        else:
       # If IP address is allowed we don't do anything
            return None