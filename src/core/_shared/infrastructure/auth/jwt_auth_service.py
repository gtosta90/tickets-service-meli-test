import os

import jwt

from src.core._shared.infrastructure.auth.auth_interface import AuthService

class JwtAuthService(AuthService):
    def __init__(self, token: str = "") -> None:
        self.public_key = os.getenv('AUTH_PUBLIC_KEY', '')
        self.token = token.replace('Bearer ', '', 1)

    def _decode_token(self) -> dict:
        try:
            public_key = f'-----BEGIN PUBLIC KEY-----\n{self.public_key}\n-----END PUBLIC KEY-----\n'
            # import ipdb; ipdb.set_trace()
            return jwt.decode(self.token, public_key, algorithms=["RS256"], audience="account")
        except jwt.PyJWTError:
            return {}

    def is_authenticated(self) -> bool:
        return bool(self._decode_token())

    def has_role(self, role: str) -> bool:
        decoded_token = self._decode_token()
        return role in decoded_token.get('realm_access', {}).get('roles', [])