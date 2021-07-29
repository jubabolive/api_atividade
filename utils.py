#como descobrir se as tableas no banco foram criadas mesmo depois da geracao do atividades.db
from models import Pessoas, Usuarios

def insere_pessoas():
    pessoa = Pessoas(nome='Oliveira', idade=36)# o id o banco criara automaticamente o dado
    print(pessoa)
    #db_session.add(pessoa) #insere os dados de pessoa na tabela do bando de dados
    #db_session.commit()# comita a insercao dos dados
    pessoa.save()# metodos que faz a mesma coisa das linhas comentadas db_session add, so que chama o save da classe models

def consulta_pessoas():
    pessoas = Pessoas.query.all()
    print(pessoas)
    pessoa = Pessoas.query.filter_by(nome='Joao').first()
    print(pessoa.idade)


#####################################################
    #pessoa = Pessoas.query.filter_by(nome='Oliveira')
    #for p in pessoa: # precisa do for para acessar
      #  print(p)
#####################################################



def altera_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Oliveira').first()
    pessoa.nome='Joao'
    pessoa.save()

def  exclui_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Oliveira').first() #.first eu tenho uma lista, uso o first para pegar o objeto
    pessoa.delete()

def insere_usuario(login, senha):
    usuario = Usuarios(login=login, senha = senha)
    usuario.save()

def consulta_todos_usuarios():
    usuarios = Usuarios.query.all()
    print(usuarios)




if __name__ == '__main__':
    insere_usuario('joao','1234')
    insere_usuario('oliveira', '4321')
    consulta_todos_usuarios()
    #insere_pessoas()
    #altera_pessoa()
    #consulta_pessoas()
    #exclui_pessoa()


