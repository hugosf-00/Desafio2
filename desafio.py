from datetime import datetime


banco = {}


def log_operacoes(func):
    def wrapper(*args, **kwargs):
        resultado = func(*args, **kwargs)
        
        
        operacao = func.__name__.replace('_', ' ').capitalize()
        conta = args[0] if args else 'Desconhecida'
        valor = kwargs.get('valor', 'N/A')
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        
        with open("log_banco.txt", "a") as log_file:
            log_file.write(f"[{data_hora}] Operação: {operacao} - Conta: {conta} - Valor: {valor}\n")
        
        return resultado
    return wrapper


@log_operacoes
def criar_conta():
    numero_conta = input("Digite o número da nova conta: ")
    if numero_conta in banco:
        print("Essa conta já existe.")
    else:
        nome_cliente = input("Digite o nome do titular da conta: ")
        saldo_inicial = float(input("Digite o saldo inicial: "))
        banco[numero_conta] = {
            'nome': nome_cliente,
            'saldo': saldo_inicial,
            'saques_realizados': 0,
            'ultimo_saque': None,  
            'historico': []  
        }
        print(f"Conta {numero_conta} criada com sucesso!")


def verificar_limite_saque(numero_conta):
    conta = banco[numero_conta]
    hoje = datetime.now().date()
    
    
    if conta['ultimo_saque'] != hoje:
        conta['saques_realizados'] = 0
        conta['ultimo_saque'] = hoje
    
    if conta['saques_realizados'] >= 3:
        print("Você atingiu o limite de 3 saques por dia.")
        return False
    return True


def registrar_transacao(numero_conta, tipo, valor):
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    banco[numero_conta]['historico'].append({
        'tipo': tipo,
        'valor': valor,
        'data_hora': data_hora
    })


@log_operacoes
def sacar():
    numero_conta = input("Digite o número da conta: ")
    if numero_conta in banco:
        valor = float(input("Digite o valor a ser sacado (máx. R$ 500): "))
        
        if valor > 500:
            print("O valor máximo para saque é R$ 500.")
            return
        
        if not verificar_limite_saque(numero_conta):
            return
        
        if banco[numero_conta]['saldo'] >= valor:
            banco[numero_conta]['saldo'] -= valor
            banco[numero_conta]['saques_realizados'] += 1
            print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
            
            
            registrar_transacao(numero_conta, 'Saque', valor)
        else:
            print("Saldo insuficiente.")
    else:
        print("Conta não encontrada.")


@log_operacoes
def depositar():
    numero_conta = input("Digite o número da conta: ")
    if numero_conta in banco:
        valor = float(input("Digite o valor a ser depositado: "))
        banco[numero_conta]['saldo'] += valor
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
        
        
        registrar_transacao(numero_conta, 'Depósito', valor)
    else:
        print("Conta não encontrada.")


@log_operacoes
def verificar_saldo():
    numero_conta = input("Digite o número da conta: ")
    if numero_conta in banco:
        saldo = banco[numero_conta]['saldo']
        print(f"O saldo da conta {numero_conta} é R$ {saldo:.2f}.")
    else:
        print("Conta não encontrada.")


def gerar_relatorio():
    print("\n--- Relatório das Contas Bancárias ---")
    for numero_conta, dados in banco.items():
        print(f"Conta: {numero_conta}")
        print(f"Titular: {dados['nome']}")
        print(f"Saldo: R$ {dados['saldo']:.2f}")
        print(f"Saques realizados hoje: {dados['saques_realizados']}")
        print("Histórico de transações:")
        for transacao in dados['historico']:
            print(f"- {transacao['tipo']} de R$ {transacao['valor']} em {transacao['data_hora']}")
        print("-" * 30)


class BancoIterator:
    def __init__(self, contas):
        self.contas = list(contas.items())
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index < len(self.contas):
            conta_atual = self.contas[self.index]
            self.index += 1
            return conta_atual
        else:
            raise StopIteration


def iterar_contas():
    print("\n--- Iterando sobre as contas ---")
    banco_iterator = BancoIterator(banco)
    for conta, dados in banco_iterator:
        print(f"Conta: {conta}, Titular: {dados['nome']}, Saldo: R$ {dados['saldo']:.2f}")


def menu():
    while True:
        print("\n--- Sistema Bancário ---")
        print("1. Criar Conta")
        print("2. Depositar")
        print("3. Sacar")
        print("4. Verificar Saldo")
        print("5. Gerar Relatório")
        print("6. Iterar Contas")
        print("7. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            criar_conta()
        elif opcao == "2":
            depositar()
        elif opcao == "3":
            sacar()
        elif opcao == "4":
            verificar_saldo()
        elif opcao == "5":
            gerar_relatorio()
        elif opcao == "6":
            iterar_contas()
        elif opcao == "7":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")


menu()
