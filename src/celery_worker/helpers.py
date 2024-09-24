import json

from src import BASE_DIR


def mark_node_unhealthy():
    with open(f"{BASE_DIR}/health.json", "r") as file:
        data = json.load(file)

    data["healthy"] = False

    with open(f"{BASE_DIR}/health.json", "w") as file:
        json.dump(data, file)
