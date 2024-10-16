import math

class CondicoesAmbientais:
    def __init__(self):
        self.temperatura = None
        self.umidade = None
        self.pressao = None
        self.massa_especifica = None

    def get_data(self):
        temp_inicial = self.get_float_from_user("Informe a temperatura inicial(ºC): ")
        temp_final = self.get_float_from_user("Informe a temperatura final(ºC): ")
        rh_inicial = self.get_float_from_user("Informe a umidade inicial(RH %): ")
        rh_final = self.get_float_from_user("Informe a umidade final(RH %): ")
        pressao_inicial = self.get_float_from_user("Informe a pressão inicial(hPa): ")
        pressao_final = self.get_float_from_user("Informe a pressão final(hPa): ")

        self.set_data(temp_inicial, temp_final, rh_inicial, rh_final, pressao_inicial, pressao_final)

    def set_data(self, temp_inicial, temp_final, umidade_inicial, umidade_final, pressao_inicial, pressao_final):
        self.temperatura = abs(temp_inicial + temp_final) / 2
        self.umidade = abs(umidade_inicial + umidade_final) / 2
        self.pressao = abs(pressao_inicial + pressao_final) / 2
        self.calc_massa_especifica(self.temperatura, self.umidade, self.pressao)

    def get_float_from_user(self, message):
        while True:
            try:
                value = float(input(message))
                return value
            except ValueError:
                print("Valor inválido. Por favor, insira um número válido.")

    def calc_massa_especifica(self, temp, umidade, pressao):
        self.massa_especifica = ((0.348444 * pressao) - (umidade * ((0.00252 * temp) - 0.020582))) / (273.15 + temp)

    def validate_massa_especifica(self):
        print(f"A massa específica é de: {self.massa_especifica:.2f}kg/m³")
        print("A massa deve ficar entre 1,08 e 1,32kg/m³")
