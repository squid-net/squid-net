from app import app
@app.route("/revshell")
def revshell():
    return f"just took over ur computer (scary)"