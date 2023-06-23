# Importando bibliotecas
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from random import choice
from random import randint
import sqlite3
import os.path


class Personagem(BoxLayout): # Criação da classe Personagem 

    def __init__(self, nome): # Definindo os atributos
        self.nome = nome
        self.pontosEnergia = 100
        self.ataqueMax = 50
        self.ataqueMin = 10
    
    
    def Atacar(self): # Calcula o valor do ataque do personagem no bicho
        valor = randint(self.ataqueMin,self.ataqueMax)
        return valor


    def Critico(self): # Calcula o ataque do bicho no personagem 
        numero = randint(0,10)
        if numero < 2: # Interação que verifica a intensidade do ataque e retorna o dano causado ao bicho
            dano = 100
            return dano
        else: 
            dano = 0
            self.pontosEnergia += numero * 3
            return dano
  
              
    def SofreDano(self,dano): # Calcula os pontos de vida do personagem após o ataque do bicho
        self.pontosEnergia -= dano
 
    
class UtilizaBanco: # Criação da classe UtilizaBanco , utilizada para fazer a comunicação com o banco de dados e ações nele      

    def cadastraPartida(self,partida): # Cadastra uma partida no banco de dados
        BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Recupera caminho em que o banco está no sistema de arquivos
        caminhoBanco = os.path.join(BASE_DIR,'Bichomon.db')
        conexao = sqlite3.connect(caminhoBanco) # Conecta ao banco Bichomon.db
        cursor = conexao.cursor() # Abertura de canal para executar códigos SQL no banco
        SQL = '''INSERT INTO Partida(codPartida,codHistoria,nomePersonagem)
                      VALUES(?,?,?)''' # Valores a serem introduzidos na tabela Partida
        cursor.execute(SQL,partida)  # Executando uma consulta na tabela 'Partida' do banco 'Bichomon.db'
        conexao.commit() # Confirma a execução no banco de dados
        cursor.close() # Finaliza a conexão com o banco de dados
                   
        
    def RecuperaDadosHistoria(self,tipo): # Recupera um texto referente a história escolhida
        BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Recupera caminho em que o banco está no sistema de arquivos
        caminhoBanco = os.path.join(BASE_DIR,'Bichomon.db')
        conexao = sqlite3.connect(caminhoBanco)   # Conecta ao banco Bichomon.db
        SQL = '''SELECT *  
                 FROM Historia
                 WHERE tipo=?'''  # Seleciona tudo da tabela Historia em função do tipo informado
        cursor = conexao.cursor() # Abertura de canal para executar códigos SQL no banco
        cursor.execute(SQL,(tipo,))  # Executando uma consulta na tabela 'Historia' do banco 'Bichomon.db'
        registros = cursor.fetchall() # Armazenando em 'registros' todas as linhas resultantes do código SQL executado
        cursor.close() # Finaliza a conexão com o banco de dados
        hist_sorteada = choice(registros) # Sorteia um valor dentro da tupla registros
        return hist_sorteada # Retorna uma lista com os seguintes dados: codHistoria,textoIntro,tipo
         
    
    def RecuperaListaBichos(self,tipo): # Recupera a lista de bichos presentes na tabela Bicho                         
        BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Recupera caminho em que o banco está no sistema de arquivos
        caminhoBanco = os.path.join(BASE_DIR,'Bichomon.db')
        conexao = sqlite3.connect(caminhoBanco) # Conecta ao banco Bichomon.db
        SQL = '''SELECT *
                 FROM Bicho
                 WHERE codHistoria=?''' # Seleciona tudo da tabela Bicho em funçao do codHistoria informado
        cursor = conexao.cursor() # Abertura de canal para executar códigos SQL no banco
        cursor.execute(SQL,(tipo,))  # Executando uma consulta na tabela 'Bicho' do banco 'Bichomon.db'
        registros = cursor.fetchall() # Armazenando em 'registros' todas as linhas resultantes do código SQL executado
        cursor.close() # Finaliza a conexão com o banco de dados
        return registros # Retorna a lista de bichos com base no seu codHistoria contendo: codBicho, codHistoria, nome, pontosEnergia, ataqueMax, ataqueMin  
  
    
banco_dados = UtilizaBanco()  # Criação de um objeto para a classe UtilizaBanco    



