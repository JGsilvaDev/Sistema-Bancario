clientes = {}

def cadastrar_cliente(cpf):
    global clientes
    
    if cpf in clientes:
        clientes[cpf]["nome"] =  input("Nome: ")
        clientes[cpf]["endereco"] =  input("Endereço: ")
        clientes[cpf]["data_ascimento"] =  input("Data de Nascimento: ")
        
        print("Cliente cadastrado!\n")
    else:
        print("CPF invalido, por favor cadastrar conta-bancaria")
    
def cadastrar_conta_corrente(cc, saldo, limite_saque, valor_limite_saque, cpf):
    global clientes
    
    extrato = []
    
    conta = { cpf: {"cc": cc, "saldo": saldo, "limite_saque": limite_saque, "valor_limite_saque": valor_limite_saque, "extrato": extrato }}
    clientes.update(conta)
    
    print("Conta cadastrada")

# cadastrar_conta_corrente('011255-2', 1000, 5 ,"484.285.138-48") 
# cadastrar_conta_corrente('011209-2', 10000, 2, "489.225.135-46") 
# cadastrar_cliente('484.285.138-48')
# cadastrar_cliente('489.225.135-46')

def exibe_extrato(cliente):
    
    print("\nEXTRATO")
    for ext in cliente['extrato']:
        print(ext)
       
    print(f"Saldo em conta: R${cliente['saldo']:.2f}") 

def deposito(deposito, cliente):
    extrato = cliente['extrato']
    saldo = cliente['saldo']
    
    if deposito > 0:
        print('\nDepositando...')
        cliente['saldo'] = saldo
        print("Deposito realizado com sucesso")
        extrato.append(f"Deposito: R${deposito:.2f}")
    else:
        print("Valor impossivel de se depositar")

def saque(*, saque, cliente):
    extrato = cliente['extrato']
    saldo =  cliente['saldo']
    limite_saque = cliente['limite_saque']
    valor_limite_saque = cliente['valor_limite_saque']
    
    if saldo >= saque:
        if limite_saque != 0:
            if saque >= valor_limite_saque: 
                print("Valor limite excedido")
            else:   
                print("\nSacando...")
                saldo -= saque
                cliente['saldo'] = saldo
                print("Saque realizado com sucesso")
                limite_saque -= 1
                cliente['limite_saque'] = limite_saque
                extrato.append(f"Saque: R${saque:.2f}")
        else:
            print("Saques diarios excedidos")
    else:
        print("Não será possivel sacar o dinheiro por falta de saldo!")

while True:
    cpf_cliente = input("Informe o CPF: ")

    has_conta = True if cpf_cliente in clientes else False
    admin = True if cpf_cliente == '484.285.138-48' else False
    
    if admin:
        while True:
            menu_admin = int(input(
                """\n     ###    MENU    ###
                [1] Cadastrar Cliente
                [2] Cadastrar Conta
                [3] Listar Clientes
                                
                [0] Sair
                
                Selecione a operação desejada: """
                
            ))
            
            if menu_admin == 0: 
                break
            
            if menu_admin == 1:
                cadastrar_cliente(input("Inoforme o CPF: "))
                
            if menu_admin == 2:
                cadastrar_conta_corrente(
                    input("Informe a CC: "), 
                    float(input("Informe o saldo em conta: ")), 
                    int(input("Informe a quantidade de saques diarios: ")),
                    float(input("Informe o valor limite para saque diario: ")),
                    input("Informe o cpf: ")
                ) 
                
            if menu_admin == 3:
                for cpf, dados in clientes.items():
                    print(f"CPF: {cpf}, Dados: {dados}")
    
    elif has_conta:
        while True:
            menu = int(input(
            """\n     ###    MENU    ###
                [1] Depositar
                [2] Sacar
                [3] Extrato
                                
                [0] Sair
                
                Selecione a operação desejada: """))
            
            cliente = clientes[cpf_cliente]
            
            if menu == 0: 
                break
            
            if menu == 1:
                while True:
                    valor = int(input("Insira o valor a ser depositado: "))     
                    deposito(valor, cliente)
                    
                    opcao = input("Deseja realizar outro deposito? S ou N: ").strip().upper()
                    
                    if opcao != "S":
                        break
                
            if menu == 2:
                while True:
                    valor = int(input("Insira o valor a ser sacado: "))     
                    saque(saque=valor, cliente=cliente)
                    
                    opcao = input("Deseja realizar outro saque? S ou N: ").strip().upper()
                    
                    if opcao != "S":
                        break
                
            if menu == 3:
                exibe_extrato(cliente)
    else:
        print("Informe um CPF valido!\n")    