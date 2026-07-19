#!/usr/bin/env python3
"""comments-page hub server. Stdlib-only, Tailscale-only, no external deps.

Multi-doc: each reviewable doc lives under docs/<slug>/ (DOC.md, annotations.json,
meta.json). The server auto-discovers docs from that directory — adding a new doc
means adding a subdirectory, never touching this file. "/" is the hub landing page
listing every doc; each doc is reviewable at "/d/<slug>".

Bespoke doc type: if docs/<slug>/custom.html exists, it's served verbatim at
"/d/<slug>" instead of the markdown DOC.md pipeline — for tabbed data views,
live dashboards, or anything that isn't a commentable prose doc. No
annotations/comment API for these; they're self-contained static pages.

Fill in BIND_HOST/PORT below, then run: nohup python3 server.py > server.log 2>&1 & disown
"""
import json
import os
import re
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# ---- CONFIG: fill these in per instance ----
BIND_HOST = "0.0.0.0"      # set to `tailscale ip -4` output — never 0.0.0.0/127.0.0.1
PORT = 0                   # pick an unused port (check `ss -tlnp` first)
# ---------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
INDEX_PATH = os.path.join(BASE_DIR, "index.html")
HUB_PATH = os.path.join(BASE_DIR, "hub.html")

SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def list_docs():
    docs = {}
    if not os.path.isdir(DOCS_DIR):
        return docs
    for slug in sorted(os.listdir(DOCS_DIR)):
        d = os.path.join(DOCS_DIR, slug)
        meta_path = os.path.join(d, "meta.json")
        if not SLUG_RE.match(slug) or not os.path.isfile(meta_path):
            continue
        with open(meta_path) as f:
            meta = json.load(f)
        docs[slug] = {"title": meta.get("title", slug), "dir": d}
    return docs


def doc_paths(slug):
    d = os.path.join(DOCS_DIR, slug)
    return os.path.join(d, "DOC.md"), os.path.join(d, "annotations.json")


def read_annotations(slug):
    _, ann_path = doc_paths(slug)
    if not os.path.exists(ann_path):
        return []
    with open(ann_path, "r") as f:
        return json.load(f)


def write_annotations(slug, items):
    _, ann_path = doc_paths(slug)
    tmp_path = ann_path + ".tmp"
    with open(tmp_path, "w") as f:
        json.dump(items, f, indent=2)
    os.replace(tmp_path, ann_path)


class Handler(BaseHTTPRequestHandler):
    def _send_json(self, obj, status=200):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path, content_type):
        with open(path, "rb") as f:
            body = f.read()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_text(self, text):
        body = text.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b"{}"
        return json.loads(raw)

    def do_GET(self):
        path = self.path.split("?")[0]
        docs = list_docs()

        if path == "/":
            self._send_file(HUB_PATH, "text/html; charset=utf-8")
            return

        if path == "/api/docs":
            self._send_json([{"slug": s, "title": v["title"]} for s, v in docs.items()])
            return

        if path.startswith("/d/"):
            slug = path[len("/d/"):].rstrip("/")
            if slug not in docs:
                self.send_response(404); self.end_headers(); return
            custom_path = os.path.join(docs[slug]["dir"], "custom.html")
            if os.path.isfile(custom_path):
                self._send_file(custom_path, "text/html; charset=utf-8")
            else:
                self._send_file(INDEX_PATH, "text/html; charset=utf-8")
            return

        m = re.match(r"^/api/([a-z0-9-]+)/(doc|annotations|title)$", path)
        if m:
            slug, kind = m.group(1), m.group(2)
            if slug not in docs:
                self.send_response(404); self.end_headers(); return
            if kind == "doc":
                doc_path, _ = doc_paths(slug)
                with open(doc_path, "r") as f:
                    self._send_text(f.read())
            elif kind == "annotations":
                self._send_json(read_annotations(slug))
            elif kind == "title":
                self._send_json({"title": docs[slug]["title"]})
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        path = self.path.split("?")[0]
        try:
            payload = self._read_json_body()
        except json.JSONDecodeError:
            self._send_json({"error": "bad json"}, 400)
            return

        docs = list_docs()

        m = re.match(r"^/api/([a-z0-9-]+)/annotations$", path)
        if m:
            slug = m.group(1)
            if slug not in docs:
                self._send_json({"error": "unknown doc"}, 404)
                return
            text = (payload.get("text") or "").strip()
            if not text:
                self._send_json({"error": "empty text"}, 400)
                return
            items = read_annotations(slug)
            item = {
                "id": (items[-1]["id"] + 1) if items else 1,
                "type": payload.get("type") or "general",
                "start": payload.get("start"),
                "end": payload.get("end"),
                "quote": payload.get("quote"),
                "text": text,
                "author": payload.get("author") or "valen",
                "ts": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
                "status": "open",
                "reply": None,
            }
            items.append(item)
            write_annotations(slug, items)
            self._send_json(item, 201)
            return

        if path == "/api/annotations/reply":
            slug = payload.get("doc")
            if slug not in docs:
                self._send_json({"error": "unknown doc"}, 404)
                return
            aid = payload.get("id")
            items = read_annotations(slug)
            found = None
            for it in items:
                if it["id"] == aid:
                    it["reply"] = payload.get("reply")
                    it["status"] = payload.get("status") or it["status"]
                    it["replied_ts"] = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
                    found = it
                    break
            if not found:
                self._send_json({"error": "annotation not found"}, 404)
                return
            write_annotations(slug, items)
            self._send_json(found, 200)
            return

        self.send_response(404)
        self.end_headers()

    def log_message(self, fmt, *args):
        pass  # quiet; short-lived personal review tool


if __name__ == "__main__":
    if PORT == 0 or BIND_HOST in ("0.0.0.0", "127.0.0.1"):
        raise SystemExit("Fill in BIND_HOST (tailscale IP) and PORT before running.")
    server = ThreadingHTTPServer((BIND_HOST, PORT), Handler)
    print(f"comments-page hub listening on http://{BIND_HOST}:{PORT}")
    server.serve_forever()
