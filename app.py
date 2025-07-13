import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai

gemini = genai.Client()

app = Flask(__name__)
CORS(app)

@app.route('/analyze-image', methods=['POST'])
def analyze_image():
    # Get image URL from request
    data = request.get_json()
    if not data or 'imageUrl' not in data:
        return jsonify({"error": "Missing 'imageUrl' in request body"}), 400
    
    image_url = data['imageUrl']
    print(f"Backend: Received req to analyze image: {image_url}")
    
    contents = [
        {"text": "What do you see in this image? Provide a clear, concise, detailed, and helpful caption for someone with visual impairments. Focus on key objects, actions, and the overall scene."},
        {
            "fileData": {
                "mimeType": "image/jpeg",
                "fileUri": image_url
            }
        },
    ]
    
    try:
        response = gemini.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents
        )
        
        description = response.text
        print(f"Backend: Generated description: {description}")
        return jsonify({"description": description}), 200
    
    except Exception as e:
        print(f"Backend: Error calling API: {e}")
        return jsonify({"error": f"Failed to analyze image: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)