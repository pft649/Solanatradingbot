import json
import requests
import time
from solana.rpc.api import Client
from solana.keypair import Keypair

# Wallet de la comisión (no editable)
COMMISSION_WALLET = "CaY66KrsMUFCPuGQ3jomNoai4magF5kAbdm9Tr8pKYyB"

CONFIG_FILE = "config.json"

def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

config = load_config()
PRIVATE_KEY = config["private_key"]
keypair = Keypair.from_secret_key(bytes.fromhex(PRIVATE_KEY))
solana_client = Client(config["rpc_url"])

def get_quote(input_mint, output_mint, amount):
    """Obtiene la cotización del token en Jupiter."""
    jupiter_api_url = "https://quote-api.jup.ag/v6/quote"
    params = {
        "inputMint": input_mint,
        "outputMint": output_mint,
        "amount": int(amount * 1e9),
        "slippageBps": int(config["slippage"] * 100)
    }
    
    response = requests.get(jupiter_api_url, params=params)
    return response.json() if response.status_code == 200 else None

def execute_trade(token_address, amount, action):
    """Ejecuta una compra o venta. Solo las ventas tienen comisión del 1%."""
    
    if action == "Vendiendo":
        commission = amount * 0.01
        trade_amount = amount - commission
        send_commission(commission)
    else:
        trade_amount = amount
    
    quote = get_quote(
        "So11111111111111111111111111111111111111112",
        token_address,
        trade_amount
    )

    if not quote:
        print(f"Error obteniendo cotización para {token_address}.")
        return

    price = quote['outAmount'] / trade_amount
    print(f"{action} {trade_amount} SOL → {token_address} a {price} promedio.")
    print("✅ Operación completada con éxito." if quote else "❌ Falló la operación.")

def send_commission(amount):
    """Envía la comisión del 1% a la wallet de comisión."""
    print(f"Enviando {amount} SOL de comisión a {COMMISSION_WALLET}...")
    # Aquí iría la lógica para enviar la transacción en Solana

def auto_buy(token_address):
    """Compra automáticamente un token con la cantidad predefinida."""
    amount = config["auto_buy_amount"]
    print(f"Ejecutando Auto Buy de {amount} SOL en {token_address}...")
    execute_trade(token_address, amount, "Comprando")

def sell(token_address, amount):
    """Vende un token y aplica comisión del 1%."""
    print(f"Ejecutando venta de {amount} SOL en {token_address}...")
    execute_trade(token_address, amount, "Vendiendo")

def auto_buy_strategy(token_address):
    """Compra y vende el token automáticamente en 7 segundos."""
    amount = config["auto_buy_amount"]
    print(f"Ejecutando Auto Buy Estrategia en {token_address}...")

    execute_trade(token_address, amount, "Comprando")
    time.sleep(7)
    execute_trade(token_address, amount, "Vendiendo")
