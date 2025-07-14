# AdaLens - Backend API

This repository contains the backend server for the **AdaLens Chrome Extension**. Its sole purpose is to securely receive image analysis requests from the extension, interact with the Google Gemini API using a user-provided key, and return the generated description.

The backend is built with Python and Flask and is designed to be stateless, secure, and efficient. It is deployed on Render and communicates with the [frontend extension](https://github.com/sijun-kevin-hu/AdaLens).

## ✨ Key Features

- **Secure API Endpoint:** Handles image analysis requests from the extension.
- **Per-Request Authentication:** Safely uses the API key provided by each user in the request header, without storing it.
- **Stateless Design:** No user data or API keys are ever logged or stored on the server.
- **Rate Limiting:** Protects the API from abuse and excessive usage.
- **Production-Ready:** Deployed with Gunicorn for stable performance.

## API Endpoint

### `POST /analyze-image`

Receives an image URL and an API key, and returns an AI-generated description.

- **Method:** `POST`
- **Headers:**
- `Content-Type: application/json`
- `x-api-key: YOUR_GEMINI_API_KEY`
- **Request Body:**

    ```json
    {
      "imageUrl": "[https://path.to/some/image.jpg](https://path.to/some/image.jpg)"
    }
    ```

- **Success Response (200):**

    ```json
    {
      "description": "A clear and concise description of the image."
    }
    ```

## 🛠️ Local Development Setup

To run this server locally for development or contributions:

1. **Clone the repository:**

    ```bash
    git clone [https://github.com/sijun-kevin-hu/AdaLens_Backend.git](https://github.com/your-username/adalens-backend.git)
    cd AdaLens_Backend
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

3. **Install Python dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Flask server:**

    ```bash
    flask run
    ```

The backend server will now be running on `http://127.0.0.1:5000`.

## 💻 Tech Stack

- **Framework:** Python, Flask
- **WSGI Server:** Gunicorn
- **API:** Google Gemini
- **Deployment:** Render
