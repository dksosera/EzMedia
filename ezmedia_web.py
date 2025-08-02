from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash
import os
import json
import csv
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)
app.secret_key = 'ezmedia_secret_key'

USUARIOS_FILE = "usuarios.json"
HISTORICO_FILE_TEMPLATE = "historico_{}.json"
CORES_STATUS = {
    "Excluído": "#f28b82",
    "Aprovado": "#ccffcc",
    "Dispensado": "#fff2b2"
}

# Utilitários de persistência

def carregar_usuarios():
    if os.path.exists(USUARIOS_FILE):
        with open(USUARIOS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
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

def calcular_media(notas):
    notas_preenchidas = [n for n in notas if n is not None]
    if len(notas_preenchidas) < 3:
        return None
    return sum(notas_preenchidas) / len(notas_preenchidas)

def classificar(media):
    if media is None:
        return "-"
    if media < 9.5:
        return "Excluído"
    elif media < 13.5:
        return "Aprovado"
    else:
        return "Dispensado"

@app.route('/', methods=['GET', 'POST'])
def login():
    if 'usuario' in session:
        return redirect(url_for('principal'))
    erro = None
    if request.method == 'POST':
        nome = request.form['nome'].strip().lower()
        senha = request.form['senha'].strip()
        usuarios = carregar_usuarios()
        if nome in usuarios and usuarios[nome] == senha:
            session['usuario'] = nome
            return redirect(url_for('principal'))
        else:
            erro = 'Nome ou senha incorretos.'
    return render_template('login.html', erro=erro)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    erro = None
    if request.method == 'POST':
        nome = request.form['nome'].strip().lower()
        senha = request.form['senha'].strip()
        usuarios = carregar_usuarios()
        if not nome or not senha:
            erro = 'Preencha nome e senha.'
        elif nome in usuarios:
            erro = 'Usuário já existe.'
        else:
            usuarios[nome] = senha
            salvar_usuarios(usuarios)
            flash('Usuário cadastrado com sucesso!')
            return redirect(url_for('login'))
    return render_template('cadastro.html', erro=erro)

@app.route('/principal', methods=['GET', 'POST'])
def principal():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    usuario = session['usuario']
    historico = carregar_historico(usuario)
    erro = None
    if request.method == 'POST':
        disciplina = request.form['disciplina'].strip()
        notas = []
        for campo in ['nota1', 'nota2', 'trabalho', 'projeto']:
            valor = request.form[campo].replace(",", ".").strip()
            if valor == '':
                notas.append(None)
            else:
                try:
                    notas.append(float(valor))
                except ValueError:
                    erro = 'Notas devem ser números válidos.'
                    break
        if not erro:
            if not disciplina:
                erro = 'Informe o nome da disciplina.'
            elif len([n for n in notas if n is not None]) < 3:
                erro = 'Preencha pelo menos 3 notas.'
            else:
                media = calcular_media(notas)
                status = classificar(media)
                historico.append({
                    'disciplina': disciplina,
                    'notas': notas,
                    'media': media,
                    'status': status
                })
                salvar_historico(usuario, historico)
                return redirect(url_for('principal'))
    return render_template('principal.html', usuario=usuario, historico=historico, erro=erro, cores=CORES_STATUS)

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

@app.route('/exportar_csv')
def exportar_csv():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    usuario = session['usuario']
    historico = carregar_historico(usuario)
    output = BytesIO()
    writer = csv.writer(output)
    writer.writerow(["Disciplina", "Nota 1", "Nota 2", "Trabalho", "Projeto", "Média", "Status"])
    for dado in historico:
        notas_fmt = [f"{n:.2f}" if n is not None else "" for n in dado["notas"]]
        writer.writerow([dado["disciplina"], *notas_fmt, f"{dado['media']:.2f}", dado["status"]])
    output.seek(0)
    return send_file(output, as_attachment=True, download_name=f'{usuario}_notas.csv', mimetype='text/csv')

@app.route('/exportar_pdf')
def exportar_pdf():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    usuario = session['usuario']
    historico = carregar_historico(usuario)
    output = BytesIO()
    doc = SimpleDocTemplate(output, pagesize=A4)
    styles = getSampleStyleSheet()
    elementos = []
    titulo = Paragraph(f"<b>EzMedia - Notas do Aluno: {usuario.capitalize()}</b>", styles['Title'])
    elementos.append(titulo)
    elementos.append(Spacer(1, 18))
    cabecalho = ["Disciplina", "Nota 1", "Nota 2", "Trabalho", "Projeto", "Média", "Status"]
    tabela_dados = [cabecalho]
    for dado in historico:
        notas_fmt = [f"{n:.2f}" if n is not None else "" for n in dado["notas"]]
        media_fmt = f"{dado['media']:.2f}"
        status = dado["status"]
        tabela_dados.append([dado["disciplina"], *notas_fmt, media_fmt, status])
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
    for i, dado in enumerate(historico, start=1):
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
    output.seek(0)
    return send_file(output, as_attachment=True, download_name=f'{usuario}_notas.pdf', mimetype='application/pdf')

@app.route('/excluir_disciplina/<int:index>')
def excluir_disciplina(index):
    if 'usuario' not in session:
        return redirect(url_for('login'))
    usuario = session['usuario']
    historico = carregar_historico(usuario)
    if 0 <= index < len(historico):
        historico.pop(index)
        salvar_historico(usuario, historico)
        flash('Disciplina excluída com sucesso!')
    return redirect(url_for('principal'))

@app.route('/editar_disciplina/<int:index>', methods=['POST'])
def editar_disciplina(index):
    if 'usuario' not in session:
        return '', 401
    usuario = session['usuario']
    historico = carregar_historico(usuario)
    if 0 <= index < len(historico):
        nome = request.form.get('edit_disciplina', '').strip()
        notas = []
        for campo in ['edit_nota1', 'edit_nota2', 'edit_trabalho', 'edit_projeto']:
            valor = request.form.get(campo, '').replace(',', '.').strip()
            if valor == '':
                notas.append(None)
            else:
                try:
                    notas.append(float(valor))
                except ValueError:
                    notas.append(None)
        if nome and len([n for n in notas if n is not None]) >= 3:
            media = calcular_media(notas)
            status = classificar(media)
            historico[index] = {
                'disciplina': nome,
                'notas': notas,
                'media': media,
                'status': status
            }
            salvar_historico(usuario, historico)
    return '', 204

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

if __name__ == '__main__':
    # Crie a pasta templates e adicione os arquivos HTML necessários
    app.run(debug=True)
