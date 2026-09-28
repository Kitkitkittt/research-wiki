from __future__ import annotations

import http.server
import socket
import threading
import time
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError

from scripts import validate_public


class PublicAliasProbeTests(unittest.TestCase):
    def test_trickling_response_body_is_interrupted_at_budget(self) -> None:
        class TricklingHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self) -> None:
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.send_header("Content-Length", "100000")
                self.end_headers()
                try:
                    for _ in range(100):
                        self.wfile.write(b"x")
                        self.wfile.flush()
                        time.sleep(0.03)
                except (BrokenPipeError, ConnectionResetError):
                    pass

            def log_message(self, *_args: object) -> None:
                pass

        server = http.server.HTTPServer(("127.0.0.1", 0), TricklingHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        errors: list[str] = []
        started = time.monotonic()
        try:
            with patch.object(validate_public, "ALIAS_PROBE_BUDGET_SECONDS", 0.25):
                validate_public.validate_public_alias(f"http://127.0.0.1:{server.server_port}/", errors)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=1)

        self.assertLess(time.monotonic() - started, 1.5)
        self.assertEqual(len(errors), 1)
        self.assertIn("public alias route failed:", errors[0])
        self.assertIn("budget exhausted", errors[0])

    def test_deadline_is_not_swallowed_by_socket_address_fallback(self) -> None:
        attempted: list[object] = []
        sockets: list[socket.socket] = []

        def delayed_connect(connection: socket.socket, address: object) -> None:
            sockets.append(connection)
            attempted.append(address)
            time.sleep(0.4)
            raise OSError("unreachable address")

        addresses = [
            (socket.AF_INET, socket.SOCK_STREAM, 0, "", ("127.0.0.1", 80)),
            (socket.AF_INET, socket.SOCK_STREAM, 0, "", ("127.0.0.2", 80)),
        ]
        start = time.monotonic()
        try:
            with (
                patch.object(validate_public, "ALIAS_PROBE_BUDGET_SECONDS", 0.1),
                patch.object(socket, "getaddrinfo", return_value=addresses),
                patch.object(socket.socket, "connect", delayed_connect),
            ):
                errors: list[str] = []
                validate_public.validate_public_alias("http://alias.example/", errors)
        finally:
            for connection in sockets:
                connection.close()

        self.assertLess(time.monotonic() - start, 0.3)
        self.assertEqual(len(attempted), 1)
        self.assertEqual(len(errors), 1)
        self.assertIn("budget exhausted", errors[0])

    def test_deadline_reports_last_failure_without_starting_another_request(self) -> None:
        clock = [0.0]
        requests: list[float] = []

        def failed_request(request: object, timeout: float) -> None:
            requests.append(timeout)
            clock[0] += timeout
            raise URLError("alias gateway unavailable")

        def sleep(delay: float) -> None:
            clock[0] += delay

        errors: list[str] = []
        with (
            patch.object(validate_public, "ALIAS_PROBE_BUDGET_SECONDS", 10),
            patch.object(validate_public.time, "monotonic", side_effect=lambda: clock[0]),
            patch.object(validate_public.time, "sleep", side_effect=sleep),
            patch.object(validate_public, "urlopen", side_effect=failed_request),
        ):
            validate_public.validate_public_alias("https://alias.example/", errors)

        self.assertEqual(requests, [8])
        self.assertEqual(clock[0], 10)
        self.assertEqual(len(errors), 1)
        self.assertIn("public alias route failed: https://alias.example/guides/", errors[0])
        self.assertIn("budget exhausted", errors[0])
        self.assertIn("alias gateway unavailable", errors[0])

    def test_gateway_error_remains_failure_after_bounded_retries(self) -> None:
        clock = [0.0]
        requests = 0

        def gateway_error(request: object, timeout: float) -> None:
            nonlocal requests
            requests += 1
            clock[0] += 0.45
            raise HTTPError(request.full_url, 502, "Bad Gateway", {}, None)

        errors: list[str] = []
        with (
            patch.object(validate_public.time, "monotonic", side_effect=lambda: clock[0]),
            patch.object(validate_public.time, "sleep", side_effect=lambda delay: clock.__setitem__(0, clock[0] + delay)),
            patch.object(validate_public, "urlopen", side_effect=gateway_error),
        ):
            validate_public.validate_public_alias("https://alias.example/", errors)

        self.assertEqual(requests, validate_public.ALIAS_MAX_ATTEMPTS)
        self.assertLess(clock[0], validate_public.ALIAS_PROBE_BUDGET_SECONDS)
        self.assertEqual(len(errors), 1)
        self.assertIn("HTTP Error 502", errors[0])
        self.assertIn("failed after 6 attempts", errors[0])

    def test_deadline_is_shared_across_routes(self) -> None:
        clock = [0.0]
        urls: list[str] = []
        timeouts: list[float] = []

        class Response:
            status = 200

            class headers:
                @staticmethod
                def get_content_type() -> str:
                    return "text/html"

            def __init__(self, url: str) -> None:
                self.url = url

            def __enter__(self) -> Response:
                return self

            def __exit__(self, *_args: object) -> None:
                return None

            def read(self, _size: int) -> bytes:
                return b'<main id="content">'

            def geturl(self) -> str:
                return self.url

        def request(url_request: object, timeout: float) -> Response:
            url = url_request.full_url
            urls.append(url)
            timeouts.append(timeout)
            if len(urls) == 1:
                clock[0] = 7
                return Response(url)
            clock[0] += timeout
            raise URLError("gateway down")

        errors: list[str] = []
        with (
            patch.object(validate_public, "ALIAS_PROBE_BUDGET_SECONDS", 10),
            patch.object(validate_public.time, "monotonic", side_effect=lambda: clock[0]),
            patch.object(validate_public.time, "sleep", side_effect=lambda delay: clock.__setitem__(0, clock[0] + delay)),
            patch.object(validate_public, "urlopen", side_effect=request),
        ):
            validate_public.validate_public_alias("https://alias.example/", errors)

        self.assertEqual(urls, ["https://alias.example/guides/", "https://alias.example/guides/quickstart/"])
        self.assertEqual(timeouts, [8, 3])
        self.assertEqual(len(errors), 1)
        self.assertIn("quickstart/", errors[0])
        self.assertIn("gateway down", errors[0])

    def test_permanent_mime_mismatch_fails_without_retries(self) -> None:
        class Response:
            status = 200

            class headers:
                @staticmethod
                def get_content_type() -> str:
                    return "text/plain"

            def __enter__(self) -> Response:
                return self

            def __exit__(self, *_args: object) -> None:
                return None

            def read(self, _size: int) -> bytes:
                return b'<main id="content">'

            def geturl(self) -> str:
                return "https://alias.example/guides/"

        errors: list[str] = []
        with patch.object(validate_public, "urlopen", return_value=Response()) as opener:
            validate_public.validate_public_alias("https://alias.example/", errors)

        self.assertEqual(opener.call_count, 1)
        self.assertEqual(len(errors), 1)
        self.assertIn("HTTP 200 text/plain", errors[0])


if __name__ == "__main__":
    unittest.main()
