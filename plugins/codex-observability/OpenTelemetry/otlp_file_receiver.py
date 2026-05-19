#!/usr/bin/env python3
import http.server
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
LOG_FILE = ROOT / "otel-logs.jsonl"
TRACE_FILE = ROOT / "otel-traces.jsonl"


class Handler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length)
        content_type = self.headers.get("Content-Type", "")
        now = datetime.now(timezone.utc).isoformat()
        record = {
            "timestamp": now,
            "path": self.path,
            "bytes": length,
            "content_type": content_type,
        }

        if "json" in content_type.lower():
            try:
                body_text = body.decode("utf-8")
                record["body_text"] = body_text
                try:
                    record["body_json"] = json.loads(body_text)
                except json.JSONDecodeError:
                    record["json_decode_error"] = "invalid_json"
            except UnicodeDecodeError:
                record["decode_error"] = "invalid_utf8"
                record["body_hex_prefix"] = body[:64].hex()
        else:
            record["body_hex_prefix"] = body[:64].hex()

        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

        if self.path == "/v1/traces":
            with TRACE_FILE.open("a", encoding="utf-8") as f:
                f.write(json.dumps(record) + "\n")

        print(f"{now} {self.path} bytes={length}", flush=True)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")

    def log_message(self, _format, *_args):
        return


if __name__ == "__main__":
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 4318), Handler)
    print("otlp_receiver_listening 127.0.0.1:4318", flush=True)
    server.serve_forever()
