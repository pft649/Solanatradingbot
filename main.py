from trading import auto_buy, auto_buy_strategy
from wallet_manager import set_private_key

def main():
    while True:
        print("\nMenú:")
        print("1. Auto Buy (rápido)")
        print("2. Auto Buy Estrategia")
        print("3. Cambiar clave privada")
        print("4. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            token = input("Contrato del token: ")
            auto_buy(token)
        elif opcion == "2":
            token = input("Contrato del token: ")
            auto_buy_strategy(token)
        elif opcion == "3":
            set_private_key()
        elif opcion == "4":
            print("Saliendo...")
            break

if __name__ == "__main__":
    main()
