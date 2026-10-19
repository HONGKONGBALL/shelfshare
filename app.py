#!/usr/bin/env python3
"""ShelfShare local lend-board.

Author: Zhenhua Liu
Listens on http://127.0.0.1:8787 only. No accounts.
A request marks one listing as requested and saves it in data/listings.json.
"""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

HOST = "127.0.0.1"
PORT = 8787
ROOT = Path(__file__).resolve().parent
STATE = ROOT / "data" / "listings.json"
INDEX = ROOT / "static" / "index.html"


def load_listings():
    return json.loads(STATE.read_text(encoding="utf-8"))


def save_listings(items):
    STATE.write_text(
        json.dumps(items, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print("%s - %s" % (self.address_string(), fmt % args))

    def _send(self, code, body, content_type):
        data = body if isinstance(body, bytes) else body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _json(self, code, payload):
        self._send(
            code,
            json.dumps(payload, ensure_ascii=False),
            "application/json; charset=utf-8",
        )

    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/", "/index.html"):
            self._send(200, INDEX.read_bytes(), "text/html; charset=utf-8")
            return
        if path == "/api/listings":
            self._json(200, {"listings": load_listings()})
            return
        self._json(404, {"error": "not found"})

    def do_POST(self):
        path = urlparse(self.path).path
        prefix = "/api/listings/"
        suffix = "/request"
        if not (path.startswith(prefix) and path.endswith(suffix)):
            self._json(404, {"error": "not found"})
            return
        item_id = path[len(prefix) : -len(suffix)]
        length = int(self.headers.get("Content-Length", "0") or "0")
        if length:
            self.rfile.read(length)
        items = load_listings()
        for item in items:
            if item["id"] == item_id:
                if item["status"] != "available":
                    self._json(409, {"error": "already requested", "listing": item})
                    return
                item["status"] = "requested"
                save_listings(items)
                self._json(200, {"listing": item})
                return
        self._json(404, {"error": "listing not found"})


def main():
    if not STATE.is_file():
        raise SystemExit("missing %s" % STATE)
    if not INDEX.is_file():
        raise SystemExit("missing %s" % INDEX)
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print("ShelfShare on http://%s:%s" % (HOST, PORT), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
