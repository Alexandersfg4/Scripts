from mitmproxy import http
import re

#query, value = "rating__gte", 4
query, value = "rating", 0

def request(flow: http.HTTPFlow) -> None:
    if re.match(r"https://myb11966.test.mybook.tech/api/books/*", flow.request.url):
        flow.request.query[query] = value
        flow.request.headers["Authorization"] = ''
    elif re.match(r"https://myb11966.test.mybook.tech/api/catalog/series/\d*/books/", flow.request.url):
        flow.request.query[query] = value
        flow.request.headers["Authorization"] = ''
    else:
        pass