class Bicho: # Criação da classe Bicho

    def __init__(self, codBicho, nome, pontosEnergia, ataqueMax, ataqueMin):  # Definindo os atributos, refletindo a estrutura da tabela Bicho
        self.codBicho      = codBicho
        self.nome          = nome
        self.pontosEnergia = pontosEnergia
        self.ataqueMax     = ataqueMax
        self.ataqueMin     = ataqueMin
        
        
    def Atacar(self): # Retorna o valor do ataque do bicho no Personagem com base em seus valores de ataqueMáx e ataqueMín
        valor = randint(self.ataqueMin,self.ataqueMax)
        return valor
     
        
    def SofreDano(self,dano): # Calcula os pontos de energia do Bicho após o ataque do Personagem
        self.pontosEnergia -= dano


class Historia(BoxLayout): # Criação da classe Bicho

    def __init__(self, codHistoria, textoIntro, tipo): # Definindo os atributos, refletindo a estrutura da tabela Historia
        self.codHistoria = int(codHistoria) 
        self.textoIntro  = textoIntro
        self.tipo        = int(tipo)
        
        
    def ExibeIntro(self): # Retorna o texto referente ao tipo de história ( Fácil ou Difícil )
        return self.textoIntro

   
class Partida: # Criação da classe Partida

    def __init__(self, personagem, historia,bichos): # Definição dos atributos da classe Partida
        self.personagem       = personagem
        self.historia         = historia  
        self.bichos           = bichos
        self.contadorBatalhas = 0
  
    
    def executaTurnoPartida(self,ataqueCritico): # Executa todas ações ocorrentes em uma partida
        nome_personagem = self.personagem.nome  # Nome digitado do Personagem 
        
        if self.contadorBatalhas > 4 or self.personagem.pontosEnergia < 0 : # Interação que verifica se a quantidade de batalhas é superior a máxima quantidade de batalhas
            texto_bicho = 'O jogo acabou, recomece o jogo'  # Texto retornado após o jogo ser finalizado
            return texto_bicho
        
        if ataqueCritico == True: # Interação que verifica se o usuário selecionou o botão Atacar ou Tentar a Sorte
            valor_ataque_per = self.personagem.Critico() 

        else:
            valor_ataque_per = self.personagem.Atacar()


        
        self.bichos[self.contadorBatalhas].SofreDano(valor_ataque_per) # Uma lista de bichos baseadas no tipo de história escolhido, sofrendo o dano do ataque do Personagem
        pontos_energia_bicho = self.bichos[self.contadorBatalhas].pontosEnergia # Calcula os novos pontos de energia do bicho após o ataque do Personagem
        
        if pontos_energia_bicho > 0: # Interação que verifica se o bicho está vivo ou não
            nomeBicho = self.bichos[self.contadorBatalhas].nome # Acessa lista de bichos para retornar um nome
            valor_ataque_bicho = self.bichos[self.contadorBatalhas].Atacar() # Retorna o valor do ataque do bicho da partida
            self.personagem.SofreDano(valor_ataque_bicho) # Chama o método SofreDano() passando como parâmetro o valor do ataque do bicho
            texto_bicho = 'O personagem atacou com ' + str(valor_ataque_per) +  ' de força. O bicho '  + nomeBicho + ' agora tem '+ str(pontos_energia_bicho) + ' \npontos de energia após o ataque do ' + self.personagem.nome + '. O Bicho atacou com ' + str(valor_ataque_bicho) + ' de força.' # Texto retornado mostrando a força dos ataques e os pontos de vida restantes do bicho       
            return texto_bicho
            
        else: # Quando o bicho é derrotado      
            self.contadorBatalhas += 1 # Vai para o próximo bicho da lista
            texto = nome_personagem + ' venceu a batalha e vai enfrentar o próximo bicho.' # Texto retornado após o personagem derrotar um bicho
        
            if (self.historia.tipo == 2 and self.contadorBatalhas == 4) or (self.historia.tipo == 1 and self.contadorBatalhas == 4): # Verifica se o Personagem conseguiu derrotar todos os bichos 
                texto = 'O Mago '+ nome_personagem + ' derrotou todos os seus inimigos e assim obteve aprimoramento de seus poderes.' # Texto retornado se o Personagem conseguiu derrotar todos os bichos
            
            return texto


