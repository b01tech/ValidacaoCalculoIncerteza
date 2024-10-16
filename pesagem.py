class Pesagem:
    def __init__(self):
        self.soma_valor_real = 0.0
        self.soma_incertezas = 0.0
        self.material = 0

        self.leitura1 = 0.0
        self.leitura2 = 0.0
        self.leitura3 = 0.0

    def get_data(self):
        l1 = self.get_double_from_user("Leitura 1: ")
        l2 = self.get_double_from_user("Leitura 2: ")
        l3 = self.get_double_from_user("Leitura 3: ")
        valor = self.get_double_from_user("Informe a soma do valor convencional dos pesos utilizados: ")
        incerteza = self.get_double_from_user("Informe a soma das incertezas dos pesos: ")
        material = self.get_material("Qual o material dos pesos?\n(1 - INOX  2 - FERRO   3 - LATÃO): ")
        self.set_data(l1, l2, l3, valor, incerteza, material)

    def set_data(self, l1, l2, l3, valor, incerteza, material):
        self.leitura1 = l1
        self.leitura2 = l2
        self.leitura3 = l3
        self.soma_valor_real = valor
        self.soma_incertezas = incerteza
        self.material = material

    def get_double_from_user(self, message):
        while True:
            try:
                value = float(input(message))
                return value
            except ValueError:
                print("Valor inválido. Por favor, insira um número válido.")

    def get_material(self, message):
        while True:
            try:
                value = int(input(message))
                if value not in [1, 2, 3]:
                    raise ValueError
                return value
            except ValueError:
                print("Valor inválido. Por favor, insira um número válido.")
