import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from trl.core.base import Report
from trl.adapters.remote.client import _deserialize_irs


def _create_handler(engine):

    class EngineHandler(BaseHTTPRequestHandler):

        def do_POST(self):

            if self.path != "/process":
                self.send_error(404)
                return

            try:
                content_length = int(
                    self.headers.get("Content-Length", 0)
                )

                body = self.rfile.read(content_length)

                data = json.loads(body)
                
                ctx_irs = _deserialize_irs(
                    data.get("irs", [])
                )

                # Import here to avoid unnecessary coupling at module load time.
                from trl.core.context import RunContext

                ctx = RunContext(
                    irs=ctx_irs,
                    opts=data.get("opts", {}),
                    report=Report.from_dict(data.get("report", {}))
                )
                print(ctx.__dict__)
                engine.process(ctx)

                response = {
                    "irs": [
                        {
                            "kind": ir.kind,
                            "manifest": ir.to_manifest(),
                        }
                        for ir in ctx.irs
                    ],
                    "report": ctx.report.to_dict(),
                }

                encoded = json.dumps(
                    response
                ).encode("utf-8")
             
                self.send_response(200)
                self.send_header(
                    "Content-Type",
                    "application/json",
                )
                self.send_header(
                    "Content-Length",
                    str(len(encoded)),
                )
                self.end_headers()

                self.wfile.write(encoded)

            except Exception as exc:
                import traceback
                traceback.print_exc()

                error = json.dumps(
                    {"error": str(exc)}
                ).encode("utf-8")

                self.send_response(500)
                self.send_header(
                    "Content-Type",
                    "application/json",
                )
                self.send_header(
                    "Content-Length",
                    str(len(error)),
                )
                self.end_headers()

                self.wfile.write(error)

        def log_message(self, format, *args):
            print(
                f"[remote-server] {self.address_string()} - {format % args}"
            )

    return EngineHandler


def serve(
    engine,
    host="127.0.0.1",
    port=9000,
):

    server = HTTPServer(
        (host, port),
        _create_handler(engine),
    )

    print(
        f"Serving {engine.name} "
        f"on http://{host}:{port}/process"
    )

    server.serve_forever()