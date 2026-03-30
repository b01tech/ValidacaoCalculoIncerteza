import tkinter as tk
from tkinter import ttk, messagebox
import math

from ambiente import CondicoesAmbientais
from balanca import Balanca
from pesagem import Pesagem
from calculadora import Calculadora

class AppGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Validação Cálculo de Incerteza")
        self.geometry("750x550")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        self.create_tab_ambiente()
        self.create_tab_incerteza()

    def create_tab_ambiente(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Condições Ambientais")

        # Layout for Inputs
        frame_inputs = ttk.LabelFrame(tab, text="Dados Ambientais", padding=(10, 10))
        frame_inputs.pack(fill="x", padx=10, pady=10)

        self.env_vars = {}
        fields = [
            ("Temperatura Inicial (ºC)", "temp_ini"),
            ("Temperatura Final (ºC)", "temp_fin"),
            ("Umidade Inicial (RH %)", "umi_ini"),
            ("Umidade Final (RH %)", "umi_fin"),
            ("Pressão Inicial (hPa)", "pressao_ini"),
            ("Pressão Final (hPa)", "pressao_fin"),
        ]

        for i, (label, var_name) in enumerate(fields):
            ttk.Label(frame_inputs, text=label).grid(row=i, column=0, sticky="w", pady=5)
            var = tk.StringVar()
            ttk.Entry(frame_inputs, textvariable=var).grid(row=i, column=1, sticky="ew", padx=10, pady=5)
            self.env_vars[var_name] = var

        frame_inputs.columnconfigure(1, weight=1)

        btn_calc = ttk.Button(tab, text="Calcular", command=self.calc_ambiente)
        btn_calc.pack(pady=10)

        # Result Frame
        frame_result = ttk.LabelFrame(tab, text="Resultado", padding=(10, 10))
        frame_result.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.env_result_var = tk.StringVar()
        ttk.Label(frame_result, textvariable=self.env_result_var, font=("Arial", 11)).pack(anchor="w")

    def calc_ambiente(self):
        try:
            temp_ini = float(self.env_vars["temp_ini"].get())
            temp_fin = float(self.env_vars["temp_fin"].get())
            umi_ini = float(self.env_vars["umi_ini"].get())
            umi_fin = float(self.env_vars["umi_fin"].get())
            pressao_ini = float(self.env_vars["pressao_ini"].get())
            pressao_fin = float(self.env_vars["pressao_fin"].get())

            ca = CondicoesAmbientais()
            ca.set_data(temp_ini, temp_fin, umi_ini, umi_fin, pressao_ini, pressao_fin)
            
            massa = ca.massa_especifica
            status = "OK" if 1.08 <= massa <= 1.32 else "FORA DA FAIXA"
            
            result_text = f"Massa Específica: {massa:.4f} kg/m³\n\n"
            result_text += f"Status: {status}\n(A massa deve ficar entre 1,08 e 1,32 kg/m³)"
            
            self.env_result_var.set(result_text)

        except ValueError:
            messagebox.showerror("Erro de Validação", "Por favor, insira apenas valores numéricos válidos.")

    def create_tab_incerteza(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Cálculo de Incerteza")

        # Create two columns
        pane = ttk.PanedWindow(tab, orient="horizontal")
        pane.pack(fill="both", expand=True, padx=10, pady=10)
        
        frame_left = ttk.Frame(pane)
        frame_right = ttk.Frame(pane)
        pane.add(frame_left, weight=1)
        pane.add(frame_right, weight=1)

        # Left Column - Inputs
        frame_inputs = ttk.LabelFrame(frame_left, text="Dados da Balança e Pesagem", padding=(10, 10))
        frame_inputs.pack(fill="both", expand=True)

        self.inc_vars = {}
        fields = [
            ("Resolução da Balança", "resolucao"),
            ("Leitura 1", "l1"),
            ("Leitura 2", "l2"),
            ("Leitura 3", "l3"),
            ("Soma Valor Real (Pesos)", "soma_vc"),
            ("Soma Incertezas (Pesos)", "soma_inc"),
        ]

        for i, (label, var_name) in enumerate(fields):
            ttk.Label(frame_inputs, text=label).grid(row=i, column=0, sticky="w", pady=5)
            var = tk.StringVar()
            ttk.Entry(frame_inputs, textvariable=var).grid(row=i, column=1, sticky="ew", padx=10, pady=5)
            self.inc_vars[var_name] = var

        ttk.Label(frame_inputs, text="Material dos Pesos").grid(row=len(fields), column=0, sticky="w", pady=5)
        self.inc_vars["material"] = tk.StringVar(value="1 - INOX")
        cb_material = ttk.Combobox(frame_inputs, textvariable=self.inc_vars["material"], state="readonly")
        cb_material['values'] = ('1 - INOX', '2 - FERRO', '3 - LATÃO')
        cb_material.grid(row=len(fields), column=1, sticky="ew", padx=10, pady=5)

        frame_inputs.columnconfigure(1, weight=1)

        btn_calc = ttk.Button(frame_left, text="Calcular", command=self.calc_incerteza)
        btn_calc.pack(pady=10)

        # Right Column - Result
        frame_result = ttk.LabelFrame(frame_right, text="Resultado", padding=(10, 10))
        frame_result.pack(fill="both", expand=True)
        
        self.inc_result_var = tk.StringVar()
        lbl_result = ttk.Label(frame_result, textvariable=self.inc_result_var, font=("Consolas", 11), justify="left")
        lbl_result.pack(anchor="nw")

    def calc_incerteza(self):
        try:
            bal = Balanca()
            bal.resolucao = float(self.inc_vars["resolucao"].get().replace(",", "."))

            pesagem = Pesagem()
            l1 = float(self.inc_vars["l1"].get().replace(",", "."))
            l2 = float(self.inc_vars["l2"].get().replace(",", "."))
            l3 = float(self.inc_vars["l3"].get().replace(",", "."))
            valor = float(self.inc_vars["soma_vc"].get().replace(",", "."))
            incerteza = float(self.inc_vars["soma_inc"].get().replace(",", "."))
            
            material_str = self.inc_vars["material"].get()
            material_val = int(material_str.split(" - ")[0])
            
            pesagem.set_data(l1, l2, l3, valor, incerteza, material_val)

            # Usando as funções da Calculadora
            _k = 2.0  # fator de abrangência da calibração do Peso
            media = Calculadora.calc_media(pesagem.leitura1, pesagem.leitura2, pesagem.leitura3)
            s = Calculadora.calc_s(pesagem.leitura1, pesagem.leitura2, pesagem.leitura3)
            ua = Calculadora.calc_ua(s)
            up = Calculadora.calc_up(pesagem.soma_incertezas, _k)
            ur = Calculadora.calc_ur(bal.resolucao)
            ud = Calculadora.calc_ud(pesagem.soma_incertezas)
            ue = Calculadora.calc_ue(pesagem.soma_valor_real, pesagem.material)
            uc = Calculadora.calc_uc(ua, up, ur, ud, ue)
            veff = Calculadora.calc_veff(uc, ua)
            fator_k = Calculadora.calc_fator_k(math.floor(veff))
            ux = Calculadora.calc_ux(uc, fator_k)

            result = (
                f"Media de leitura:  {media:.6f}\n"
                f"Valor s:           {s:.6f}\n\n"
                f"Incerteza UA:      {ua:.6f}\n"
                f"Incerteza UP:      {up:.6f}\n"
                f"Incerteza UR:      {ur:.6f}\n"
                f"Incerteza UD:      {ud:.6f}\n"
                f"Incerteza UE:      {ue:.6f}\n\n"
                f"Incerteza Comb. UC:{uc:.6f}\n"
                f"Veff:              {veff:.2f}\n"
                f"Fator de abrangência K: {fator_k:.4f}\n\n"
                f"Incerteza Expandida Ux: {ux:.6f}\n"
            )

            self.inc_result_var.set(result)

        except ValueError:
            messagebox.showerror("Erro de Validação", "Por favor, insira apenas valores numéricos válidos.")

if __name__ == "__main__":
    app = AppGUI()
    app.mainloop()