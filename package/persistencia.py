import json
from .models import Paciente, Medico, Consulta, Especialidade

def salvar_pacientes(pacientes):
    dados = [p.to_dict() for p in pacientes]
    with open("pacientes.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def carregar_pacientes(consultas):
    try:
        with open("pacientes.json", "r", encoding="utf-8") as f:
            dados = json.load(f)
            return [Paciente.from_dict(p, consultas) for p in dados]
    except FileNotFoundError:
        return []


def salvar_medicos(medicos):
    dados = [m.to_dict() for m in medicos]
    with open("medicos.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def carregar_medicos(especialidades):
    try:
        with open("medicos.json", "r", encoding="utf-8") as f:
            dados = json.load(f)
            medicos = []
            for m in dados:
                especialidade_nome = m['especialidade']['nome']
                especialidade = next((e for e in especialidades if e.nome == especialidade_nome), None)
                if not especialidade:
                    especialidade = Especialidade.from_dict(m['especialidade'])
                    especialidades.append(especialidade)

                medico = Medico.from_dict(m, especialidades)  # << passa lista inteira aqui
                if hasattr(especialidade, 'adicionar_medico'):
                    especialidade.adicionar_medico(medico)

                medicos.append(medico)
            return medicos
    except FileNotFoundError:
        return []

def salvar_especialidades(especialidades):
    dados = [e.to_dict() for e in especialidades]
    with open("especialidades.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def carregar_especialidades():
    try:
        with open("especialidades.json", "r", encoding="utf-8") as f:
            dados = json.load(f)
            return [Especialidade.from_dict(e) for e in dados]
    except FileNotFoundError:
        return []

def salvar_consultas(consultas):
    dados = [c.to_dict() for c in consultas]
    with open("consultas.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def carregar_consultas(pacientes, medicos):
    try:
        with open("consultas.json", "r", encoding="utf-8") as f:
            dados = json.load(f)
            consultas = []
            for c in dados:
                paciente = next((p for p in pacientes if p.nome == c['paciente']), None)
                medico = next((m for m in medicos if m.nome == c['medico']), None)
                if paciente and medico:
                    nova = Consulta(c['data_hora'], paciente, medico, c['status'])
                    consultas.append(nova)
            return consultas
    except FileNotFoundError:
        return []

def carregar_dados():
    especialidades = []
    medicos = []

    try:
        with open('especialidades.json', 'r', encoding='utf-8') as f:
            lista_esps = json.load(f)
            for esp_data in lista_esps:
                especialidade = Especialidade.from_dict(esp_data)
                especialidades.append(especialidade)
    except FileNotFoundError:
        pass

    try:
        with open('medicos.json', 'r', encoding='utf-8') as f:
            lista_meds = json.load(f)
            for med_data in lista_meds:
                medico = Medico.from_dict(med_data, especialidades)
                medicos.append(medico)
    except FileNotFoundError:
        pass

    return medicos, especialidades


#Carregamento inicial dos dados
pacientes = carregar_pacientes(consultas=[])
especialidades = carregar_especialidades()
medicos = carregar_medicos(especialidades)
consultas = carregar_consultas(pacientes, medicos)

def carregar_dados():
    especialidades = carregar_especialidades()
    medicos = carregar_medicos(especialidades)
    pacientes = carregar_pacientes([])  # consultas ainda não carregadas
    consultas = carregar_consultas(pacientes, medicos)
    return consultas, pacientes, medicos, especialidades

