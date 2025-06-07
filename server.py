import http.server
import json
import socketserver
import spacy
import urllib.parse

PORT = 8080

nlp = spacy.load('./construction/training/ner_and_textcat')

class MyHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
    
        # Parse the query string
        parsed_url = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        print(query_params)
        
        # Send the results in json format if we got a query string
        data = {}
        if 'q' in query_params:
            text = query_params['q'][0]
            doc = nlp(text)
            data = doc.to_json()
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        json_data = json.dumps(data)
        self.wfile.write(json_data.encode('utf-8'))

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
