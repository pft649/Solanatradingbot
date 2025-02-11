import json

CONFIG_FILE = "config.json"

def set_private_key():
    """Permite establecer la clave privada desde la terminal."""
    new_key = input("Introduce tu nueva clave privada: ")
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
    
    config["private_key"] = new_key

    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

    print("Clave privada actualizada con éxito.")
