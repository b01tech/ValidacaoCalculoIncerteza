from ambiente import CondicoesAmbientais
from balanca import Balanca
from pesagem import Pesagem
from calculadora import Calculadora

def main():
    while True:
        print("1 - Validar condições ambientais  2 - Validar cálculo de incerteza")
        op = input()

        if op == "1":
            ca = CondicoesAmbientais()
            ca.get_data()
            ca.validate_massa_especifica()

            input("Pressione qualquer tecla para continuar...")
            clear_screen()

        elif op == "2":
            bal = Balanca()
            bal.get_data()

            pesagem = Pesagem()
            pesagem.get_data()

            Calculadora.execute(bal, pesagem)

            input("Pressione qualquer tecla para continuar...")
            clear_screen()

        else:
            print("Opção inválida.")
            input("Pressione qualquer tecla para continuar...")
            clear_screen()

def clear_screen():
    print("\n" * 100)

if __name__ == "__main__":
    main()
