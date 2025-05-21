from package.models import Paciente, Medico, Consulta, Especialidade, Cartao, Dinheiro, Pix
from package.persistencia import (
    salvar_pacientes, carregar_pacientes,
    salvar_medicos, salvar_especialidades,
    salvar_consultas, carregar_consultas,
    carregar_dados
)
from package.utilitarios import encontrar_paciente, encontrar_medico
from time import sleep

def input_int(msg):
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("Digite um número válido!")

def input_float(msg):
    while True:
        try:
            return float(input(msg))
        except ValueError:
            print("Digite um valor numérico válido!")


medicos, especialidades = carregar_dados()
pacientes = carregar_pacientes(consultas=[])
consultas = carregar_consultas(pacientes, medicos)

while True:
    print("\n---------- MENU ----------")
    print(" 1 - Cadastrar paciente")
    print(" 2 - Cadastrar médico")
    print(" 3 - Agendar consulta")
    print(" 4 - Cancelar consulta")
    print(" 5 - Finalizar consulta")
    print(" 6 - Exibir consultas")
    print(" 7 - Exibir médicos")
    print(" 8 - Pagamento")
    print(" 9 - Editar paciente")
    print("10 - Editar médico")
    print("11 - Sair")

    escolha = input_int("Escolha uma opção: ")

    if escolha == 1:
        nome = input("Nome: ").strip()
        cpf = input("CPF: ").strip()
        telefone = input("Telefone: ").strip()
        idade = input_int("Idade: ")
        plano = input("Plano de saúde: ").strip()
        paciente = Paciente(nome, cpf, telefone, idade,  plano)
        pacientes.append(paciente)
        salvar_pacientes(pacientes)
        print("Paciente cadastrado com sucesso!")
        sleep(1)

    elif escolha == 2:
        nome = input("Nome: ").strip()
        cpf = input("CPF: ").strip()
        telefone = input("Telefone: ").strip()
        idade = input_int("Idade: ")
        crm = input("CRM: ").strip()
        nome_esp = input("Especialidade do médico: ").strip()

        especialidade = next((e for e in especialidades if e.nome.lower() == nome_esp.lower()), None)
        if not especialidade:
            especialidade = Especialidade(nome_esp)
            especialidades.append(especialidade)

        medico = Medico(nome, cpf, telefone, idade, crm, especialidade)
        medicos.append(medico)
        salvar_medicos(medicos)
        salvar_especialidades(especialidades)
        medicos, especialidades = carregar_dados()
        print("Médico cadastrado com sucesso!")
        sleep(1)

    elif escolha == 3:
        data_hora = input("Data e hora da consulta (HH:MM DD/MM/AA): ").strip()
        nome_paciente = input("Nome do paciente: ").strip()
        nome_medico = input("Nome do médico: ").strip()

        paciente = encontrar_paciente(nome_paciente, pacientes)
        medico = encontrar_medico(nome_medico, medicos)

        if paciente and medico:
            consulta = Consulta(data_hora, paciente, medico, "Agendada")
            consulta.agendar()
            consultas.append(consulta)



            salvar_consultas(consultas)

            print("Consulta agendada com sucesso!")

        else:
            print("Paciente ou médico não encontrado.")
        sleep(1)

    elif escolha == 4:
        if not consultas:
            print("Não há consultas para cancelar.")
            sleep(1)
            continue

        for i, c in enumerate(consultas):
            print(f"{i} - {c.data_hora} | Paciente: {c.paciente.nome} | Médico: {c.medico.nome} | Status: {c.status}")

        op = input_int("Informe o número da consulta a cancelar: ")
        if 0 <= op < len(consultas):
            consulta = consultas[op]
            consulta.cancelar_consulta()
            salvar_consultas(consultas)

            print("Consulta cancelada com sucesso.")
        else:
            print("Número inválido.")
        sleep(1)

    elif escolha == 5:
        if not consultas:
            print("Não há consultas para finalizar.")
            sleep(1)
            continue

        for i, c in enumerate(consultas):
            print(f"{i} - {c.data_hora} | Paciente: {c.paciente.nome} | Médico: {c.medico.nome} | Status: {c.status}")

        op = input_int("Informe o número da consulta a finalizar: ")
        if 0 <= op < len(consultas):
            consulta = consultas[op]
            consulta.finalizar_consulta()
            salvar_consultas(consultas)

            print("Consulta finalizada com sucesso.")
        else:
            print("Número inválido.")
        sleep(1)

    elif escolha == 6:
        if consultas:
            print("Consultas agendadas:")
            for i, c in enumerate(consultas):
                print(f"{i} - {c.data_hora} | Paciente: {c.paciente.nome} | Médico: {c.medico.nome} | Status: {c.status}")
        else:
            print("Nenhuma consulta cadastrada.")
        sleep(1)

    elif escolha == 7:
        if especialidades:
            for esp in especialidades:
                esp.listar_medicos()
        else:
            print("Nenhuma especialidade cadastrada.")
        sleep(1)

    elif escolha == 8:
        if not consultas:
            print("Não há consultas para pagamento.")
            sleep(1)
            continue

        for i, c in enumerate(consultas):
            print(f"{i} - {c.data_hora} | Paciente: {c.paciente.nome} | Médico: {c.medico.nome} | Status: {c.status}")

        op = input_int("Escolha a consulta (número): ")
        if 0 <= op < len(consultas):
            valor = input_float("Valor do pagamento: R$ ")
            data = input("Data do pagamento (DD/MM/AA): ").strip()
            tipo = input("Tipo (cartão/dinheiro/pix): ").strip().lower()

            if tipo == "cartão" or tipo == "cartao":
                numero = input("Número do cartão: ").strip()
                pgto = Cartao(valor, data, consultas[op], numero)
            elif tipo == "dinheiro":
                pgto = Dinheiro(valor, data, consultas[op])
            elif tipo == "pix":
                chave = input("Chave PIX: ").strip()
                pgto = Pix(valor, data, consultas[op], chave)
            else:
                print("Tipo inválido!")
                sleep(1)
                continue

            pgto.processar_pagamento()
            print("Pagamento realizado com sucesso!")
        else:
            print("Número inválido.")
        sleep(1)


    elif escolha == 9:
        for i, p in enumerate(pacientes):
            print(f"{i} - {p.nome}")

        idx = input_int("Escolha o número do paciente que deseja editar: ")
        if 0 <= idx < len(pacientes):
            paciente = pacientes[idx]
            print("Digite a opção que deseja editar:")
            print(f"1 - Nome: {paciente.nome}")
            print(f"2 - CPF: {paciente.cpf}")
            print(f"3 - Telefone: {paciente.telefone}")
            print(f"4 - Idade: {paciente.idade}")
            print(f"5 - Plano de Saúde: {paciente.plano_saude}")

            num = input_int("Opção: ")

            if num == 1:
                paciente.nome = input("Digite o novo nome do paciente: ")
            elif num == 2:
                paciente.cpf = input("Digite o novo CPF do paciente: ")
            elif num == 3:
                paciente.telefone = input("Digite o novo telefone do paciente: ")
            elif num == 4:
                paciente.idade = input_int("Digite a nova idade do paciente: ")
            elif num == 5:
                paciente.plano_saude = input("Digite o novo plano de saúde do paciente: ")
            else:
                print("Opção inválida.")


            salvar_pacientes(pacientes)
            print("Editado com sucesso!")
            sleep(1)

        else:
            print("Índice inválido.")
            sleep(1)


    elif escolha == 10:

        for i, m in enumerate(medicos):
            print(f"{i} - {m.nome}")

        idx = input_int("Escolha o número do médico que deseja editar: ")
        if 0 <= idx < len(medicos):
            medico = medicos[idx]
            print("Digite a opção que deseja editar:")
            print(f"1 - Nome: {medico.nome}")
            print(f"2 - CPF: {medico.cpf}")
            print(f"3 - Telefone: {medico.telefone}")
            print(f"4 - Idade: {medico.idade}")
            print(f"5 - CRM: {medico.crm}")
            print(f"6 - Especialidade: {medico.especialidade.nome}")

            num = input_int("Opção: ")

            if num == 1:
                medico.nome = input("Digite o novo nome do médico: ")
            elif num == 2:
                medico.cpf = input("Digite o novo CPF do médico: ")
            elif num == 3:
                medico.telefone = input("Digite o novo telefone do médico: ")
            elif num == 4:
                medico.idade = input_int("Digite a nova idade do médico: ")
            elif num == 5:
                medico.crm = input("Digite o novo CRM do médico: ")
            elif num == 6:
                especialidade_antiga = medico.especialidade
                nome_nova = input("Digite o nome da nova especialidade: ").strip()


                existente = next((e for e in especialidades if e.nome.lower() == nome_nova.lower()), None)
                if existente:
                    medico.especialidade = existente
                else:
                    nova_esp = Especialidade(nome_nova)
                    especialidades.append(nova_esp)
                    medico.especialidade = nova_esp

                ainda_usada = any(m.especialidade.nome == especialidade_antiga.nome for m in medicos if m != medico)
                if not ainda_usada:
                    especialidades.remove(especialidade_antiga)

            else:
                print("Opção inválida.")
                sleep(1)


            salvar_medicos(medicos)
            salvar_especialidades(especialidades)
            medicos, especialidades = carregar_dados()

            print("Editado com sucesso!")
            sleep(1)


        else:
            print("Índice inválido.")
            sleep(1)

    elif escolha == 11:
        print("Encerrando sistema...")
        break

    else:
        print("Opção inválida.")
        sleep(1)



