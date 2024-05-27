from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime
import textwrap

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        
    def transferencia(self, conta, valor):
        valor.registrar(conta)
        
    def add_conta(self, conta):
        self.contas.append(conta)
        
class PF(Cliente):
    def __init__(self, endereco, nome, dt_nascimento, cpf):
        super().__init__(endereco)
        self.nome = nome
        self.dt_nascimento = dt_nascimento
        self.cpf = cpf
        
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = cliente
        self._historico = Historico()
        
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self._saldo
        
        if valor > saldo:
            print("Operação inválida, saldo insuficiente")
            return True
            
        elif valor > 0:
            self._saldo -= valor
            print("Saque realizado com sucesso")
            return True
        
        else:
            print("Operação falhou. O valor invalido")
            
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Deposito realizado com sucesso")
            return True
        
        else:
            print("Operação falhou. O valor invalido")
            
        return False
        
class CC(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saque=3):
        super().__init__(numero, cliente)   
        self.limite = limite
        self.limite_saque = limite_saque
        
        def sacar(self, valor):
            numero_saques = len(
                [
                    transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__
                ]
            )
            
            if valor > self.limite:
                print("Valor de saque excede o limite")
                
            elif numero_saques > self.limite_saque:
                print("Numero maximo de saque excedido")
                
            else:
                return super().sacar(valor)
            
            return False
        
    def __str__(self):
        return f"""\
                Ag: {self.agencia}
                C/CC: {self.numero}
                Titular: {self.cliente.nome}
            """

class Historico:
    def __init__(self) -> None:
        self.transacoes = []
        
    @property
    def trasancoes(self):
        return self.transacoes
    
    def add_transacao(self, transacao):
        self.transacoes.append(
            {
                "tp": transacao.__clas__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }
        )
        
class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    
    @abstractclassmethod
    def registrar(self, conta):
        pass
    
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.add_transacao(self)
            
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.add_transacao(self)
            
def menu():
   menu = """
   ********** MENU **********
   [1] Depositar
   [2] Sacar
   [3] Extrato
   [4] Nova Conta
   [5] Listar Contas
   [6] Novo Usuario
   
   [0] Sair
   => """
   
   return int(input("Informe a opção desejada: "))   

def filtrar_cliente(cpf, clientes):
    cliente_fitrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    
    return cliente_fitrados[0] if cliente_fitrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não possui conta!")
        return
    
    return cliente.contas[0]   

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente =  filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("Cliente não encontrado!")
        return
    
    valor =  float(input("Informe o valor do deposito: "))
    transacao = Deposito(valor)
    
    if not recuperar_conta_cliente(cliente):
        return
    
    cliente.realizar_transacao(recuperar_conta_cliente(cliente), transacao)

def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente =  filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("Cliente não encotrado!")
        return
    
    valor =  float(input("Informe o valor do saque: "))
    transacao = Saque(valor)
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente =  filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("Cliente não encotrado!")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("############### EXTRATO ###############")
    transacoes = conta.historico.transacoes

    extrato = ''
    if not transacoes:
        extrato = "Não foram realizadas movimentações"
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\nR${transacao['valor']:.2f}"
            
    print(extrato)
    print(f"\nSaldo: R$ {conta.saldo:.2f}")

def criar_cliente(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente =  filtrar_cliente(cpf, clientes)
    
    if cliente:
        print("Cliente já existe!")
        return
    
    cliente = PF(
                    nome=input("Infome o nome: "),
                    dt_nascimento=input("Informe a data de nascimento: "),
                    cpf=input("Informe o cpf: "),
                    endereco=input("Informe o endereço: ")
                )

    clientes.append(cliente)
    
    print("Cliente cadastrado com sucesso!")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente =  filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("Cliente não encotrado!")
        return
    
    conta = CC.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    
    print("Conta criada com sucesso! ")

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def main():
    clientes = []
    contas = []
    
    while True:
        opcao = menu()
        
        if opcao == 1:
            depositar(clientes)
            
        elif opcao == 2:
            sacar(clientes)
            
        elif opcao == 3:
            exibir_extrato(clientes)
            
        elif opcao == 4:
            criar_cliente(clientes)
        
        elif opcao == 5:
            listar_contas(contas)
            
        elif opcao == 6:         
            criar_conta(len(contas + 1), clientes, contas)
            
        elif opcao == 0:
            break
        
        else:
            print("Operação invalida!")