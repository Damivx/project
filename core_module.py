from input_module import get_input_url
from mitmproxy import http, ctx

class CoreEngine:
    def __init__(self, url):
        self.url = url

    def start_engine(self):
        # Load the URL like a browser to intercept HTTP/HTTPS requests
        self.load_url()
    
    def load_url(self):
        try:
            # Send GET request to the URL
            response = requests.get(self.url)
            # Check response status and content
            if response.status_code == 200:
                # Start intercepting requests using mitmproxy
                ctx.log.info("URL loaded successfully: {}".format(self.url))
            else:
                ctx.log.error("Failed to load URL: {} (Status code: {})".format(self.url, response.status_code))
        except Exception as e:
            ctx.log.error("Error loading URL: {}".format(str(e)))

    def intercept_request(self, flow: http.HTTPFlow):
        # Intercept HTTP requests and analyze for vulnerabilities
        request_url = flow.request.url
        request_method = flow.request.method
        request_headers = flow.request.headers
        request_body = flow.request.content

        # Write intercepted request details to a text file
        self.write_to_file(request_url, request_method, request_headers, request_body)

        # Process the vulnerabilities and send them to the output module (not implemented here)

    def write_to_file(self, request_url, request_method, request_headers, request_body):
        try:
            with open("intercepted_requests.txt", "a") as file:
                file.write("Request URL: {}\n".format(request_url))
                file.write("Request Method: {}\n".format(request_method))
                file.write("Request Headers:\n{}\n".format(request_headers))
                file.write("Request Body:\n{}\n\n".format(request_body))
                ctx.log.info("Intercepted request written to file: intercepted_requests.txt")
        except Exception as e:
            ctx.log.error("Error writing intercepted request to file: {}".format(str(e)))

def start_core_engine():
    input_url = get_input_url()
    core_engine = CoreEngine(input_url)
    core_engine.start_engine()

# Example usage
if __name__ == "__main__":
    start_core_engine()
