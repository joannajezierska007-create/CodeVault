import json
import os

VAULT_FILE = "vault.json"

def init():
    if not os.path.exists(VAULT_FILE):
        with open(VAULT_FILE, "w") as f:
            json.dump({}, f)


def add_entry(original, locked):
    data = load()
    data[locked] = original

    with open(VAULT_FILE, "w") as f:
        json.dump(data, f, indent=4)


def load():
    with open(VAULT_FILE, "r") as f:
        return json.load(f)