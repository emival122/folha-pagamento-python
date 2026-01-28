import os
import locale
from tkinter import *
from tkinter import messagebox, ttk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle

# ================= CONFIGURAÇÕES =================
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except:
    pass

COR_PRIMARIA = "#1A3366"
COR_SECUNDARIA = "#F4F7FA"
COR_TEXTO = "#2C3E50"
COR_ACENTO = "#27AE60"


def moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ================= ÍCONE =================


def adicionar_icone(root):
    try:
        caminho = os.path.join(os.path.dirname(__file__), "icon.png")
        icon = PhotoImage(file=caminho)
        root.iconphoto(True, icon)
    except:
        pass

# ================= CÁLCULOS =================


def calcular_inss(salario):
    faixas = [
        (1412.00, 0.075),
        (2666.68, 0.09),
        (4000.03, 0.12),
        (7786.02, 0.14)
    ]
    desconto = 0
    limite_anterior = 0

    if salario <= 0:
        return 0

    for limite, aliquota in faixas:
        if salario > limite:
            desconto += (limite - limite_anterior) * aliquota
            limite_anterior = limite
        else:
            desconto += (salario - limite_anterior) * aliquota
            return round(desconto, 2)
    return 908.85


def calcular_irrf(base):
    if base <= 2259.20:
        return 0
    elif base <= 2826.65:
        return (base * 0.075) - 169.44
    elif base <= 3751.05:
        return (base * 0.15) - 381.44
    elif base <= 4664.68:
        return (base * 0.225) - 662.77
    else:
        return (base * 0.275) - 896.00


def calcular_horas_extra(salario, horas):
    if salario <= 0 or horas <= 0:
        return 0
    return horas * ((salario / 220) * 1.5)

# ================= DADOS =================


def obter_dados():
    try:
        sal = e_salario.get().replace('R$', '').replace(
            '.', '').replace(',', '.').strip()
        horas = e_horas.get().replace(',', '.').strip()

        return {
            "nome": e_nome.get().strip(),
            "cpf": e_cpf.get().strip(),
            "cargo": e_cargo.get().strip(),
            "salario": float(sal or 0),
            "horas": float(horas or 0)
        }
    except ValueError:
        messagebox.showerror("Erro", "Use apenas números em salário e horas.")
        return None


def atualizar_resumo():
    d = obter_dados()
    if not d:
        return

    h = calcular_horas_extra(d['salario'], d['horas'])
    inss = calcular_inss(d['salario'])
    base_irrf = (d['salario'] + h) - inss
    irrf = max(0, calcular_irrf(base_irrf))
    total = (d['salario'] + h) - inss - irrf

    lbl_salario.config(text=moeda(d['salario']))
    lbl_horas.config(text=moeda(h))
    lbl_inss.config(text=f"- {moeda(inss)}", fg="#E74C3C")
    lbl_irrf.config(text=f"- {moeda(irrf)}", fg="#E74C3C")
    lbl_final.config(text=moeda(total), fg=COR_ACENTO)

# ================= PDF =================


def gerar_pdf():
    d = obter_dados()
    if not d:
        return

    if not d['nome'] or not d['cpf'] or not d['cargo']:
        messagebox.showwarning(
            "Atenção", "Preencha todos os campos obrigatórios.")
        return

    h = calcular_horas_extra(d['salario'], d['horas'])
    inss = calcular_inss(d['salario'])
    base_irrf = (d['salario'] + h) - inss
    irrf = max(0, calcular_irrf(base_irrf))
    total = (d['salario'] + h) - inss - irrf

    nome_arquivo = f"Holerite_{d['nome'].replace(' ', '_')}.pdf"
    c = canvas.Canvas(nome_arquivo, pagesize=letter)

    c.setFillColor(COR_PRIMARIA)
    c.rect(0, 700, 612, 112, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, 750, "PRIME SYSTEMS - PAYROLL")

    c.setFillColor(COR_TEXTO)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, 670, f"COLABORADOR: {d['nome'].upper()}")

    c.save()
    messagebox.showinfo("Sucesso", "PDF gerado com sucesso!")


