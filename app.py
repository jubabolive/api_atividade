from flask import Flask, request
from flask_restful import Resource, Api
from models import Pessoas, Atividades, Usuarios
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)

#USUARIOS = {     comentando codigo, usuario serao inseridos via tabela banco de dados
 #   'jonatas':'123',
 #   'oliveira':'321'
#}

#@auth.verify_password
#def verificacao(login, senha): #vai retornar falso caso a autenticacao nao tenha sido feita com sucesso
 #   print('Validando Usuario')
  #  print(USUARIOS.get(login) == senha)
   # if not (login, senha):
    #    return False
    #return USUARIOS.get(login) == senha

@auth.verify_password
def verificacao(login, senha): #vai retornar falso caso a autenticacao nao tenha sido feita com sucesso
       if not (login, senha):
          return False
       return Usuarios.query.filter_by(login=login, senha=senha).first()




class Pessoa(Resource):
    @auth.login_required   #estou obrigando que o metodo get passe pela verificacao de senha
    def get(self, nome): #recebendo nome como parametro
        pessoa = Pessoas.query.filter_by(nome=nome).first() #.first para pegar o objeto
        try:
                response = {
                    'nome':pessoa.nome,
                    'idade':pessoa.idade,
                    'id':pessoa.id

                }
        except AttributeError:
                response = {
                    'status':'error',
                    'mensagem':'Pessoa nao encontrada'
                }

        return response

    def  put(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()  # ira realizar uma consulta no banco de dados
        dados = request.data.json
        if 'nome' in dados: #se existir nome dentro do dicionario dados
            pessoa.nome = dados['nome']
        if 'idade' in dados: #se existir idade dentro do dicionario dados
            pessoa.idade = dados['idade']
        pessoa.save()
        response = {
            'id':pessoa.id,
            'nome':pessoa.nome,
            'idade':pessoa.idade
        }
        return response

    def delete(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        mensagem = 'Pessoa {} excluida com sucesso' .format(pessoa.nome)
        pessoa.delete()
        return{'status':'sucesso', 'mensagem':mensagem}

class ListaPessoas(Resource):
    @auth.login_required()
    def get(self):
        pessoas = Pessoas.query.all()
        response = [{'id':i.id, 'nome':i.nome, 'idade':i.idade} for i in pessoas]  #response recebe uma lista de um dicionario {} esse for se chama for in line, e como se fosse um lambda
        print(response)
        return response

    def post(self):
        dados = request.json
        pessoa = Pessoas(nome=dados['nome'], idade=dados['idade'])
        pessoa.save()
        response = {
            'id': pessoa.id,
            'nome': pessoa.nome,
            'idade': pessoa.idade
        }
        return response

class ListaAtividades(Resource):
    def  get(self):
        atividades = Atividades.query.all()
        response = [{'id':i.id, 'nome':i.nome, 'pessoa':i.pessoa.nome} for i in atividades] #acesso o objeto pessoa e acesso o nome da pessoa
        return response

    def post(self):
        dados = request.json
        pessoa = Pessoas.query.filter_by(nome=dados['pessoa']).first()
        atividade = Atividades(nome=dados['nome'], pessoa = pessoa)
        atividade.save()
        response = {
            'pessoa':atividade.pessoa.nome,
            'nome':atividade.nome,
            'id':atividade.id
        }
        return response




api.add_resource(Pessoa, '/pessoa/<string:nome>/') #rotas para a pagina web
api.add_resource(ListaPessoas, '/pessoa/')
api.add_resource(ListaAtividades, '/atividades/')



if __name__ == '__main__':
    app.run(debug=True)