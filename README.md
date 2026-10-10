Crack Detector App
A web-based crack detection application that processes uploaded images using computer vision techniques and displays an image highlighting detected crack-like edges. Built with Python, Flask, OpenCV, NumPy, SciPy, and SQLite.
Features
- Upload an image through a web interface.
- Detect prominent edges and crack-like patterns using image processing.
- Apply Gaussian background filtering, Sobel gradients, oriented non-maximum suppression, and morphological closing.
- View the processed output image.
- Store processing history and timestamps in an SQLite database.
- Browse previously processed results through the history page.
Tech Stack
- Python — application logic
- Flask — web framework
- OpenCV — image processing
- NumPy — numerical operations
- SciPy — maximum-filter operations for non-maximum suppression
- SQLite — processing-history storage
- HTML/CSS — templates and interface
Project Structure
crack-detector-app/
├── app.py
├── crack_logic.py
├── database.db              # Created/used by the application
├── requirements.txt
├── render.yaml
├── templates/
│   ├── index.html
│   └── history.html
├── static/
│   └── output/              # Processed images are saved here
└── uploads/                 # Uploaded images are saved here
How It Works
1. The user uploads an image through the Flask interface.
2. The image is loaded in grayscale and normalized.
3. Gaussian filtering estimates the background, which is subtracted to emphasize local details.
4. Sobel operators calculate horizontal and vertical gradients; gradient magnitude and direction are computed.
5. A threshold suppresses weaker responses, and oriented non-maximum suppression thins the detected edges.
6. Morphological closing connects nearby edge segments, and the result is saved as a processed PNG image.
7. The application records the input filename, output filename, and upload timestamp in SQLite and displays the result.
Note: This is a classical image-processing approach, not a trained machine-learning model. Its output highlights edge patterns that may correspond to cracks; lighting, texture, image quality, and parameter settings can affect results. It should not be treated as a certified structural-safety assessment.

Requirements
- Python 3.9 or newer (a compatible Python version for your installed dependencies)
- pip
Installation and Run
1. Clone the repository and move into the project directory:
   git clone https://github.com/Geethaasree/crack-detector-app.git
   cd crack-detector-app
2. (Recommended) Create and activate a virtual environment:
   Windows
   python -m venv .venv
   .venv\Scripts\activate
   macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
3. Install dependencies:
   pip install -r requirements.txt
4. Start the application:
   python app.py
5. Open http://127.0.0.1:5000 in your browser.
The application creates the upload and output directories if they do not exist. The database table is initialized when init_db() is called; if starting the app locally does not initialize it automatically, ensure init_db() is called before serving requests.
Usage
- Open the home page.
- Select an image and submit it for processing.
- Review the generated crack-edge image.
- Visit /history to see recorded processing history.

