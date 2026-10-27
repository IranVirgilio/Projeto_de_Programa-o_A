class Cliente:
 
    def __init__(self, nome, cpf):
        
        self.nome = nome
        self.cpf = cpf

    def __str__(self):
        return f"Cliente: {self.nome} | CPF: {self.cpf}"


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

    def __str__(self):
        return f"Conta: {self.id} | Saldo: R$ {self.__saldo:.2f}"


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

    def listar_contas(self):
        if not self.contas:
            print("Não há contas cadastradas!")
        else:
            for conta in self.contas:
                print("\n===============================")
                print(conta) 
                print("===============================\n")


# =====================================================================
# INTERFACE DO TERMINAL
# =====================================================================

meu_banco = Banco()
opcao = 1

while opcao != 0:
    print("=============================================================")
    print("=====================MENU PRINCIPAL==========================")
    print("=============================================================")
    print("|| [1] - Cadastrar Cliente                                 ||")
    print("|| [2] - Cadastrar Conta                                   ||")
    print("|| [3] - Listar Contas                                     ||")
    print("|| [4] - Buscar Conta                                      ||")
    print("|| [5] - Consultar Saldo                                   ||")
    print("|| [6] - Depositar                                         ||")
    print("|| [7] - Sacar                                             ||")
    print("|| [0] - Sair                                              ||")
    print("=============================================================")
    print(" ")
    
    opcao = int(input("Digite a opção desejada: "))
    

    if opcao == 1:
        print("======CADASTRO DE CLIENTE======\n")
        nome = input("Digite o nome do cliente: ")
        cpf = input("Digite o CPF: ")
        
       
        novo_cliente = Cliente(nome, cpf)
        meu_banco.adicionar_cliente(novo_cliente)

        print("\n===============================")
        print("       Cliente cadastrado      ")
        print("===============================\n")

    elif opcao == 2:
        print("=======CADASTRO DE CONTA=======\n")
        id_conta = int(input("Digite o número da conta: "))
        saldo = float(input("Digite saldo da conta: "))
        
        nova_conta = Conta(id_conta, saldo)
        meu_banco.adicionar_conta(nova_conta)

        print("\n===============================")
        print("       Conta Cadastrada        ")
        print("===============================\n")

    elif opcao == 3:
        print("=======LISTA DE CONTAS========\n")
        meu_banco.listar_contas()

    elif opcao == 4:
        print("=======BUSCAR CONTA========\n")
        id_conta = int(input("Digite o número da conta: "))
        conta_encontrada = meu_banco.buscar_conta(id_conta)
        
        if conta_encontrada:
            print(f"Conta encontrada: {conta_encontrada.id}, saldo da conta R$ {conta_encontrada.saldo:.2f}")
        else:
            print("Conta não encontrada!")

    elif opcao == 5:
        print("=======CONSULTAR SALDO========\n")
        id_conta = int(input("Digite o número da conta: "))
        conta_encontrada = meu_banco.buscar_conta(id_conta)
        
        if conta_encontrada:
            print(f"\nSaldo da conta é R$ {conta_encontrada.saldo:.2f}\n")
        else:
            print("\nConta não encontrada!\n")

    elif opcao == 6:
        print("=======DEPOSITAR========\n")
        id_conta = int(input("Digite o número da conta: "))
        conta_encontrada = meu_banco.buscar_conta(id_conta)

        if conta_encontrada:
            valor_deposito = float(input("Digite o valor do depósito: "))
            
            if conta_encontrada.depositar(valor_deposito):
                print(f"\nDepósito realizado com sucesso! Novo saldo: R$ {conta_encontrada.saldo:.2f}\n")
            else:
                print("\nValor de depósito inválido!\n")
        else:
            print("Conta não encontrada!")

    elif opcao == 7:
        print("=======SACAR========\n")
        id_conta = int(input("Digite o número da conta: "))
        conta_encontrada = meu_banco.buscar_conta(id_conta)

        if conta_encontrada:
            valor_saque = float(input("Digite o valor do saque: "))
            
            if conta_encontrada.sacar(valor_saque):
                print(f"\nSaque realizado com sucesso! Novo saldo: R$ {conta_encontrada.saldo:.2f}\n")
            else:
                print("\nSaldo insuficiente ou valor inválido!\n")
        else:
            print("Conta não encontrada!")

    elif opcao == 0:
        print("Saindo do programa...")

    else:
         print("\nPor favor, digite um número válido!")

print("Programa Encerrado com Sucesso!")