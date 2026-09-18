clientes = []
contas = []
opcao = 1

def buscar(id,lista_contas):
    for conta in lista_contas:
        if conta in lista_contas:
            if conta ['id'] == id:
             return conta
    return None
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
        novo_cliente = {"nome":nome, "cpf":cpf}
        clientes.append(novo_cliente)

        print(" ")
        print("===============================")
        print("       Cliente cadastrado      ")
        print("===============================\n")

    elif opcao == 2:
        print("=======CADASTRO DE CONTA=======\n")
        id = int(input("Digite o número da conta: "))
        saldo = float(input("Digite saldo da conta: "))
        nova_conta = {"id":id, "saldo":saldo}
        contas.append(nova_conta)

        print(" ")
        print("===============================")
        print("       Conta Cadastradada      ")
        print("\n===============================")

    elif opcao == 3:
        print("=======LISTA DE CONTAS========\n")
        if len(contas) == 0:
            print("Não há contas cadastradas!")
        else:
            for conta in contas:
             print("\n===============================")
             print(f"Conta: {conta['id']}")
             print("===============================\n")

    elif opcao == 4:
        print("=======BUSCAR CONTA========\n")
        id = int(input("Digite o número da conta: "))
        encontrar_conta = (buscar(id, contas))
        if encontrar_conta:
            print(f"Conta encontrada: {encontrar_conta['id']}, saldo da conta R$ {encontrar_conta['saldo']}")
        else:
            print("Conta não encontrada!")

    elif opcao == 5:
        print("=======CONSULTAR SALDO========\n")
        id = int(input("Digite o número da conta: "))
        encontrar_conta = (buscar(id, contas))
        if encontrar_conta:
            print(" ")
            print(f"Saldo da conta é R$ {encontrar_conta['saldo']}\n")
        else:
            print("Conta não encontrada!\n")

    elif opcao == 6:
        print("=======DEPOSITAR========\n")
        id = int(input("Digite o número da conta: "))
        encontrar_conta = (buscar(id, contas))

        if encontrar_conta:
            valor_deposito = float(input("Digite o valor do depósito: "))
            encontrar_conta['saldo'] += valor_deposito

            print(" ")
            print(f"Depósito realizado com sucesso! Novo saldo: R$ {encontrar_conta['saldo']}\n")
        else:
            print("Conta não encontrada!")

    elif opcao == 7:
        print("=======SACAR========\n")
        id = int(input("Digite o número da conta: "))
        encontrar_conta = (buscar(id, contas))

        if encontrar_conta:
            valor_saque = float(input("Digite o valor do saque: "))
            if encontrar_conta['saldo'] >= valor_saque:
                encontrar_conta['saldo'] -= valor_saque
                print(" ")
                print(f"Saque realizado com sucesso! Novo saldo: R$ {encontrar_conta['saldo']}\n")

            else:
                print("Saldo insuficiente!")
        else:
            print("Conta não encontrada!")

    elif opcao == 0:
        print("Saindo do programa...")

    else:
        print("\n Opção Inválida!")

print("Programa Encerrado com Sucesso!")