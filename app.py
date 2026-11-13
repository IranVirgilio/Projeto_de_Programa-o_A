from flask import Flask, render_template, request, redirect, url_for, flash
from abc import ABC, abstractmethod

app = Flask(__name__)
app.secret_key = "chave_secreta_banco_poo"

class Cliente:
    def __init__(self, nome, cpf, salario, telefone):
        self.nome = nome
        self.cpf = cpf
        self.salario = float(salario)
        self.telefone = telefone


class Conta(ABC):
    def __init__(self, numero, saldo, cliente):
        self.numero = numero
        self._saldo = float(saldo) 
        self._cliente = cliente  
        self._historico_transacoes = []  

        if self._saldo > 0:
            self._historico_transacoes.append(f"Saldo inicial: +R$ {self._saldo:.2f}")

    @property
    def saldo(self):
        return self._saldo
        
    @property
    def cliente(self):
        return self._cliente

    def depositar(self, valor, registrar=True):
        if valor > 0:
            self._saldo += valor
            if registrar:
                self._historico_transacoes.append(f"Depósito: +R$ {valor:.2f}")
            return True
        return False

    def sacar(self, valor, registrar=True):
        if valor > 0 and self._saldo >= valor:
            self._saldo -= valor
            if registrar:
                self._historico_transacoes.append(f"Saque: -R$ {valor:.2f}")
            return True
        return False

    def transferir(self, conta_destino, valor):
        if self.numero == conta_destino.numero:
            return False
        if self.sacar(valor, registrar=False):
            conta_destino.depositar(valor, registrar=False)
            self._historico_transacoes.append(
                f"Transferência para Conta {conta_destino.numero}: -R$ {valor:.2f}"
            )
            conta_destino._historico_transacoes.append(
                f"Transferência da Conta {self.numero}: +R$ {valor:.2f}"
            )
            return True
        return False
        
    def exibir_historico_saldo(self):
        return self._historico_transacoes



class ContaCorrente(Conta):
    def __init__(self, numero, saldo, cliente, taxa_manutencao=15.0):
        super().__init__(numero, saldo, cliente)
        self.tipo = "Corrente"
        self.taxa_manutencao = float(taxa_manutencao)

    def descontar_taxa(self):
        if self._saldo >= self.taxa_manutencao:
            self._saldo -= self.taxa_manutencao
            self._historico_transacoes.append(f"Taxa de Manutenção: -R$ {self.taxa_manutencao:.2f}")
            return True
        return False


class ContaPoupanca(Conta):
    def __init__(self, numero, saldo, cliente, taxa_rendimento=0.05):
        super().__init__(numero, saldo, cliente)
        self.tipo = "Poupança"
        self.taxa_rendimento = float(taxa_rendimento)

    def aplicar_rendimento(self):
        rendimento = self._saldo * self.taxa_rendimento
        self._saldo += rendimento
        self._historico_transacoes.append(f"Rendimento Aplicado: +R$ {rendimento:.2f}")
        return True


class Agencia:
    def __init__(self, nome, numero):
        self.nome = nome
        self.numero = numero
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def buscar_conta(self, numero):
        for conta in self.contas:
            if conta.numero == numero:
                return conta
        return None

    def calcular_patrimonio_total(self):
        return sum(conta.saldo for conta in self.contas)


agencia_unica = Agencia("Agência Central POO", "001")
clientes_cadastrados = []

def buscar_cliente(cpf):
    for cliente in clientes_cadastrados:
        if cliente.cpf == cpf:
            return cliente
    return None

def validar_numero_decimal(texto):
    texto_limpo = texto.strip().replace(",", ".")
    return texto_limpo.replace(".", "", 1).isdigit()


@app.route("/")
def index():
    return render_template("index.html", agencia=agencia_unica, clientes=clientes_cadastrados)

@app.route("/cadastrar_cliente", methods=["GET", "POST"])
def cadastrar_cliente():
    if request.method == "POST":
        nome, cpf = request.form["nome"].strip(), request.form["cpf"].strip()
        salario, telefone = request.form["salario"].strip(), request.form["telefone"].strip()

        if buscar_cliente(cpf):
            flash("CPF já cadastrado!", "erro")
            return redirect(url_for("cadastrar_cliente"))

        if not validar_numero_decimal(salario):
            flash("Salário inválido!", "erro")
            return redirect(url_for("cadastrar_cliente"))

        novo_cliente = Cliente(nome, cpf, float(salario.replace(",", ".")), telefone)
        clientes_cadastrados.append(novo_cliente)
        flash(f"Cliente {nome} cadastrado com sucesso!", "sucesso")
        return redirect(url_for("index"))

    return render_template("cadastrar_cliente.html")

@app.route("/cadastrar_conta", methods=["GET", "POST"])
def cadastrar_conta():
    if not clientes_cadastrados:
        flash("Cadastre um cliente primeiro!", "erro")
        return redirect(url_for("cadastrar_cliente"))

    if request.method == "POST":
        numero, saldo = request.form["numero"].strip(), request.form["saldo"].strip()
        tipo, cpf_cliente = request.form["cpf_cliente"], request.form["cpf_cliente"]

        if agencia_unica.buscar_conta(int(numero)):
            flash("Número de conta já existe!", "erro")
            return redirect(url_for("cadastrar_conta"))

        cliente_encontrado = buscar_cliente(cpf_cliente)
        saldo_float = float(saldo.replace(",", "."))
        numero_int = int(numero)

        if tipo == "Corrente":
            nova_conta = ContaCorrente(numero_int, saldo_float, cliente_encontrado)
        else:
            nova_conta = ContaPoupanca(numero_int, saldo_float, cliente_encontrado)

        agencia_unica.adicionar_conta(nova_conta)
        flash(f"Conta {tipo} criada com sucesso!", "sucesso")
        return redirect(url_for("index"))

    return render_template("cadastrar_conta.html", clientes=clientes_cadastrados)

@app.route("/operacao/<tipo>", methods=["GET", "POST"])
def operacao(tipo):
    if request.method == "POST":
        numero_origem = request.form["numero_origem"].strip()
        valor = float(request.form["valor"].strip().replace(",", "."))
        conta_origem = agencia_unica.buscar_conta(int(numero_origem))

        if not conta_origem:
            flash("Conta não encontrada!", "erro")
            return redirect(url_for("operacao", tipo=tipo))

        if tipo == "depositar" and conta_origem.depositar(valor):
            flash(f"Depósito de R$ {valor:.2f} concluído!", "sucesso")
        elif tipo == "sacar" and conta_origem.sacar(valor):
            flash(f"Saque de R$ {valor:.2f} concluído!", "sucesso")
        elif tipo == "transferir":
            conta_destino = agencia_unica.buscar_conta(int(request.form["numero_destino"].strip()))
            if conta_origem.transferir(conta_destino, valor):
                flash("Transferência concluída!", "sucesso")
            else:
                flash("Falha na transferência. Verifique os saldos ou se a conta é a mesma.", "erro")
        else:
            flash("Operação falhou. Saldo insuficiente ou valor inválido.", "erro")

        return redirect(url_for("index"))

    return render_template("operacao.html", tipo=tipo)

@app.route("/extrato/<int:numero>")
def extrato(numero):
    conta = agencia_unica.buscar_conta(numero)
    # Mostramos o extrato aproveitando o novo método exigido
    historico = conta.exibir_historico_saldo() 
    return render_template("extrato.html", conta=conta, historico=historico)

if __name__ == "__main__":
    app.run(debug=True)