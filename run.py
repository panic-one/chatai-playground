from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    env = os.environ.get("ENV", "development")
    debug_mode = env == "development"
    app.run(host="0.0.0.0", port=5000, debug=debug_mode, use_reloader=False)
