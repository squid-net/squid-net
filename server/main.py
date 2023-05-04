from app import app
import os
from pyngrok import ngrok

if __name__ == "__main__":
    ngrok_tunnel = ngrok.connect(6969)
    print('Public URL:', ngrok_tunnel.public_url)

    app.run("0.0.0.0", port=os.getenv('PORT', 6969))