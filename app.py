import base64
import io
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from google import genai
from PIL import Image
import requests

app = Flask(__name__)
CORS(app)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["60 per minute"]
)
PROMPT = (
    "What do you see in this image? "
    "Provide a clear, concise, detailed, and helpful caption for someone with visual impairments. "
    "Focus on key objects, actions, and the overall scene. "
    "Limit the given description to less than 40 words."
)

@app.route('/analyze-image', methods=['POST'])
@limiter.limit("30 per minute") # Limit for this route
def analyze_image():
    # Get API Key from req header
    api_key = request.headers.get('x-api-key')
    if not api_key:
        return jsonify({'error': 'API key is missing'}), 401
    
    # Get image URL from request
    data = request.get_json()
    if not data or 'imageUrl' not in data:
        return jsonify({"error": "Missing 'imageUrl' in request body"}), 400
    
    image_url = data['imageUrl']
    print(f"Backend: Received req to analyze image: {image_url}")
    
    try:
        gemini = genai.Client(api_key=api_key)
        image_data = get_image_source(image_url)
        
        image = Image.open(io.BytesIO(image_data['bytes'])).convert('RGB')
        contents = [PROMPT, image]
    
        response = gemini.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
        )
        
        description = response.text
        print(f"Backend: Generated description: {description}")
        return jsonify({"description": description}), 200
    
    except Exception as e:
        print(f"Backend: Error calling API: {e}")
        return jsonify({"error": f"Failed to analyze image: {str(e)}"}), 500

def get_image_source(source_url):
    if source_url.startswith('http'):
        response = requests.get(source_url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        return {
            "bytes": response.content,
            "mime_type": response.headers.get('Content-Type', 'image/jpeg')
        }
    
    if source_url.startswith('data:image'):
        header, encoded_data = source_url.split(',', 1)
        mime_type = header.split(';')[0].split(':')[1]
        image_bytes = base64.b64decode(encoded_data)
        return {
            "bytes": image_bytes,
            "mime_type": mime_type
        }
    
    raise ValueError("Unsupported URL or data format")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
@app.route('/', methods=['GET'])
def health_check():
    # A simple endpoint for pings
    return jsonify({"status": "healthy"}), 200