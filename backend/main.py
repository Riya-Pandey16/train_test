# backend/main.py
#import eventlet
#eventlet.monkey_patch()
from apps import create_app, socketio
from flask import send_from_directory
import os



# Get absolute path to frontend/dist
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.abspath(os.path.join(BASE_DIR, '../frontend/dist'))

print("Static folder exists:", os.path.exists(DIST_DIR))
print("Index.html exists:", os.path.exists(os.path.join(DIST_DIR, 'index.html')))



app = create_app(static_folder=DIST_DIR)  # Pass to factory

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_vue_app(path):
    file_path = os.path.join(app.static_folder, path)
    if path != "" and os.path.exists(file_path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)
