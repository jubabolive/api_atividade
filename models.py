#no models onde terao as classes que referenciarao uma tabela no banco de dados

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey #Colum para poder criar colunas, integer e string para dados inteiros e strings no banco
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///atividades.db', convert_unicode=True) #criando as conexoes com o banco de dados
db_session = scoped_session(sessionmaker(autocommit=False,
                                                                                bind = engine))
Base = declarative_base()
Base.query = db_session.query_property()

class Pessoas(Base):#tem que ter o Base como parametro na classe...
    __tablename__= 'pessoas'# o nome da tabela é o que está referenciado aqui no tablename idependente  do nome da classe
    id = Column (Integer, primary_key = True)
    nome = Column(String(40), index = True) #cria um indice para essa coluna para deixar a consulta mais rapida quando for pelo nome
    idade = Column(Integer)

    def __repr__(self):  #funcao de representacao da classe
        return '<Pessoa {} >' .format(self.nome)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

class Atividades(Base):
        __tablename__='atividades' #tablename recebe atividades
        id = Column(Integer, primary_key=True)
        nome = Column(String(80) )
        pessoa_id = Column(Integer, ForeignKey('pessoas.id'))
        pessoa = relationship("Pessoas")# para reconhecer o relacionamento da tabela atividades com a tabela pessoas

        def __repr__(self):  # funcao de representacao da classe
            return '<Atividades {} >'.format(self.nome)

        def save(self):
            db_session.add(self)
            db_session.commit()

        def delete(self):
            db_session.delete(self)
            db_session.commit()

class Usuarios(Base):  #criacao de tabela de usuarios para autenticacao na pagina
    __tablename__= 'usuarios'
    id = Column(Integer, primary_key=True)
    login = Column(String(20), unique=True)
    senha = Column(String(20))

    def  __repr__(self):
        return '<Usuario {}' .format(self.login)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()





def init_db():
            Base.metadata.create_all(bind=engine)#esse comando que criará o banco de dados

if __name__ == '__main__':
    init_db()


