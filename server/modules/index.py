from app import app
@app.route("/")
@app.route("/<name>")
def index(name='Anonymous'):
    return f"Hello {name}!!"