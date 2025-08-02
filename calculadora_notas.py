import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import csv
import json
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

USUARIOS_FILE = "usuarios.json"
HISTORICO_FILE_TEMPLATE = "historico_{}.json"

CORES_STATUS = {
    "Excluído": "#f28b82",
    "Aprovado": "#ccffcc",
    "Dispensado": "#fff2b2"
}

# Funções utilitárias para persistência

def carregar_usuarios():
    if os.path.exists(USUARIOS_FILE):
        with open(USUARIOS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    # Usuários padrão se arquivo não existir
    return {
        "joao": "1234",
        "maria": "abcd",
        "ana": "2024",
        "carlos": "senha"
    }

def salvar_usuarios(usuarios):
    with open(USUARIOS_FILE, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, ensure_ascii=False, indent=2)

def carregar_historico(usuario):
    fname = HISTORICO_FILE_TEMPLATE.format(usuario)
    if os.path.exists(fname):
        with open(fname, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_historico(usuario, historico):
    fname = HISTORICO_FILE_TEMPLATE.format(usuario)
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=2)

class CalculadoraNotasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EzMedia")
        self.root.geometry("750x540")
        self.root.resizable(False, False)
        self.usuarios = carregar_usuarios()  # {usuario: senha}
        self.usuario_logado = None
        self.historico = []  # [{disciplina, notas, media, status}]
        self._tela_login()

    def _tela_login(self):
        self._limpar_tela()
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)
        tk.Label(frame, text="Login", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        tk.Label(frame, text="Nome:").grid(row=1, column=0, sticky="e", pady=5)
        tk.Label(frame, text="Senha:").grid(row=2, column=0, sticky="e", pady=5)
        self.entry_nome = tk.Entry(frame)
        self.entry_nome.grid(row=1, column=1, pady=5)
        self.entry_senha = tk.Entry(frame, show="*")
        self.entry_senha.grid(row=2, column=1, pady=5)
        btn_login = tk.Button(frame, text="Entrar", width=15, command=self._login)
        btn_login.grid(row=3, column=0, columnspan=2, pady=10)
        btn_cadastrar = tk.Button(frame, text="Cadastrar", width=15, command=self._abrir_cadastro)
        btn_cadastrar.grid(row=4, column=0, columnspan=2, pady=5)
        self.root.bind('<Return>', lambda event: self._login())

    def _abrir_cadastro(self):
        def cadastrar():
            nome = entry_nome.get().strip().lower()
            senha = entry_senha.get().strip()
            if not nome or not senha:
                messagebox.showerror("Erro", "Preencha nome e senha.")
                return
            if nome in self.usuarios:
                messagebox.showerror("Erro", "Usuário já existe.")
                return
            self.usuarios[nome] = senha
            salvar_usuarios(self.usuarios)
            messagebox.showinfo("Cadastro", "Usuário cadastrado com sucesso!")
            win.destroy()
        win = tk.Toplevel(self.root)
        win.title("Cadastro de Usuário")
        win.geometry("300x180")
        win.resizable(False, False)
        tk.Label(win, text="Nome:").pack(pady=8)
        entry_nome = tk.Entry(win)
        entry_nome.pack()
        tk.Label(win, text="Senha:").pack(pady=8)
        entry_senha = tk.Entry(win, show="*")
        entry_senha.pack()
        btn = tk.Button(win, text="Cadastrar", width=15, command=cadastrar)
        btn.pack(pady=15)
        entry_nome.focus_set()

    def _login(self):
        nome = self.entry_nome.get().strip().lower()
        senha = self.entry_senha.get().strip()
        if nome in self.usuarios and self.usuarios[nome] == senha:
            self.usuario_logado = nome
            self.historico = carregar_historico(nome)
            self._tela_principal()
        else:
            messagebox.showerror("Erro de Login", "Nome ou senha incorretos.")

    def _tela_principal(self):
        self._limpar_tela()
        # Topo com nome do aluno
        topo = tk.Frame(self.root, pady=10)
        topo.pack(fill="x")
        tk.Label(topo, text=f"Aluno: {self.usuario_logado.capitalize()}", font=("Arial", 14, "bold")).pack(side="left", padx=20)
        btn_logout = tk.Button(topo, text="Sair", command=self._logout)
        btn_logout.pack(side="right", padx=20)
        btn_historico = tk.Button(topo, text="Histórico", command=self._mostrar_historico)
        btn_historico.pack(side="right", padx=10)

        # Frame de entrada de dados
        frame = tk.LabelFrame(self.root, text="Adicionar Disciplina", padx=10, pady=10)
        frame.pack(padx=20, pady=10, fill="x")
        tk.Label(frame, text="Disciplina:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_disciplina = tk.Entry(frame, width=20)
        self.entry_disciplina.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(frame, text="Nota 1:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_n1 = tk.Entry(frame, width=5)
        self.entry_n1.grid(row=0, column=3, padx=5, pady=5)
        tk.Label(frame, text="Nota 2:").grid(row=0, column=4, padx=5, pady=5)
        self.entry_n2 = tk.Entry(frame, width=5)
        self.entry_n2.grid(row=0, column=5, padx=5, pady=5)
        tk.Label(frame, text="Trabalho:").grid(row=0, column=6, padx=5, pady=5)
        self.entry_trab = tk.Entry(frame, width=5)
        self.entry_trab.grid(row=0, column=7, padx=5, pady=5)
        tk.Label(frame, text="Projeto:").grid(row=0, column=8, padx=5, pady=5)
        self.entry_proj = tk.Entry(frame, width=5)
        self.entry_proj.grid(row=0, column=9, padx=5, pady=5)
        btn_add = tk.Button(frame, text="Adicionar", width=12, command=self._adicionar_disciplina)
        btn_add.grid(row=0, column=10, padx=10)

        # Tabela Treeview
        tabela_frame = tk.Frame(self.root)
        tabela_frame.pack(padx=20, pady=10, fill="both", expand=True)
        colunas = ("Disciplina", "Nota 1", "Nota 2", "Trabalho", "Projeto", "Média", "Status")
        self.tree = ttk.Treeview(tabela_frame, columns=colunas, show="headings", height=10)
        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=90)
        self.tree.pack(side="left", fill="both", expand=True)
        self._atualizar_tabela()
        # Scrollbar
        scrollbar = ttk.Scrollbar(tabela_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Botão exportar CSV
        btn_exportar = tk.Button(self.root, text="Exportar para CSV", width=20, command=self._exportar_csv)
        btn_exportar.pack(pady=5)
        # Botão exportar PDF
        btn_exportar_pdf = tk.Button(self.root, text="Exportar para PDF", width=20, command=self._exportar_pdf)
        btn_exportar_pdf.pack(pady=5)

    def _adicionar_disciplina(self):
        nome_disc = self.entry_disciplina.get().strip()
        notas = []
        for entry in [self.entry_n1, self.entry_n2, self.entry_trab, self.entry_proj]:
            valor = entry.get().replace(",", ".").strip()
            if valor == "":
                notas.append(None)
            else:
                try:
                    notas.append(float(valor))
                except ValueError:
                    messagebox.showerror("Erro", "Notas devem ser números válidos.")
                    return
        if not nome_disc:
            messagebox.showerror("Erro", "Informe o nome da disciplina.")
            return
        notas_preenchidas = [n for n in notas if n is not None]
        if len(notas_preenchidas) < 3:
            messagebox.showerror("Erro", "Preencha pelo menos 3 notas.")
            return
        media = sum(notas_preenchidas) / len(notas_preenchidas)
        if media < 9.5:
            status = "Excluído"
        elif media < 13.5:
            status = "Aprovado"
        else:
            status = "Dispensado"
        # Salva os dados
        self.historico.append({
            "disciplina": nome_disc,
            "notas": notas,
            "media": media,
            "status": status
        })
        salvar_historico(self.usuario_logado, self.historico)
        self._limpar_campos_disciplina()
        self._atualizar_tabela()

    def _atualizar_tabela(self):
        # Limpa tabela
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Insere dados
        for dado in self.historico:
            notas_fmt = [f"{n:.2f}" if n is not None else "" for n in dado["notas"]]
            media_fmt = f"{dado['media']:.2f}"
            status = dado["status"]
            item_id = self.tree.insert("", "end", values=(dado["disciplina"], *notas_fmt, media_fmt, status))
            self.tree.item(item_id, tags=(status,))
        # Configura cores
        for status, cor in CORES_STATUS.items():
            self.tree.tag_configure(status, background=cor)

    def _limpar_campos_disciplina(self):
        self.entry_disciplina.delete(0, tk.END)
        self.entry_n1.delete(0, tk.END)
        self.entry_n2.delete(0, tk.END)
        self.entry_trab.delete(0, tk.END)
        self.entry_proj.delete(0, tk.END)

    def _exportar_csv(self):
        dados = self.historico
        if not dados:
            messagebox.showinfo("Exportação", "Nenhuma disciplina para exportar.")
            return
        nome_arquivo = f"{self.usuario_logado}_notas.csv"
        try:
            with open(nome_arquivo, mode="w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Disciplina", "Nota 1", "Nota 2", "Trabalho", "Projeto", "Média", "Status"])
                for dado in dados:
                    notas_fmt = [f"{n:.2f}" if n is not None else "" for n in dado["notas"]]
                    writer.writerow([dado["disciplina"], *notas_fmt, f"{dado['media']:.2f}", dado["status"]])
            messagebox.showinfo("Exportação", f"Dados exportados para {nome_arquivo}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar: {e}")

    def _exportar_pdf(self):
        dados = self.historico
        if not dados:
            messagebox.showinfo("Exportação", "Nenhuma disciplina para exportar.")
            return
        nome_arquivo = f"{self.usuario_logado}_notas.pdf"
        try:
            doc = SimpleDocTemplate(nome_arquivo, pagesize=A4)
            styles = getSampleStyleSheet()
            elementos = []
            titulo = Paragraph(f"<b>EzMedia - Notas do Aluno: {self.usuario_logado.capitalize()}</b>", styles['Title'])
            elementos.append(titulo)
            elementos.append(Spacer(1, 18))
            # Cabeçalho e dados
            cabecalho = ["Disciplina", "Nota 1", "Nota 2", "Trabalho", "Projeto", "Média", "Status"]
            tabela_dados = [cabecalho]
            for dado in dados:
                notas_fmt = [f"{n:.2f}" if n is not None else "" for n in dado["notas"]]
                media_fmt = f"{dado['media']:.2f}"
                status = dado["status"]
                tabela_dados.append([dado["disciplina"], *notas_fmt, media_fmt, status])
            # Cria tabela
            t = Table(tabela_dados, repeatRows=1)
            estilo = TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
                ('TEXTCOLOR', (0,0), (-1,0), colors.black),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,-1), 10),
                ('BOTTOMPADDING', (0,0), (-1,0), 8),
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ])
            # Cores por status
            for i, dado in enumerate(dados, start=1):
                cor = None
                if dado["status"] == "Excluído":
                    cor = colors.HexColor("#f28b82")
                elif dado["status"] == "Aprovado":
                    cor = colors.HexColor("#ccffcc")
                elif dado["status"] == "Dispensado":
                    cor = colors.HexColor("#fff2b2")
                if cor:
                    estilo.add('BACKGROUND', (0,i), (-1,i), cor)
            t.setStyle(estilo)
            elementos.append(t)
            doc.build(elementos)
            messagebox.showinfo("Exportação", f"PDF exportado para {nome_arquivo}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar PDF: {e}")

    def _mostrar_historico(self):
        win = tk.Toplevel(self.root)
        win.title("Histórico de Disciplinas")
        win.geometry("700x400")
        colunas = ("Disciplina", "Nota 1", "Nota 2", "Trabalho", "Projeto", "Média", "Status")
        tree = ttk.Treeview(win, columns=colunas, show="headings", height=15)
        for col in colunas:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=90)
        tree.pack(side="left", fill="both", expand=True)
        # Scrollbar
        scrollbar = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        # Preenche histórico
        for dado in self.historico:
            notas_fmt = [f"{n:.2f}" if n is not None else "" for n in dado["notas"]]
            media_fmt = f"{dado['media']:.2f}"
            status = dado["status"]
            item_id = tree.insert("", "end", values=(dado["disciplina"], *notas_fmt, media_fmt, status))
            tree.item(item_id, tags=(status,))
        for status, cor in CORES_STATUS.items():
            tree.tag_configure(status, background=cor)

    def _logout(self):
        self.usuario_logado = None
        self.historico = []
        self._tela_login()

    def _limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraNotasApp(root)
    root.mainloop()
