from __future__ import annotations

import base64
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


JENKINS_URL = os.environ['JENKINS_URL'].rstrip('/')
JENKINS_USER = os.environ['JENKINS_USER']
JENKINS_PASSWORD = os.environ['JENKINS_PASSWORD']
JENKINS_JOB_NAME = os.environ['JENKINS_JOB_NAME']


def build_auth_header() -> str:
    token = base64.b64encode(f'{JENKINS_USER}:{JENKINS_PASSWORD}'.encode('utf-8')).decode('ascii')
    return f'Basic {token}'


def fetch_crumb(auth_header: str) -> tuple[str | None, str | None]:
    request = Request(f'{JENKINS_URL}/crumbIssuer/api/json', headers={'Authorization': auth_header})
    try:
        with urlopen(request, timeout=10) as response:
            payload = json.load(response)
    except HTTPError as error:
        if error.code == 404:
            return None, None
        raise
    return payload['crumbRequestField'], payload['crumb']


def trigger_build() -> None:
    auth_header = build_auth_header()
    crumb_field, crumb_value = fetch_crumb(auth_header)
    headers = {'Authorization': auth_header}
    if crumb_field and crumb_value:
        headers[crumb_field] = crumb_value

    request = Request(
        f'{JENKINS_URL}/job/{JENKINS_JOB_NAME}/build',
        data=b'',
        method='POST',
        headers=headers,
    )

    with urlopen(request, timeout=10):
        return


class RelayHandler(BaseHTTPRequestHandler):
    server_version = 'gitea-jenkins-relay/1.0'

    def do_GET(self) -> None:
        if self.path == '/healthz':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'ok')
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self) -> None:
        if self.path != '/gitea/push':
            self.send_response(404)
            self.end_headers()
            return

        content_length = int(self.headers.get('Content-Length', '0'))
        if content_length:
            self.rfile.read(content_length)

        event = self.headers.get('X-Gitea-Event') or self.headers.get('X-Gogs-Event')
        if event and event.lower() != 'push':
            self.send_response(202)
            self.end_headers()
            self.wfile.write(b'ignored')
            return

        try:
            trigger_build()
        except (HTTPError, URLError, KeyError, TimeoutError) as error:
            self.send_response(502)
            self.end_headers()
            self.wfile.write(str(error).encode('utf-8'))
            return

        self.send_response(202)
        self.end_headers()
        self.wfile.write(b'scheduled')

    def log_message(self, format: str, *args: object) -> None:
        print(format % args, flush=True)


if __name__ == '__main__':
    server = ThreadingHTTPServer(('0.0.0.0', 8081), RelayHandler)
    server.serve_forever()