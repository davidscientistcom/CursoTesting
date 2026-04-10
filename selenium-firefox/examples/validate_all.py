from __future__ import annotations

import importlib
import os
import sys
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


COURSE_ROOT = Path(__file__).resolve().parents[1]
PORT = 8765
MODULES = [
    "module1_intro",
    "module2_webdriver",
    "module3_interactions",
    "module4_waits",
]


class ReusableHTTPServer(ThreadingHTTPServer):
    allow_reuse_address = True


def start_server() -> tuple[ReusableHTTPServer, threading.Thread]:
    handler = partial(SimpleHTTPRequestHandler, directory=str(COURSE_ROOT))
    server = ReusableHTTPServer(("127.0.0.1", PORT), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


def main() -> int:
    os.environ.setdefault("HEADLESS", "1")
    os.environ["SELENIUM_LAB_URL"] = f"http://127.0.0.1:{PORT}/lab"

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    server, _ = start_server()
    failures: list[str] = []

    try:
        for module_name in MODULES:
            module = importlib.import_module(module_name)
            for example_name, example_func in module.EXAMPLES.items():
                try:
                    result = example_func()
                    print(f"PASS {example_name}: {result}")
                except Exception as exc:
                    failures.append(f"FAIL {example_name}: {exc}")
                    print(failures[-1])
    finally:
        server.shutdown()
        server.server_close()

    if failures:
        print("\nSe detectaron fallos:\n" + "\n".join(failures))
        return 1

    print("\nTodos los ejemplos han pasado contra la web de prácticas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())