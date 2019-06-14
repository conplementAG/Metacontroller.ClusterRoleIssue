from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json

class Controller(BaseHTTPRequestHandler):
  def sync(self, parent, children):
    name = parent.get("spec", {}).get("name", "no-name-defined")

    # Generate the desired child object(s).
    desired_children = [
      {
        "apiVersion": "v1",
        "kind": "Namespace",
        "metadata": {
          "name": name
        }
      },
      {
        "apiVersion": "rbac.authorization.k8s.io/v1",
        "kind": "ClusterRole",
        "metadata": {
          "name": name + "-my-special-role",
          "namespace": name
        },
        "rules": [
          {
            "apiGroups": ["conplement.cloud"],
            "resources": ["supernamespaces"],
            "verbs": ["get", "list", "update", "delete"],
            "resourceNames": [name]
          }
        ]
      }
    ]

    return {"children": desired_children}

  def do_POST(self):
    # Serve the sync() function as a JSON webhook.
    observed = json.loads(self.rfile.read(int(self.headers.getheader("content-length"))))
    desired = self.sync(observed["parent"], observed["children"])

    self.send_response(200)
    self.send_header("Content-type", "application/json")
    self.end_headers()
    self.wfile.write(json.dumps(desired))

HTTPServer(("", 80), Controller).serve_forever()