import json
from mitmproxy import http
from mitmproxy import ctx

class ChangeHTTPCode:
    filter = "mybook.ru/api/info/"

    def response(self, flow: http.HTTPFlow) -> None:
        if (self.filter in flow.request.pretty_url):
           # with flow.response.decode:  # automatically decode gzipped responses.
             data = json.loads(flow.response.content)
             data["language_counters"]["en"]["free"] = 0
             data["language_counters"]["en"]["only_pro"] = 0
             data["language_counters"]["en"]["standard"] = 0
             data["language_counters"]["en"]["standard_free"] = 0
             data["language_counters"]["en"]["audio"] = 0
             data["language_counters"]["en"]["text"] = 0
             data["language_counters"]["en"]["rent_only"] = 0
             data["language_counters"]["en"]["is_synced"] = 0
             data["language_counters"]["en"]["total"] = 0
             data["language_counters"]["en"]["podcast"] = 0

             data["language_counters"]["ru"]["free"] = 0
             data["language_counters"]["ru"]["only_pro"] = 0
             data["language_counters"]["ru"]["standard"] = 0
             data["language_counters"]["ru"]["standard_free"] = 0
             data["language_counters"]["ru"]["audio"] = 0
             data["language_counters"]["ru"]["text"] = 0
             data["language_counters"]["ru"]["rent_only"] = 0
             data["language_counters"]["ru"]["is_synced"] = 0
             data["language_counters"]["ru"]["total"] = 0
             data["language_counters"]["ru"]["podcast"] = 0

             data["language_counters"]["uk"]["free"] = 0
             data["language_counters"]["uk"]["only_pro"] = 0
             data["language_counters"]["uk"]["standard"] = 0
             data["language_counters"]["uk"]["standard_free"] = 0
             data["language_counters"]["uk"]["audio"] = 0
             data["language_counters"]["uk"]["text"] = 0
             data["language_counters"]["uk"]["rent_only"] = 0
             data["language_counters"]["uk"]["is_synced"] = 0
             data["language_counters"]["uk"]["total"] = 0
             data["language_counters"]["uk"]["podcast"] = 0

             flow.response.content = str.encode(json.dumps(data))

addons = [ChangeHTTPCode()]


