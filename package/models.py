import json
class Pessoa:
    def __init__(self, nome, cpf, telefone, idade):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.idade = idade

    def exibir_dados(self):
        print(f'Nome: {self.nome}')
        print(f'CPF: {self.cpf}')
        print(f'Telefone: {self.telefone}')


class Consulta:
    def __init__(self, data_hora, paciente, medico, status):
        self.data_hora = data_hora
        self.paciente = paciente
        self.medico = medico
        self.status = status

    def agendar(self):
        self.medico.consultas.append(self)

        self.status = "Agendada"

    def cancelar_consulta(self):
        if self in self.medico.consultas:
            self.medico.consultas.remove(self)

        self.status = "Cancelada"

    def finalizar_consulta(self):
        self.status = "Finalizada"

    def to_dict(self):
        return {
            'data_hora': self.data_hora,
            'paciente': self.paciente.nome,
            'medico': self.medico.nome,
            'status': self.status
        }

    @classmethod
    def from_dict(cls, data, pacientes, medicos):
        paciente = next((p for p in pacientes if p.nome == data["paciente"]), None)
        medico = next((m for m in medicos if m.nome == data["medico"]), None)
        if paciente and medico:
            return cls(data["data_hora"], paciente, medico, data["status"])
        return None



class Paciente(Pessoa):
    def __init__(self, nome, cpf, telefone, idade, plano_saude):
        super().__init__(nome, cpf, telefone, idade)

        self.plano_saude = plano_saude

    def infos(self):
        print(f'Nome: {self.nome}')
        print(f'Idade: {self.idade}')
        print(f"Plano de saúde: {self.plano_saude}")


    def to_dict(self):
        return {
            "nome": self.nome,
            "cpf": self.cpf,
            "telefone": self.telefone,
            "idade": self.idade,
            "plano_saude": self.plano_saude,

        }

    @classmethod
    def from_dict(cls, data, consultas):
        return cls(
            data["nome"],
            data["cpf"],
            data["telefone"],
            data["idade"],
            data["plano_saude"]
        )



class Especialidade:
    def __init__(self, nome):
        self.nome = nome
        self.medicos = []

    def adicionar_medico(self, medico):
        if medico not in self.medicos:
            self.medicos.append(medico)


    def listar_medicos(self):
        print(f"Médicos com especialidade em {self.nome}:")
        for medico in self.medicos:
            print(f"- Dr(a). {medico.nome} (CRM: {medico.crm})")
        # print("Médicos cadastrados:")
        # for m in self.medicos:
        #     print(f"- Dr(a). {m.nome} (CRM: {m.crm}) - Especialidade: {m.especialidade.nome}")

    def to_dict(self):
        return {
            "nome": self.nome,
            "medicos": [medico.nome for medico in self.medicos]
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["nome"])


class Medico(Pessoa):
    def __init__(self, nome, cpf, telefone, idade, crm, especialidade):
        super().__init__(nome, cpf, telefone, idade)
        self.crm = crm
        self.especialidade = especialidade
        self.consultas = []

    def listar_consultas(self):
        for consulta in self.consultas:
            print(f"{consulta.data_hora} com {consulta.paciente.nome}")

    def to_dict(self):
        return {
            "nome": self.nome,
            "cpf": self.cpf,
            "telefone": self.telefone,
            "idade": self.idade,
            "crm": self.crm,
            "especialidade": self.especialidade.to_dict()
        }

    @classmethod
    def from_dict(cls, data, especialidades):
        nome_esp = data["especialidade"]["nome"]
        especialidade = next((e for e in especialidades if e.nome == nome_esp), None)
        if not especialidade:
            especialidade = Especialidade(nome_esp)
            especialidades.append(especialidade)
        medico = cls(
            data["nome"],
            data["cpf"],
            data["telefone"],
            data["idade"],
            data["crm"],
            especialidade
        )
        especialidade.adicionar_medico(medico)
        return medico


class Pagamento:
    def __init__(self, valor, data, consulta):
        self.valor = valor
        self.data = data
        self.consulta = consulta


class Cartao(Pagamento):
    def __init__(self, valor, data, consulta, numero_cartao):
        super().__init__(valor, data, consulta)
        self.numero_cartao = numero_cartao

    def processar_pagamento(self):
        print(f"Processando pagamento de R${self.valor:.2f} no cartão ****{self.numero_cartao[-4:]}")


class Dinheiro(Pagamento):
    def processar_pagamento(self):
        print(f"Pagamento de R${self.valor:.2f} em dinheiro realizado na data {self.data}")


class Pix(Pagamento):
    def __init__(self, valor, data, consulta, chave_pix):
        super().__init__(valor, data, consulta)
        self.chave_pix = chave_pix

    def processar_pagamento(self):
        print(f"Pagamento de R${self.valor:.2f} via PIX para {self.chave_pix}")
