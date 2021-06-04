from mitmproxy import http
import re

# Наши квери параметры
query, value = "rating__gte", 4


def request(flow: http.HTTPFlow) -> None:
    if re.match(r"https://myb11966.test.mybook.tech/api/books/*", flow.request.url):
        flow.request.query[query] = value
        flow.request.headers["Authorization"] = ''
