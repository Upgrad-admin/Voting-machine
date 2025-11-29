from flask import Flask, render_template, request, redirect
import redis

app = Flask(__name__)

# Redis connection
redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

# Initialize keys if not present
OPTIONS = ["Cats", "Dogs", "Parrots"]

for option in OPTIONS:
    if not redis_client.exists(option):
        redis_client.set(option, 0)


@app.route("/")
def index():
    # Read voting counts
    votes = {option: int(redis_client.get(option)) for option in OPTIONS}

    # Calculate percentage
    total_votes = sum(votes.values())
    percentages = {}
    for option in OPTIONS:
        percentages[option] = (
            (votes[option] / total_votes * 100) if total_votes > 0 else 0
        )

    return render_template("index.html", votes=votes, percentages=percentages)


@app.route("/vote", methods=["POST"])
def vote():
    selected = request.form.get("vote_option")
    if selected in OPTIONS:
        redis_client.incr(selected)
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
