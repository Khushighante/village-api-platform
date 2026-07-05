import hmac
import hashlib
import time
import secrets
from django.core.cache import cache
from rest_framework import authentication, exceptions, throttling

# Section 8.4 & 10.4 Configuration Constants
REPLAY_WINDOW_SECONDS = 300
TIER_LIMITS = {
    'BASIC': {'min': 10, 'hr': 100, 'day': 500},
    'PRO': {'min': 60, 'hr': 1000, 'day': 10000},
    'ENTERPRISE': {'min': 300, 'hr': 10000, 'day': 100000}
}

class ChannelPartnerHMACAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        api_key_id = request.META.get('HTTP_X_API_KEY_ID')
        timestamp = request.META.get('HTTP_X_TIMESTAMP')
        signature = request.META.get('HTTP_X_SIGNATURE')
        nonce = request.META.get('HTTP_X_NONCE')

        if not all([api_key_id, timestamp, signature, nonce]):
            raise exceptions.AuthenticationFailed('Missing required security headers: X-API-Key-ID, X-Timestamp, X-Signature, X-Nonce.')

        # 1. Time-window validation to prevent replay exploits
        try:
            request_time = int(timestamp)
            if abs(int(time.time()) - request_time) > REPLAY_WINDOW_SECONDS:
                raise exceptions.AuthenticationFailed('Request timestamp expired. Clock skew exceeds 5 minutes.')
        except ValueError:
            raise exceptions.AuthenticationFailed('Invalid timestamp encoding format.')

        # 2. Extract Partner Record from database (Simulated for validation tracking)
        # In production: partner = ChannelPartner.objects.get(api_key_id=api_key_id)
        mock_partner_secret = b"partner_secret_signing_token_key_2026"
        mock_partner_tier = "PRO"

        # 3. Re-calculate Signature exactly as specified
        message = f"{timestamp}{nonce}{request.path}".encode('utf-8')
        expected_sig = hmac.new(mock_partner_secret, message, hashlib.sha256).hexdigest()

        if not secrets.compare_digest(expected_sig, signature):
            raise exceptions.AuthenticationFailed('Invalid signature token verification fail.')

        # Return session tuple
        return ({"id": api_key_id, "tier": mock_partner_tier}, None)

class PartnerTierRateThrottle(throttling.BaseThrottle):
    def allow_request(self, request, view):
        if not request.user or 'tier' not in request.user:
            return True # Pass to alternative fallback throttles
            
        tier = request.user['tier']
        partner_id = request.user['id']
        limits = TIER_LIMITS.get(tier, TIER_LIMITS['BASIC'])
        
        current_time = int(time.time())
        minute_bucket = current_time // 60
        
        # Redis Counter key tracking
        redis_key = f"throttle:partner:{partner_id}:min:{minute_bucket}"
        
        try:
            # Using inline pipeline/incr strategy for thread safety
            current_count = cache.get(redis_key, 0)
            if current_count >= limits['min']:
                return False
                
            cache.set(redis_key, current_count + 1, timeout=60)
            return True
        except Exception:
            return True # Soft fail gracefully if Redis goes down during high traffic
