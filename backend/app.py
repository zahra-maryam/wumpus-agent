from flask import Flask, jsonify, request
from flask_cors import CORS
import agent

WumpusWorld = agent.WumpusWorld
Agent = agent.Agent

app = Flask(__name__)
CORS(app)

world = WumpusWorld(6, 6)
agent_instance = Agent(world)


@app.route("/")
def home():
    return "Flask is running!"


@app.route("/step", methods=["GET"])
def step():
    percepts = agent_instance.perceive_and_update()
    pos = agent_instance.move()

    return jsonify({
        "x": pos[0],
        "y": pos[1],
        "percepts": percepts,
        "steps": agent_instance.inference_steps,
        "safe": list(agent_instance.safe),
        "danger": list(agent_instance.danger),
        "visited": list(agent_instance.visited)
    })


@app.route("/reset", methods=["GET"])
def reset():
    global world, agent_instance

    rows = int(request.args.get("rows", 6))
    cols = int(request.args.get("cols", 6))

    world = WumpusWorld(rows, cols)
    agent_instance = Agent(world)

    return jsonify({"message": "reset successful"})


if __name__ == "__main__":
    app.run()