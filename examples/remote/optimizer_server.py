from trl.modules.optimizer.engine import OptimizerEngine
from trl.adapters.remote.server import serve


if __name__ == "__main__":
    serve(
        OptimizerEngine(),
        host="127.0.0.1",
        port=9001,
    )