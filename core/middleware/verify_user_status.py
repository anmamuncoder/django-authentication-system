from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse

class VerifyUserStatus:
    def __init__(self,get_response):
        self.get_response = get_response
        
    def __call__(self, request): 
        response = self.get_response(request) 

        # don't require authentication or email verification
        allowed_paths = [ 
            reverse('users:login'),
            reverse('users:login-refresh'),
            reverse('users:register'),
            reverse('verification:request-verify'),
            reverse('verification:conform-verify'),
            reverse('verification:forgot-password-send-otp'),
            reverse('verification:forgot-password-verify-otp'),
            reverse('verification:forgot-password-reset'),
        ]

        # Skip allowed paths
        if request.path in allowed_paths or request.path.startswith('/admin/'):
            return response

        user = getattr(request, 'user', None)
        is_api = request.path.startswith('/auth/')


        # Unauthenticated ---- block API or redirect web
        if not user or not user.is_authenticated:
            if is_api:
                return JsonResponse({"detail": "Authentication credentials were not provided."}, status=401)
            return redirect(f"{reverse('users:login')}?next={request.path}")
    
        # Authenticated but not email-verify -- block response
        if not getattr(user, 'is_email_verify', False):
            if is_api:
                return JsonResponse({"detail": "Email not verified. Please verify your email first."}, status=403)
            return redirect(f"{reverse('verification:request-verify')}?next={request.path}")
 
        return response

 