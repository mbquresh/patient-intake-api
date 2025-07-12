from flask import Flask, request, jsonify
from requests_toolbelt.multipart import decoder
import re

app = Flask(__name__)

@app.route('/parse-multipart', methods=['POST'])
def parse_multipart():
    content_type = request.headers.get('Content-Type')
    body = request.get_data()
    if not content_type or not body:
        return jsonify({"error": "Missing Content-Type or body"}), 400

    multipart_data = decoder.MultipartDecoder(body, content_type)
    parsed_data = {}

    for part in multipart_data.parts:
        disposition = part.headers.get(b"Content-Disposition", b"").decode()
        match = re.search(r'name="(.+?)"', disposition)
        if match:
            name = match.group(1)
            value = part.content.decode("utf-8")
            parsed_data[name] = value

    return jsonify(parsed_data)

if __name__ == "__main__":
    app.run(debug=True)
