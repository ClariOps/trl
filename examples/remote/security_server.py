from trl.modules.security.engine import SecurityEngine
from trl.adapters.remote.server import serve


if __name__ == "__main__":
    serve(
        SecurityEngine(),
        host="127.0.0.1",
        port=9003,
    )