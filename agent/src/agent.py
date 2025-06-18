# agent/src/agent.py
import requests

AGENT_ID = "agent-001"
NACFY_SERVER = "http://localhost:3000"

def fetch_config(agent_id):
    try:
        res = requests.get(f"{NACFY_SERVER}/api/config/{agent_id}")
        res.raise_for_status()
        return res.json()
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch config: {e}")
        return None

def main():
    config = fetch_config(AGENT_ID)
    if config:
        print(f"[INFO] config received: {config}")


if __name__ == "__main__":
    main()
