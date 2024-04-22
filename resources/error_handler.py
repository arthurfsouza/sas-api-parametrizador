class TokenError(Exception):
    code = 500
    error_name = "Token error"


class SIDError(Exception):
    error_name = "Internal SID error"