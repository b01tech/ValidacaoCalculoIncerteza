class Balanca:
    def __init__(self):
        self.resolucao = None

    def get_data(self):
        res = self.get_float_from_user("Qual a resolução da balança: ")
        self.resolucao = res

    def get_float_from_user(self, message):
        while True:
            try:
                value = float(input(message))
                return value
            except ValueError:
                print("Valor inválido. Por favor, insira um número válido.")
