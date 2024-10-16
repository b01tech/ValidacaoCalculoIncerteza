import math

class Calculadora:
    VeffValues = [1, 2, 3, 4, 5, 6, 7, 8, 10, 20, 50, float('inf')]
    KValues = [13.97, 4.53, 3.31, 2.87, 2.65, 2.52, 2.43, 2.37, 2.28, 2.13, 2.05, 2.00]

    @staticmethod
    def calc_media(l1, l2, l3):
        return (l1 + l2 + l3) / 3

    @staticmethod
    def calc_ua(l1, l2, l3):
        media = Calculadora.calc_media(l1, l2, l3)
        s = math.sqrt(((l1 - media) ** 2 + (l2 - media) ** 2 + (l3 - media) ** 2) / 2)
        return s / math.sqrt(3)

    @staticmethod
    def calc_up(soma_incerteza_pd, k):
        return soma_incerteza_pd / k

    @staticmethod
    def calc_ur(res):
        return res * 0.5 / math.sqrt(3)

    @staticmethod
    def calc_ud(soma_incerteza_pd):
        return soma_incerteza_pd / math.sqrt(3)

    @staticmethod
    def calc_ue(vc_peso, ppm):
        return ((vc_peso / 1000000000.0) * ppm) / math.sqrt(3)

    @staticmethod
    def calc_uc(ua, up, ur, ud, ue):
        soma_quadrados = ua**2 + up**2 + ur**2 + ud**2 + ue**2
        return math.sqrt(soma_quadrados)

    @staticmethod
    def calc_ux(uc, fator_k):
        return uc * fator_k

    @staticmethod
    def calc_veff(uc, ua):
        v = 2  # número de medições menos 1
        if ua == 0.0:
            return float('inf')
        else:
            veff = (uc**4) / ((ua**4) / v)
            return veff

    @staticmethod
    def calc_fator_k(veff):
        if veff <= Calculadora.VeffValues[0]:
            return Calculadora.KValues[0]
        if veff >= Calculadora.VeffValues[-2]:
            return Calculadora.KValues[-1]

        for i in range(len(Calculadora.VeffValues) - 1):
            if veff >= Calculadora.VeffValues[i] and veff <= Calculadora.VeffValues[i + 1]:
                veff1 = Calculadora.VeffValues[i]
                veff2 = Calculadora.VeffValues[i + 1]
                k1 = Calculadora.KValues[i]
                k2 = Calculadora.KValues[i + 1]
                return k1 + ((veff - veff1) * (k2 - k1)) / (veff2 - veff1)
        return 0.0

    @staticmethod
    def execute(balanca, pesagem):
        _k = 2.0  # fator de abrangência da calibração do Peso
        media = Calculadora.calc_media(pesagem.leitura1, pesagem.leitura2, pesagem.leitura3)
        ua = Calculadora.calc_ua(pesagem.leitura1, pesagem.leitura2, pesagem.leitura3)
        up = Calculadora.calc_up(pesagem.soma_incertezas, _k)
        ur = Calculadora.calc_ur(balanca.resolucao)
        ud = Calculadora.calc_ud(pesagem.soma_incertezas)
        ue = Calculadora.calc_ue(pesagem.soma_valor_real, pesagem.material)
        uc = Calculadora.calc_uc(ua, up, ur, ud, ue)
        veff = Calculadora.calc_veff(uc, ua)
        fator_k = Calculadora.calc_fator_k(veff)
        ux = Calculadora.calc_ux(uc, fator_k)

        result = (
            f"Media de leitura: {media}\n"
            f"Incerteza calculada por meios estatísticos UA: {ua}\n"
            f"Incerteza do peso padrão UP: {up}\n"
            f"Incerteza da resolução da balança UR: {ur}\n"
            f"Incerteza da deriva do padrão UD: {ud}\n"
            f"Incerteza do empuxo do ar UE: {ue}\n"
            f"Incerteza combinada UC: {uc}\n"
            f"Veff: {veff}\n"
            f"Fator de abrangência K: {fator_k}\n"
            f"Incerteza expandida: {ux}\n"
        )
        print(result)

