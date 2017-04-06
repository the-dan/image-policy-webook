import http.server
import logging
import json
import argparse

logging.basicConfig(level=logging.DEBUG)

# TODO: we could do better
valid_repos = []

class ImagePolicyWebhook(http.server.BaseHTTPRequestHandler):
	def do_POST(self):
		length = int(self.headers.get('content-length'))
		payload = self.rfile.read(length)
		payload = payload.decode("utf8")

		logging.debug("Request <%s>",payload)

		is_allowed = True
		bad_images = []
		reason = ""

		#valid_repos = ["dcr.qiwi.com"]

		review = json.loads(payload)
		containers = review["spec"]["containers"]
		for c in containers:
			for vr in valid_repos:
				if not c["image"].startswith(vr):
					bad_images.append(c["image"])
					is_allowed = False

		if not is_allowed:
			reason = "Following images are rejected by policy %s" % (repr(bad_images),)
			logging.info(reason)
		else:
			logging.info("All images are fine")

		response = {
			"apiVersion" : "imagepolicy.k8s.io/v1alpha1",
			"kind" : "ImageReview",
			"status" : {
				"allowed" : is_allowed,
				"reason" : reason
			}
		}

		self.send_response(200)
		self.end_headers()
		self.wfile.write(json.dumps(response).encode("utf8"))


def start_server(bind_address, port):
	server_address = (bind_address, port)
	handler_class = ImagePolicyWebhook
	httpd = http.server.HTTPServer(server_address, handler_class)
	httpd.serve_forever()

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='Kubernetes image repo policy checker')
	parser.add_argument('repos', metavar='REPO', type=str, nargs='+',
                    help='valid repos')
	parser.add_argument('--port', "-p", dest='port',
                    default=8090,
                    help='port to run on')
	parser.add_argument('--bind-address', "-b", dest='bind_address',
                    default="0.0.0.0",
                    help='listen on')
	
	args = parser.parse_args()
	port = args.port
	bind_address = args.bind_address
	valid_repos = args.repos
	start_server(bind_address, port)
