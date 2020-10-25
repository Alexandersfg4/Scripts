import re, json
from mitmproxy import http

regex = re.compile('.*(graph.microsoft.com).*')

error_resource_type = {
  "error": {
    "code": "serviceNotAvailable",
    "message": "The service is not available. Try the request again after a delay. There may be a Retry-After header.",
    "innerError": {
      "requestId": "87725851-77fb-xxxx-xxxx-xxxxxxxxxxxx",
      "date": "2020-03-01T16:55:43"
    }
  }
}

"""Send a reply from the proxy without sending any data to the remote server."""

def request(flow: http.HTTPFlow) -> None:
    if regex.search(flow.request.pretty_url):
        print('SUCCESS!')
        flow.response = http.HTTPResponse.make(
            503,  # (optional) status code
            json.dumps(error_resource_type),  # (optional) content
            {"Content-Type": "application/json"}
        )



if __name__ == '__main__':
    request()