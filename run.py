"""
Simple script to run the Flask application
"""
from app import app, HOST, PORT, DEBUG

if __name__ == "__main__":
    print(f"""
    ========================================================
         Alliance Management System - Flask Server
    ========================================================

    Starting Flask server...

    Server URL: http://localhost:{PORT}
    Health:     http://localhost:{PORT}/health

    Press CTRL+C to stop the server
    """)

    app.run(host=HOST, port=PORT, debug=DEBUG)
