"""
QUANTUM REDIRECT SYSTEM
Super advanced 4-stage cryptographic verification and tracking system
Designed for maximum security, data fidelity, and speed (<3 seconds total)
"""

import jwt
import time
import hashlib
import secrets
import redis
import json
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
from urllib.parse import urlencode, urlparse, parse_qs
import requests
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import os

class QuantumRedirectSystem:
    def __init__(self):
        # Multi-layer cryptographic keys
        self.SECRET_KEY_1 = os.environ.get('QUANTUM_SECRET_1', 'quantum_genesis_key_2025_ultra_secure')
        self.SECRET_KEY_2 = os.environ.get('QUANTUM_SECRET_2', 'quantum_transit_key_2025_ultra_secure')
        self.SECRET_KEY_3 = os.environ.get('QUANTUM_SECRET_3', 'quantum_routing_key_2025_ultra_secure')
        
        # Redis for high-speed nonce verification
        try:
            self.redis_client = redis.Redis(
                host=os.environ.get('REDIS_HOST', 'localhost'),
                port=int(os.environ.get('REDIS_PORT', 6379)),
                db=0,
                decode_responses=True
            )
            # Test connection
            self.redis_client.ping()
        except:
            # Fallback to in-memory cache for development
            self.redis_client = None
            self._memory_cache = {}
        
        # Advanced configuration
        self.GENESIS_TOKEN_EXPIRY = 15  # seconds
        self.TRANSIT_TOKEN_EXPIRY = 10  # seconds
        self.ROUTING_TOKEN_EXPIRY = 5   # seconds
        self.NONCE_CACHE_TTL = 60       # seconds
        
        # Performance tracking
        self.performance_metrics = {
            'total_redirects': 0,
            'successful_redirects': 0,
            'blocked_attempts': 0,
            'average_processing_time': 0,
            'security_violations': {
                'invalid_signature': 0,
                'expired_token': 0,
                'ip_mismatch': 0,
                'ua_mismatch': 0,
                'replay_attack': 0,
                'invalid_audience': 0
            }
        }

    def _hash_value(self, value: str) -> str:
        """Create SHA-256 hash of a value for security"""
        return hashlib.sha256(value.encode()).hexdigest()

    def _generate_nonce(self) -> str:
        """Generate cryptographically secure nonce"""
        return secrets.token_urlsafe(32)

    def _store_nonce(self, nonce: str) -> None:
        """Store nonce in cache to prevent replay attacks"""
        if self.redis_client:
            self.redis_client.setex(f"nonce:{nonce}", self.NONCE_CACHE_TTL, "used")
        else:
            # Fallback to memory cache
            current_time = time.time()
            self._memory_cache[nonce] = current_time
            # Clean old entries
            self._memory_cache = {
                k: v for k, v in self._memory_cache.items() 
                if current_time - v < self.NONCE_CACHE_TTL
            }

    def _check_nonce(self, nonce: str) -> bool:
        """Check if nonce has been used before (replay attack detection)"""
        if self.redis_client:
            return self.redis_client.exists(f"nonce:{nonce}")
        else:
            current_time = time.time()
            return nonce in self._memory_cache and (current_time - self._memory_cache[nonce]) < self.NONCE_CACHE_TTL

    def _create_advanced_jwt(self, payload: Dict, secret_key: str, expiry_seconds: int) -> str:
        """Create advanced JWT with comprehensive security claims"""
        now = datetime.utcnow()
        
        jwt_payload = {
            **payload,
            'iat': now,  # Issued at
            'exp': now + timedelta(seconds=expiry_seconds),  # Expiration
            'nbf': now,  # Not before
            'jti': self._generate_nonce(),  # JWT ID for uniqueness
        }
        
        return jwt.encode(
            jwt_payload, 
            secret_key, 
            algorithm='HS256',
            headers={'typ': 'JWT', 'alg': 'HS256'}
        )

    def _verify_advanced_jwt(self, token: str, secret_key: str, expected_audience: str) -> Tuple[bool, Optional[Dict], str]:
        """Verify JWT with comprehensive security checks"""
        try:
            # Decode and verify signature
            payload = jwt.decode(
                token, 
                secret_key, 
                algorithms=['HS256'],
                options={'verify_exp': True, 'verify_nbf': True}
            )
            
            # Verify audience
            if payload.get('aud') != expected_audience:
                return False, None, "invalid_audience"
            
            # Check for replay attack
            jti = payload.get('jti')
            if jti and self._check_nonce(jti):
                return False, None, "replay_attack"
            
            # Store nonce to prevent future replay
            if jti:
                self._store_nonce(jti)
            
            return True, payload, "valid"
            
        except jwt.ExpiredSignatureError:
            return False, None, "expired_token"
        except jwt.InvalidTokenError:
            return False, None, "invalid_signature"
        except Exception as e:
            return False, None, f"verification_error: {str(e)}"

    def stage1_genesis_link(self, link_id: str, user_ip: str, user_agent: str, referrer: str = '', original_params: Dict = None) -> Dict:
        """
        Stage 1: Genesis Link Processing
        Creates cryptographically signed JWT and redirects to validation hub
        Target execution time: <100ms
        """
        start_time = time.time()
        
        try:
            # Generate unique click ID
            click_id = f"{link_id}_{int(time.time() * 1000)}_{secrets.token_hex(8)}"
            nonce = self._generate_nonce()
            
            # Ensure original_params is not None
            if original_params is None:
                original_params = {}
            
            # Create genesis token payload
            genesis_payload = {
                'iss': 'genesis-link-generator',
                'sub': click_id,
                'aud': 'validation-hub',
                'nonce': nonce,
                'ip_hash': self._hash_value(user_ip),
                'ua_hash': self._hash_value(user_agent),
                'link_id': link_id,
                'referrer': referrer,
                'stage': 'genesis',
                'original_params': original_params  # CRITICAL: Store original parameters
            }
            
            # Create signed JWT
            genesis_token = self._create_advanced_jwt(
                genesis_payload, 
                self.SECRET_KEY_1, 
                self.GENESIS_TOKEN_EXPIRY
            )
            
            # Log the genesis event
            genesis_log = {
                'click_id': click_id,
                'link_id': link_id,
                'user_ip': user_ip,
                'user_agent': user_agent,
                'referrer': referrer,
                'timestamp': datetime.utcnow().isoformat(),
                'stage': 'genesis',
                'processing_time_ms': (time.time() - start_time) * 1000
            }
            
            # Update performance metrics
            self.performance_metrics['total_redirects'] += 1
            
            # Generate validation hub URL
            validation_url = f"http://127.0.0.1:5000/validate-quantum?token={genesis_token}"
            
            return {
                'success': True,
                'redirect_url': validation_url,
                'click_id': click_id,
                'processing_time_ms': (time.time() - start_time) * 1000,
                'stage': 'genesis_complete',
                'log_data': genesis_log
            }
            
        except Exception as e:
            self.performance_metrics['blocked_attempts'] += 1
            return {
                'success': False,
                'error': f"Genesis stage failed: {str(e)}",
                'processing_time_ms': (time.time() - start_time) * 1000,
                'stage': 'genesis_failed'
            }

    def stage2_validation_hub(self, genesis_token: str, current_ip: str, current_user_agent: str) -> Dict:
        """
        Stage 2: Validation Hub Processing
        Ruthless validation of traffic with cryptographic verification
        Target execution time: <150ms
        """
        start_time = time.time()
        
        try:
            # Verify genesis token
            is_valid, payload, error_reason = self._verify_advanced_jwt(
                genesis_token, 
                self.SECRET_KEY_1, 
                'validation-hub'
            )
            
            if not is_valid:
                self.performance_metrics['security_violations'][error_reason] += 1
                self.performance_metrics['blocked_attempts'] += 1
                return {
                    'success': False,
                    'error': f"Token validation failed: {error_reason}",
                    'processing_time_ms': (time.time() - start_time) * 1000,
                    'stage': 'validation_failed',
                    'security_violation': error_reason
                }
            
            # Contextual verification - IP and User-Agent matching
            current_ip_hash = self._hash_value(current_ip)
            current_ua_hash = self._hash_value(current_user_agent)
            
            if payload['ip_hash'] != current_ip_hash:
                self.performance_metrics['security_violations']['ip_mismatch'] += 1
                self.performance_metrics['blocked_attempts'] += 1
                return {
                    'success': False,
                    'error': "IP address mismatch - potential token interception",
                    'processing_time_ms': (time.time() - start_time) * 1000,
                    'stage': 'validation_failed',
                    'security_violation': 'ip_mismatch'
                }
            
            if payload['ua_hash'] != current_ua_hash:
                self.performance_metrics['security_violations']['ua_mismatch'] += 1
                self.performance_metrics['blocked_attempts'] += 1
                return {
                    'success': False,
                    'error': "User-Agent mismatch - potential bot activity",
                    'processing_time_ms': (time.time() - start_time) * 1000,
                    'stage': 'validation_failed',
                    'security_violation': 'ua_mismatch'
                }
            
            # Generate transit token for routing gateway
            transit_payload = {
                'iss': 'validation-hub',
                'sub': payload['sub'],  # Original click ID
                'aud': 'routing-gateway',
                'link_id': payload['link_id'],
                'validated_at': datetime.utcnow().isoformat(),
                'stage': 'transit',
                'security_score': 100  # Passed all validations
            }
            
            transit_token = self._create_advanced_jwt(
                transit_payload,
                self.SECRET_KEY_2,
                self.TRANSIT_TOKEN_EXPIRY
            )
            
            # Log validation success
            validation_log = {
                'click_id': payload['sub'],
                'link_id': payload['link_id'],
                'validation_result': 'passed',
                'security_checks': {
                    'token_signature': 'valid',
                    'token_expiry': 'valid',
                    'ip_verification': 'passed',
                    'ua_verification': 'passed',
                    'nonce_check': 'passed'
                },
                'timestamp': datetime.utcnow().isoformat(),
                'stage': 'validation_complete',
                'processing_time_ms': (time.time() - start_time) * 1000
            }
            
            # Generate routing gateway URL
            routing_url = f"http://127.0.0.1:5000/route-quantum?transit_token={transit_token}"
            
            return {
                'success': True,
                'redirect_url': routing_url,
                'click_id': payload['sub'],
                'processing_time_ms': (time.time() - start_time) * 1000,
                'stage': 'validation_complete',
                'log_data': validation_log
            }
            
        except Exception as e:
            self.performance_metrics['blocked_attempts'] += 1
            return {
                'success': False,
                'error': f"Validation stage failed: {str(e)}",
                'processing_time_ms': (time.time() - start_time) * 1000,
                'stage': 'validation_failed'
            }

    def stage3_routing_gateway(self, transit_token: str, tracking_params: Dict = None) -> Dict:
        """
        Stage 3: Routing Gateway Processing
        Final decision making and commercial tracking parameter injection
        Target execution time: <100ms
        """
        start_time = time.time()
        
        try:
            # Verify transit token
            is_valid, payload, error_reason = self._verify_advanced_jwt(
                transit_token,
                self.SECRET_KEY_2,
                'routing-gateway'
            )
            
            if not is_valid:
                self.performance_metrics['security_violations'][error_reason] += 1
                self.performance_metrics['blocked_attempts'] += 1
                return {
                    'success': False,
                    'error': f"Transit token validation failed: {error_reason}",
                    'processing_time_ms': (time.time() - start_time) * 1000,
                    'stage': 'routing_failed',
                    'security_violation': error_reason
                }
            
            # Get link configuration (this would come from database in real implementation)
            link_config = self._get_link_configuration(payload['link_id'])
            
            if not link_config:
                return {
                    'success': False,
                    'error': "Link configuration not found",
                    'processing_time_ms': (time.time() - start_time) * 1000,
                    'stage': 'routing_failed'
                }
            
            # Get original parameters from JWT payload
            original_params = payload.get('original_params', {})
            
            # Merge original parameters with tracking parameters
            all_params = {**(tracking_params or {}), **original_params}
            
            # Build final URL with ALL parameters (original + tracking)
            final_url = self._build_final_url(
                link_config['destination_url'],
                payload['sub'],  # click_id
                all_params  # Include original parameters
            )
            
            # Log successful routing
            routing_log = {
                'click_id': payload['sub'],
                'link_id': payload['link_id'],
                'final_destination': final_url,
                'security_score': payload.get('security_score', 100),
                'timestamp': datetime.utcnow().isoformat(),
                'stage': 'routing_complete',
                'processing_time_ms': (time.time() - start_time) * 1000
            }
            
            # Update success metrics
            self.performance_metrics['successful_redirects'] += 1
            
            return {
                'success': True,
                'final_url': final_url,
                'click_id': payload['sub'],
                'processing_time_ms': (time.time() - start_time) * 1000,
                'stage': 'routing_complete',
                'log_data': routing_log
            }
            
        except Exception as e:
            self.performance_metrics['blocked_attempts'] += 1
            return {
                'success': False,
                'error': f"Routing stage failed: {str(e)}",
                'processing_time_ms': (time.time() - start_time) * 1000,
                'stage': 'routing_failed'
            }

    def _get_link_configuration(self, link_id: str) -> Optional[Dict]:
        """Get link configuration from database"""
        # This would be a database lookup in real implementation
        # For now, return a mock configuration
        return {
            'destination_url': 'https://advertiser.com/product-page',
            'tracking_enabled': True,
            'campaign_id': 'camp_123',
            'utm_source': 'quantum_redirect',
            'utm_medium': 'link',
            'utm_campaign': 'advanced_tracking'
        }

    def _build_final_url(self, base_url: str, click_id: str, additional_params: Dict) -> str:
        """Build final URL with all tracking parameters - PRESERVING ORIGINAL PARAMETERS"""
        # Parse existing URL
        parsed = urlparse(base_url)
        existing_params = parse_qs(parsed.query)
        
        # Add quantum tracking parameters (only if not overridden by original params)
        quantum_params = {
            'quantum_click_id': click_id,
            'quantum_timestamp': str(int(time.time())),
            'quantum_verified': 'true'
        }
        
        # Start with quantum parameters as base
        all_params = quantum_params.copy()
        
        # Add existing URL parameters (from destination URL)
        for key, values in existing_params.items():
            if values:
                all_params[key] = values[0]
        
        # CRITICAL: Original parameters take HIGHEST PRIORITY
        # This ensures user_id, email, campaign_id, pixel_id are preserved
        if additional_params:
            all_params.update(additional_params)
        
        # Build final URL
        query_string = urlencode(all_params)
        final_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        if query_string:
            final_url += f"?{query_string}"
        
        return final_url

    def get_performance_metrics(self) -> Dict:
        """Get comprehensive performance and security metrics"""
        total_attempts = self.performance_metrics['total_redirects']
        if total_attempts > 0:
            success_rate = (self.performance_metrics['successful_redirects'] / total_attempts) * 100
            block_rate = (self.performance_metrics['blocked_attempts'] / total_attempts) * 100
        else:
            success_rate = 0
            block_rate = 0
        
        return {
            **self.performance_metrics,
            'success_rate_percentage': round(success_rate, 2),
            'block_rate_percentage': round(block_rate, 2),
            'security_effectiveness': round(block_rate, 2),  # Higher block rate = better security
            'system_health': 'excellent' if success_rate > 95 else 'good' if success_rate > 85 else 'needs_attention'
        }

    def analyze_security_threats(self) -> Dict:
        """Analyze security threat patterns"""
        violations = self.performance_metrics['security_violations']
        total_violations = sum(violations.values())
        
        if total_violations == 0:
            return {
                'threat_level': 'minimal',
                'primary_threats': [],
                'recommendations': ['System is secure - continue monitoring']
            }
        
        # Calculate threat percentages
        threat_analysis = {}
        for threat_type, count in violations.items():
            if count > 0:
                percentage = (count / total_violations) * 100
                threat_analysis[threat_type] = {
                    'count': count,
                    'percentage': round(percentage, 2)
                }
        
        # Determine primary threats
        primary_threats = sorted(
            threat_analysis.items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )[:3]
        
        # Generate recommendations
        recommendations = []
        for threat_type, data in primary_threats:
            if threat_type == 'replay_attack':
                recommendations.append("Implement stricter nonce validation and reduce token expiry times")
            elif threat_type == 'ip_mismatch':
                recommendations.append("Investigate potential token interception or proxy usage")
            elif threat_type == 'ua_mismatch':
                recommendations.append("Enhanced bot detection - possible automated traffic")
            elif threat_type == 'expired_token':
                recommendations.append("Users may be using cached/bookmarked links - consider education")
        
        # Determine overall threat level
        if total_violations > 100:
            threat_level = 'high'
        elif total_violations > 50:
            threat_level = 'medium'
        else:
            threat_level = 'low'
        
        return {
            'threat_level': threat_level,
            'total_violations': total_violations,
            'threat_breakdown': threat_analysis,
            'primary_threats': [{'type': t[0], **t[1]} for t in primary_threats],
            'recommendations': recommendations
        }

# Global quantum redirect system instance
quantum_redirect = QuantumRedirectSystem()
