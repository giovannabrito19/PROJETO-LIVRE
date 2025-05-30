from flask import Flask, render_template, request, flash, redirect, url_for
from package.models import Paciente, Medico, Consulta, Especialidade, Cartao, Dinheiro, Pix
from package.persistencia import (
    salvar_pacientes, salvar_medicos, salvar_especialidades, salvar_consultas,
    carregar_dados
)
from package.utilitarios import encontrar_paciente, encontrar_medico

app = Flask(__name__)
app.secret_key = 'chave_secreta'

consultas, pacientes, medicos, especialidades = carregar_dados()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/paciente/novo', methods=['GET', 'POST'])
def cadastrar_paciente():
    global pacientes

    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        idade = int(request.form['idade'])
        plano = request.form.get('plano_saude', '')
        paciente = Paciente(nome, cpf, telefone, idade, plano)
        pacientes.append(paciente)
        salvar_pacientes(pacientes)
        flash('Paciente cadastrado com sucesso!')
        return redirect(url_for('index'))
    return render_template('cadastrar_paciente.html')

@app.route('/medico/novo', methods=['GET', 'POST'])
def cadastrar_medico():
    global medicos, especialidades

    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        idade = int(request.form['idade'])
        crm = request.form['crm']
        nome_esp = request.form['nome_esp']

        especialidade = next((e for e in especialidades if e.nome.lower() == nome_esp.lower()), None)
        if not especialidade:
            especialidade = Especialidade(nome_esp)
            especialidades.append(especialidade)
            _, _, medicos, especialidades = carregar_dados()

        medico = Medico(nome, cpf, telefone, idade, crm, especialidade)
        medicos.append(medico)

        salvar_medicos(medicos)
        salvar_especialidades(especialidades)
        flash('Médico cadastrado com sucesso!')
        return redirect(url_for('index'))
       
    return render_template('cadastrar_medicos.html')

@app.route('/agendar/consulta', methods=['GET', 'POST'])
def agendar_consulta():
    if request.method == 'POST':
        data_hora = request.form['data_hora']
        nome_paciente = request.form['paciente']
        nome_medico = request.form['medico']

        paciente = encontrar_paciente(nome_paciente, pacientes)
        medico = encontrar_medico(nome_medico, medicos)

        if paciente and medico:
            consulta = Consulta(data_hora, paciente, medico, "Agendada")
            consulta.agendar()
            consultas.append(consulta)



            salvar_consultas(consultas)
        flash('Consulta agendada com sucesso!')
        return redirect(url_for('index'))
    
    return render_template('agendar_consulta.html')

@app.route("/consultas")
def listar_consultas():
    consultas, _, _, _ = carregar_dados()
    return render_template("consultas.html", consultas=consultas)

@app.route("/consultas/cancelar/<int:consulta_id>")
def cancelar_consulta(consulta_id):
    consultas, _, _, _ = carregar_dados()

    if 0 <= consulta_id < len(consultas):
        consulta = consultas[consulta_id]
        consulta.cancelar_consulta()
        salvar_consultas(consultas)

    return redirect(url_for("listar_consultas"))

@app.route("/consultas/finalizar/<int:consulta_id>")
def finalizar_consulta(consulta_id):
    consultas, _, _, _ = carregar_dados()

    if 0 <= consulta_id < len(consultas):
        consulta = consultas[consulta_id]
        consulta.finalizar_consulta()
        salvar_consultas(consultas)

    return redirect(url_for("listar_consultas"))

@app.route("/pagamentos", methods=["GET", "POST"])
def pagamento():
    global consultas
    if request.method == "POST":
        try:
            indice = int(request.form["consulta"])
            valor = float(request.form["valor"])
            data = request.form["data"]
            tipo = request.form["tipo"]
            consulta = consultas[indice]

            if tipo == "cartao":
                numero = request.form["numero"]
                pgto = Cartao(valor, data, consulta, numero)
            elif tipo == "dinheiro":
                pgto = Dinheiro(valor, data, consulta)
            elif tipo == "pix":
                chave = request.form["chave"]
                pgto = Pix(valor, data, consulta, chave)
            else:
                flash("Tipo de pagamento inválido.", "erro")
                return redirect(url_for("pagamento"))

            pgto.processar_pagamento()
            salvar_consultas(consultas)
            flash("Pagamento realizado com sucesso!", "sucesso")
            return redirect(url_for("index"))

        except Exception as e:
            flash(f"Erro no pagamento: {str(e)}", "erro")
            return redirect(url_for("pagamento"))

    return render_template("pagar_consulta.html", consultas=consultas)

@app.route("/pacientes")
def listar_pacientes():
    return render_template("listar_pacientes.html", pacientes=pacientes)

@app.route("/editar_paciente/<int:idx>", methods=["GET", "POST"])
def editar_paciente(idx):
    if 0 <= idx < len(pacientes):
        paciente = pacientes[idx]

        if request.method == "POST":
            campo = request.form.get("campo")
            valor = request.form.get("valor")

            if campo == "nome":
                paciente.nome = valor
            elif campo == "cpf":
                paciente.cpf = valor
            elif campo == "telefone":
                paciente.telefone = valor
            elif campo == "idade":
                paciente.idade = int(valor)
            elif campo == "plano_saude":
                paciente.plano_saude = valor

            salvar_pacientes(pacientes)
            return redirect(url_for("listar_pacientes"))

        return render_template("editar_paciente.html", paciente=paciente, idx=idx)
    
    return "Paciente não encontrado", 404

@app.route("/medicos")
def listar_medicos():
    return render_template("listar_medicos.html", medicos=medicos)

@app.route("/editar_medico/<int:idx>", methods=["GET", "POST"])
def editar_medico(idx):
    if 0<= idx < len(medicos):
        medico = medicos[idx]

        if request.method == "POST":
            campo = request.form.get("campo")
            valor = request.form.get("valor")

            if campo=="nome":
                medico.nome = valor
            elif campo == "cpf":
                medico.cpf = valor
            elif campo == "telefone":
                medico.telefone = valor
            elif campo == "idade":
                medico.idade = valor
            elif campo == "crm":
                medico.crm = valor 
            elif campo == "especialidade":
                especialidade_antiga = medico.especialidade
                nome_nova = valor.strip()

                existente = next((e for e in especialidades if e.nome.lower() == nome_nova.lower()), None)
                if existente:
                    medico.especialidade = existente
                else:
                    nova = Especialidade(nome_nova)
                    especialidades.append(nova)
                    medico.especialidade = nova

                ainda_usada = any(m.especialidade.nome == especialidade_antiga.nome for m in medicos if m != medico)
                if not ainda_usada:
                    especialidades.remove(especialidade_antiga)

            salvar_medicos(medicos)
            salvar_especialidades(especialidades)

            return redirect(url_for("listar_medicos"))

        return render_template("editar_medicos.html", medico=medico, idx=idx)

    return "Médico não encontrado", 404
 

if __name__ == '__main__':
    app.run(debug=True)