# ARQUIVO KV 
class Joguinho(BoxLayout): # Criação da classe do arquivo kv

    def __init__(self,**kwargs): # Definição dos atributos
        super().__init__(**kwargs)    
        Window.size = (1000, 600)  # Define o tamanho da janela
        Window.clearcolor = 0.3,0,0.6,0 # Define a cor da janela
        self.nivel = 0
        self.personagem = ' ' 
        self.partida = ' '
        self.Bichos = []
        self.story = ' '


    def selDificuldade(self,nivel): # Verificou o tipo de história ( dificulade ) que o usuário selecionou       
        if nivel == 'Dificil': # Definição do nível com base na história escolhida
            self.nivel = 1
        if nivel == 'Facil':
            self.nivel = 2
      
        
    def iniciar(self): # Utilizado para começar uma partida      
        listabichos = banco_dados.RecuperaListaBichos(self.nivel)
        self.Bichos = [] # Lista vazia
        for i in listabichos: # i é cada uma das listas
            bicho = Bicho(codBicho = i[0] , nome = i[2], pontosEnergia= i[3], ataqueMax= i[4], ataqueMin = i[5]) # Criação de um objeto para a classe Bicho
            self.Bichos.append(bicho) # Adiciona o objeto a lista de bichos 
            
        nome_personagem = self.ids.personagem.text  # Nome digitado do Personagem
        
        if self.nivel == 1: # Interação que verifica o tipo de história selecionada
            self.personagem = Personagem(nome_personagem) # Criando o objeto da classe Personagem
            self.story = Historia(1, banco_dados.RecuperaDadosHistoria(1)[1], 1)  # Criando um objeto da classe Historia 
            self.ids.dadosbh.text = self.story.ExibeIntro() # Exibe no kv a intro da história com base no nível Difícil 
            self.ids.dadosper.text  = 'O mago ' + self.personagem.nome + ' possui '+ str(self.personagem.pontosEnergia) + ' pontos de energia.' # Exibe no kv os pontos de energia do personagem
            
        if self.nivel == 2:
            self.personagem = Personagem(nome_personagem) # Criando o objeto da classe Personagem
            self.story = Historia(2, banco_dados.RecuperaDadosHistoria(2)[1], 2)  # Criando um objeto da classe Historia  
            self.ids.dadosbh.text = self.story.ExibeIntro() # Exibe no kv a intro da história com base no nível Fácil
            self.ids.dadosper.text  = 'O mago ' + self.personagem.nome + ' possui '+ str(self.personagem.pontosEnergia) + ' pontos de energia.' # Exibe no kv os pontos de energia do personagem      
        
        self.partida = Partida(self.personagem,self.story,self.Bichos) # Criando um objeto para a classe Partida
        ptd = (None,self.nivel,nome_personagem) # Valores a serem adicionados na tabela Partida
        banco_dados.cadastraPartida(ptd) # Adicionando a tabela os valores de uma Partida
        

    def Atacar(self):  # Função atacar 
        nome_personagem = self.ids.personagem.text # Nome digitado do Personagem
        self.ids.dadosbh.text = self.partida.executaTurnoPartida(False) # Chama o método de executar partida, passando False como parâmetro para representar que o usuário apertou no botão Atacar
      
        if self.personagem.pontosEnergia <= 0: # Interação que verifica se o personagem morreu
            self.ids.dadosbh.text = 'O Mago '+ nome_personagem + ' infelizmente perdeu essa batalha. Mais sorte na próxima vez...' # Texto retornado se o personagem morrer
            self.ids.dadosper.text = 'O mago ' + self.personagem.nome + ' morreu, tente novamente vencer os bichos!'  # Texto retornado se o personagem morrer
            
        else: # Mostra os pontos de energia resultantes do personagem
            self.ids.dadosper.text = 'O mago '+ self.personagem.nome + ' está com '+ str(self.personagem.pontosEnergia) +' pontos de energia.'
    
     
    def tentarsorte(self):  # Função tentar a sorte 
        nome_personagem = self.ids.personagem.text # Nome digitado do Personagem
        self.ids.dadosbh.text = self.partida.executaTurnoPartida(True) # Chama o método de executar partida, passando True como parâmetro para representar que o usuário apertou no botão Tentar a Sorte
        self.ids.dadosper.text = 'O personagem ' + nome_personagem + ' foi atacado e agora tem ' + str(self.personagem.pontosEnergia) + ' pontos de energia. \n ' + nome_personagem + ' não conseguiu atacar o bicho, mas recuperou um pouco de energia ' # Texto retornado após o ataque do bicho


class bichomonApp(App): # Criação do App
    def build(self): # Utilizado para criar o Joguinho
        self.title = 'Jogo do Mago Implacável' #Título app
        return Joguinho()
    
obj = bichomonApp() # Definição do objeto do App
obj.run() # Roda o Joguinho
