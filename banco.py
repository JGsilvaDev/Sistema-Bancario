saldo = 10000
LIMITE_SAQUE = 3
extrato = []

def exibe_extrato():
    global saldo, extrato
    print("\nEXTRATO")
    for ext in extrato:
        print(ext)
       
    print(f"Saldo em conta: R${saldo:.2f}") 
    

def deposito(deposito):
    global saldo, extrato
    
    if deposito > 0:
        print('\nDepositando...')
        saldo += deposito
        print("Deposito realizado com sucesso")
        extrato.append(f"Deposito: R${deposito:.2f}")
    else:
        print("Valor impossivel de se depositar")

def saque(saque):
    global saldo, LIMITE_SAQUE, extrato
    
    if saldo >= saque:
        if LIMITE_SAQUE != 0:
            if saque >= 500: 
                print("Valor limite excedido")
            else:   
                print("\nSacando...")
                saldo -= saque
                print("Saque realizado com sucesso")
                LIMITE_SAQUE -= 1
                extrato.append(f"Saque: R${saque:.2f}")
        else:
            print("Saques diarios excedidos")
    else:
        print("Não será possivel sacar o dinheiro por falta de saldo!")
   
while True:
    menu = int(input(
    """\n     ###    MENU    ###
        [1] Depositar
        [2] Sacar
        [3] Extrato
                         
        [0] Sair
        
        Selecione a operação desejada: """))
    
    if menu == 0: break
    
    if menu == 1:
        while True:
            valor = int(input("Insira o valor a ser depositado: "))     
            deposito(valor)
            
            opcao = input("Deseja realizar outro deposito? S ou N: ").strip().upper()
            
            if opcao != "S":
                break
        
    if menu == 2:
        while True:
            valor = int(input("Insira o valor a ser sacado: "))     
            saque(valor)
            
            opcao = input("Deseja realizar outro saque? S ou N: ").strip().upper()
            
            if opcao != "S":
                break
        
    if menu == 3:
        exibe_extrato()
    