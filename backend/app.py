from flask import Flask, jsonify
from flask_cors import CORS
from agent import WumpusWorld, Agent

app = Flask(__name__)
CORS(app)

world = WumpusWorld(6, 6)
agent = Agent(world)


@app.route("/")
def home():
    return "Flask is running!"


@app.route("/step", methods=["GET"])
def step():
    percepts = agent.perceive_and_update()
    pos = agent.move()

    return jsonify({
        "x": pos[0],
        "y": pos[1],
        "percepts": percepts,
        "steps": agent.inference_steps,
        "safe": list(agent.safe),
        "danger": list(agent.danger),
        "visited": list(agent.visited)
    })


@app.route("/reset", methods=["GET"])
def reset():
    global world, agent
    world = WumpusWorld(6, 6)
    agent = Agent(world)

    return jsonify({"message": "reset successful"})


if __name__ == "__main__":
    app.run(debug=True)