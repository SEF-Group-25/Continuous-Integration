from flask import Flask

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    pass

@app.route("/history", methods=["GET"])
def history():
    pass

@app.route("/history/<commit_id>", methods=["GET"])
def history_details(commit_id):
    pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)