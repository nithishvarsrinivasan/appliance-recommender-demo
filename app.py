
from flask import Flask, request, jsonify, render_template
from recommender import ensure_data, load_data, Recommender, FeedbackStore

DATA_DIR = "data"
CSV_PATH = ensure_data(DATA_DIR)
DF = load_data(CSV_PATH)

recommender = Recommender(DF)
feedback_store = FeedbackStore()

app = Flask(__name__)

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/users")
def users():
    users = sorted(DF["user_id"].unique().tolist())
    return jsonify(users)

@app.get("/recommend")
def recommend():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error":"Missing required query parameter: user_id"}), 400
    rec = recommender.recommend_for_user(user_id)
    if rec is None:
        return jsonify({"error": f"No data for user_id={user_id}"}), 404
    stats = feedback_store.stats_for(rec["user_id"], rec["appliance"], rec["recommended_model"])
    return jsonify({"recommendation": rec, "feedback_stats": stats})

@app.post("/feedback")
def feedback():
    try:
        payload = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Invalid or missing JSON body"}), 400
    required = ["user_id","appliance","recommended_model","helpful"]
    missing = [k for k in required if k not in payload]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400
    if not isinstance(payload.get("helpful"), bool):
        return jsonify({"error":"'helpful' must be a boolean"}), 400
    stats = feedback_store.add(payload["user_id"], payload["appliance"], payload["recommended_model"], payload["helpful"])
    return jsonify({"ok": True, "tally": stats, "last_feedback": feedback_store.last})

if __name__ == "__main__":
    app.run(debug=True)
