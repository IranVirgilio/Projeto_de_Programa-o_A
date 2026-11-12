from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "chave_secreta_para_alertas" # Necessário para exibir mensagens de erro/sucesso


class Cliente:
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf

class Conta:
    def __init__(self, id_conta, saldo_inicial):
        self.id = id_conta
        self.__saldo = saldo_inicial

    @property
    def saldo(self):
        return self.__saldo

    def depositar(self, valor):
        if valor > 0:
            self.__saldo += valor
            return True
        return False

    def sacar(self, valor):
        if valor > 0 and self.__saldo >= valor:
            self.__saldo -= valor
            return True
        return False

class Banco:
    def __init__(self):
        self.clientes = []
        self.contas = []

    def adicionar_cliente(self, cliente):
        self.clientes.append(cliente)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def buscar_conta(self, id_conta):
        for conta in self.contas:
            if conta.id == id_conta:
                return conta
        return None


meu_banco = Banco()


@app.route('/')
def index():
    # Renderiza o menu principal na web
    return render_template('index.html', contas=meu_banco.contas)

@app.route('/cadastrar_conta', methods=['GET', 'POST'])
def cadastrar_conta():
    if request.method == 'POST':
        id_conta = request.form['id_conta']
        saldo = request.form['saldo']
        
        if id_conta.isdigit() and saldo.replace('.', '', 1).isdigit():
            nova_conta = Conta(int(id_conta), float(saldo))
            meu_banco.adicionar_conta(nova_conta)
            flash(f"Conta {id_conta} cadastrada com sucesso!", "sucesso")
            return redirect(url_for('index'))
        else:
            flash("Valores inválidos!", "erro")
            
    return render_template('formulario.html', acao="Cadastrar Conta")

@app.route('/operacao/<tipo>', methods=['GET', 'POST'])
def operacao(tipo):
    # 'tipo' pode ser 'depositar' ou 'sacar'
    if request.method == 'POST':
        id_conta = request.form['id_conta']
        valor = request.form['valor']
        
        if id_conta.isdigit() and valor.replace('.', '', 1).isdigit():
            conta = meu_banco.buscar_conta(int(id_conta))
            if conta:
                valor_float = float(valor)
                if tipo == 'depositar' and conta.depositar(valor_float):
                    flash(f"Depósito realizado! Novo saldo: R$ {conta.saldo:.2f}", "sucesso")
                elif tipo == 'sacar' and conta.sacar(valor_float):
                    flash(f"Saque realizado! Novo saldo: R$ {conta.saldo:.2f}", "sucesso")
                else:
                    flash("Operação falhou. Verifique o valor ou o saldo.", "erro")
            else:
                flash("Conta não encontrada!", "erro")
        return redirect(url_for('index'))
        
    return render_template('formulario.html', acao=tipo.capitalize())

if __name__ == '__main__':
    # Executa o servidor na sua máquina (http://127.0.0.1:5000)
    app.run(debug=True)