from urllib.parse import urlencode


def build_url(base: str, path: str, params: dict) -> str:
    if params:
        return f"{base}{path}?{urlencode(params)}"
    return f"{base}{path}"