# ================= INTERFACE =================
root = Tk()
root.title("PrimeSystems - Folha de Pagamento")
root.geometry("1100x650")
root.configure(bg=COR_SECUNDARIA)

adicionar_icone(root)

header = Frame(root, bg=COR_PRIMARIA, height=100)
header.pack(fill="x")
Label(header, text="Payroll Pro System", bg=COR_PRIMARIA,
      fg="white", font=("Helvetica", 27, "bold")).pack(pady=30)

main = Frame(root, bg=COR_SECUNDARIA)
main.pack(fill="both", expand=True, padx=40, pady=15)
main.columnconfigure(0, weight=3)
main.columnconfigure(1, weight=1)

f_inputs = LabelFrame(main, text=" Cadastro do Colaborador ", bg=COR_SECUNDARIA,
                      font=("Helvetica", 14, "bold"), padx=30, pady=30)
f_inputs.grid(row=0, column=0, sticky="nsew", padx=(0, 20))

labels = ["Nome:", "CPF:", "Cargo:", "Salário Bruto:", "Horas Extras:"]
entries = []

for i, text_label in enumerate(labels):
    Label(f_inputs, text=text_label, bg=COR_SECUNDARIA,
          font=("Helvetica", 12)).grid(row=i, column=0, sticky="w", pady=10)
    e = Entry(f_inputs, font=("Helvetica", 14))
    e.grid(row=i, column=1, pady=10, sticky="ew")
    entries.append(e)

f_inputs.columnconfigure(1, weight=1)
e_nome, e_cpf, e_cargo, e_salario, e_horas = entries

f_resumo = LabelFrame(main, text=" Resumo ", bg="white",
                      font=("Helvetica", 14, "bold"), padx=30, pady=30)
f_resumo.grid(row=0, column=1, sticky="nsew")

lbl_salario = Label(f_resumo, text="R$ 0,00",
                    bg="white", font=("Helvetica", 13))
lbl_horas = Label(f_resumo, text="R$ 0,00", bg="white", font=("Helvetica", 13))
lbl_inss = Label(f_resumo, text="R$ 0,00", bg="white", font=("Helvetica", 13))
lbl_irrf = Label(f_resumo, text="R$ 0,00", bg="white", font=("Helvetica", 13))
lbl_final = Label(f_resumo, text="R$ 0,00", bg="white",
                  font=("Helvetica", 22, "bold"), fg=COR_ACENTO)

res = [("Bruto:", lbl_salario), ("Extras:", lbl_horas),
       ("INSS:", lbl_inss), ("IRRF:", lbl_irrf)]

for i, (txt, lbl) in enumerate(res):
    Label(f_resumo, text=txt, bg="white",
          font=("Helvetica", 12)).grid(row=i, column=0, sticky="w", pady=8)
    lbl.grid(row=i, column=1, sticky="e")

ttk.Separator(f_resumo, orient="horizontal").grid(
    row=4, column=0, columnspan=2, sticky="ew", pady=15)

Label(f_resumo, text="LÍQUIDO:", bg="white",
      font=("Helvetica", 14, "bold")).grid(row=5, column=0, sticky="w")
lbl_final.grid(row=5, column=1, sticky="e")

f_btns = Frame(root, bg=COR_SECUNDARIA)
f_btns.pack(pady=15)

Button(f_btns, text="CALCULAR", command=atualizar_resumo, bg=COR_ACENTO,
       fg="white", font=("Helvetica", 12, "bold"),
       width=25, height=2).pack(side="left", padx=20)

Button(f_btns, text="GERAR PDF", command=gerar_pdf, bg=COR_PRIMARIA,
       fg="white", font=("Helvetica", 12, "bold"),
       width=25, height=2).pack(side="left", padx=20)

root.mainloop()
