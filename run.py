from app import create_app
from app.config import Config

app = create_app()

if __name__ == '__main__':
    # Use config-configured port and debug mode
    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)
