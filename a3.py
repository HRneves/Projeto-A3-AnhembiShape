import tkinter as tk
from tkinter import messagebox
import time

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class AppFitness(tk.Tk, metaclass=SingletonMeta):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("App Fitness")
        self.attributes('-fullscreen', True)  # Iniciar em tela cheia

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (WelcomePage, IMCPage, TreinoPage, CronometroPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("WelcomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class WelcomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Bem-vindo ao App Fitness!", font=("Helvetica", 16)).pack(pady=10)
        tk.Button(self, text="Calculo de IMC", command=lambda: controller.show_frame("IMCPage"), width=15).pack(pady=5)
        tk.Button(self, text="Treino", command=lambda: controller.show_frame("TreinoPage"), width=15).pack(pady=5)
        tk.Button(self, text="Cronômetro", command=lambda: controller.show_frame("CronometroPage"), width=15).pack(pady=5)
        tk.Button(self, text="Fechar", command=self.fechar_app, width=15).pack(pady=5)

    def fechar_app(self):
        AppFitness().destroy()

class IMCPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Preencha os dados para calcular o IMC:", font=("Helvetica", 14)).pack(pady=10)

        label_peso = tk.Label(self, text="Peso (kg):", font=("Helvetica", 12))
        label_altura = tk.Label(self, text="Altura (cm):", font=("Helvetica", 12))

        entry_peso = tk.Entry(self, font=("Helvetica", 14))
        entry_altura = tk.Entry(self, font=("Helvetica", 14))

        label_peso.pack(pady=5)
        entry_peso.pack(pady=5)
        label_altura.pack(pady=5)
        entry_altura.pack(pady=5)

        tk.Button(self, text="Calcular IMC", command=lambda: self.calcular_imc(entry_peso, entry_altura, controller), width=15).pack(pady=10)
        tk.Button(self, text="Voltar ao Menu", command=lambda: controller.show_frame("WelcomePage"), width=15).pack(pady=5)

        self.label_resultado_imc = tk.Label(self, text="", font=("Helvetica", 14))
        self.label_resultado_imc.pack(pady=10)

    def calcular_imc(self, entry_peso, entry_altura, controller):
        try:
            peso = float(entry_peso.get())
            altura_cm = float(entry_altura.get())
            altura_m = altura_cm / 100
            imc = peso / (altura_m ** 2)

            resultado = f"Seu IMC é: {imc:.2f}"
            categoria = self.obter_categoria_imc(imc)
            resultado_final = f"{resultado} ({categoria})"
            self.label_resultado_imc.config(text=resultado_final)

            sugestao = self.obter_sugestao_treino(imc)
            messagebox.showinfo("Resultado", f"{resultado_final}\n\n{sugestao}")
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores numéricos para peso e altura.")

    def obter_categoria_imc(self, imc):
        if imc < 18.5:
            return "Abaixo do peso"
        elif 18.5 <= imc < 24.99:
            return "Peso normal"
        elif 25 <= imc < 29.99:
            return "Sobrepeso"
        elif 30 <= imc < 34.99:
            return "Obesidade Grau 1"
        elif 35 <= imc < 39.99:
            return "Obesidade Grau 2 (severa)"
        else:
            return "Obesidade Grau 3 (mórbida)"

    def obter_sugestao_treino(self, imc):
        if imc < 18.5:
            return "Treino para ganho de massa muscular leve e alimentação balanceada."
        elif 18.5 <= imc < 24.99:
            return "Manutenção de peso com exercícios regulares e alimentação saudável."
        elif 25 <= imc < 29.99:
            return "Treino para perda de gordura e controle da ingestão calórica."
        elif 30 <= imc < 34.99:
            return "Treino para perda de gordura e fortalecimento cardiovascular."
        elif 35 <= imc < 39.99:
            return "Treino supervisionado para perda de gordura e melhoria cardiovascular."
        else:
            return "Consulte um profissional de saúde para orientação personalizada."

class TreinoPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Escolha o tipo de treino:", font=("Helvetica", 14)).pack(pady=10)

        var_tipo_treino = tk.StringVar()
        radio_ganho_massa = tk.Radiobutton(self, text="Ganho de Massa", variable=var_tipo_treino, value="ganho_massa", font=("Helvetica", 14))
        radio_perda_gordura = tk.Radiobutton(self, text="Perda de Gordura", variable=var_tipo_treino, value="perda_gordura", font=("Helvetica", 14))

        radio_ganho_massa.pack(pady=5)
        radio_perda_gordura.pack(pady=5)

        tk.Button(self, text="Exibir Treino", command=lambda: self.exibir_treino(var_tipo_treino), width=15).pack(pady=10)
        tk.Button(self, text="Voltar ao Menu", command=lambda: controller.show_frame("WelcomePage"), width=15).pack(pady=5)

    def exibir_treino(self, var_tipo_treino):
        tipo_treino = var_tipo_treino.get()
        treino_text = self.obter_treino(tipo_treino)

        if treino_text:
            messagebox.showinfo("Treino", treino_text)
        else:
            messagebox.showwarning("Treino", "Escolha um tipo de treino válido.")

    def obter_treino(self, tipo_treino):
        if tipo_treino == "ganho_massa":
            return """Treino para Ganho de Massa Muscular:

            Segunda - Feira:
            Peito e Tríceps: 15x3 Supino, 10x3 Supino Inclinado com Halteres, 10x3 Crucifixo, 10x3 Tríceps Corda na Polia, 10x3 Tríceps Testa na Barra W, 10x3 Tríceps Francês na Polia.

            Terça - Feira:
            Costas e Bíceps: 10x3 Pulley Frente, 10x3 Remada Unilateral na Máquina, 10x3 Remada Cavalinho, 10x3 Rosca Barra W, 10x3 Rosca Martelo com Halteres.

            Quarta - Feira:
            Ombro: 10x4 Elevação Lateral com Halteres, 10x5 Desenvolvimento com Halteres, 10x3 Elevação Frontal com Halteres.

            Quinta - Feira:
            Perna: 10x3 Agachamento Livre, 10x3 Leg Press, 10x3 Cadeira Flexora, 10x3 Cadeira Extensora, 10x3 Mesa Flexora.

            Sexta - Feira:
            Cardio."""
        elif tipo_treino == "perda_gordura":
            return """Treino para Perda de Gordura:

            Segunda - Feira:
            2 minutos de caminhada, seguido por 2 minutos de corrida (repetir 10 vezes).

            Terça - Feira:
            Perna: 10x2 Agachamento Livre, 10x2 Leg Press, 10x2 Cadeira Extensora. Simulador de Escada por 30 minutos.

            Quarta - Feira:
            Superiores: 10x2 Supino, 10x2 Remada Unilateral, 10x2 Rosca com Barra W, 10x2 Desenvolvimento com Halteres, 10x2 Tríceps na Polia. Simulador de Escada por 30 minutos.

            Quinta - Feira:
            Simulador de Escada por 45 minutos."""
        else:
            return ""

class CronometroPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.tempo_inicial = 0
        self.tempo_decorrido = tk.StringVar()
        self.tempo_decorrido.set("00:00")

        label_tempo = tk.Label(self, textvariable=self.tempo_decorrido, font=("Helvetica", 24))
        label_tempo.pack(pady=10)

        btn_iniciar = tk.Button(self, text="Iniciar", command=self.iniciar_cronometro, width=15)
        btn_parar = tk.Button(self, text="Parar", command=self.parar_cronometro, width=15)
        btn_resetar = tk.Button(self, text="Resetar", command=self.resetar_cronometro, width=15)
        btn_voltar = tk.Button(self, text="Voltar ao Menu", command=lambda: controller.show_frame("WelcomePage"), width=15)

        btn_iniciar.pack(pady=5)
        btn_parar.pack(pady=5)
        btn_resetar.pack(pady=5)
        btn_voltar.pack(pady=5)

        self.atualizar_tempo()

    def iniciar_cronometro(self):
        if self.tempo_inicial == 0:
            self.tempo_inicial = time.time() - int(self.tempo_decorrido.get()[:2]) * 60 - int(self.tempo_decorrido.get()[3:])
            self.atualizar_tempo()

    def parar_cronometro(self):
        if self.tempo_inicial != 0:
            self.tempo_decorrido.set(self.formatar_tempo(time.time() - self.tempo_inicial))
            self.tempo_inicial = 0

    def resetar_cronometro(self):
        self.tempo_inicial = 0
        self.tempo_decorrido.set("00:00")

    def atualizar_tempo(self):
        if self.tempo_inicial != 0:
            tempo_decorrido = time.time() - self.tempo_inicial
            self.tempo_decorrido.set(self.formatar_tempo(tempo_decorrido))
            self.after(1000, self.atualizar_tempo)

    def formatar_tempo(self, segundos):
        minutos = int(segundos // 60)
        segundos = int(segundos % 60)
        return f"{minutos:02d}:{segundos:02d}"

if __name__ == "__main__":
    app = AppFitness()
    app.mainloop()
