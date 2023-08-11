from peewee import *
from enum import Enum

db = Proxy()


# faixasEtarias = {1: '18 a 25 anos',
#                  2: '26 a 35 anos',
#                  3: '36 a 45 anos',
#                  4: '46 a 55 anos',
#                  5: 'Mais de 55 anos'}

# tempoInstituicao = {1: 'Menos de 2 anos',
#                     2: 'Entre 3 a 6 anos',
#                     3: 'Entre 7 a 10 anos',
#                     4: 'Entre 11 a 15 anos',
#                     5: 'Mais de 15 anos'}


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    email = CharField()
    permissao = CharField()
    created = DateTimeField()


class Unidade(BaseModel):
    sigla = CharField()


class Area(BaseModel):
    nome = CharField()


class Cargo(BaseModel):
    nome = CharField()


class Questionario(BaseModel):
    titulo = CharField()
    ano = IntegerField()
    descricao = TextField()
    status = CharField()
    created = DateTimeField()
    inicio = DateTimeField()
    fim = DateTimeField()

    def dimensoes(self):
        return (Dimensao
                .select(Dimensao)
                .join(Grupo, on=(Dimensao.id == Grupo.dimensao_id), join_type=JOIN.LEFT_OUTER)
                .join(Questionario, on=(Questionario.id == Grupo.questionario_id), join_type=JOIN.LEFT_OUTER)
                .order_by(Dimensao.ordem).distinct())

    def grupos(self):
        return (Grupo
                .select(Grupo)
                .join(Questionario, on=(Questionario.id == Grupo.questionario_id))
                .order_by(Grupo.ordem))


class Dimensao(BaseModel):
    titulo = CharField()
    ordem = IntegerField()
    # status = CharField()


class QuestionarioDimensao(BaseModel):
    questionario = ForeignKeyField(Questionario, backref='questionario')
    dimensao = ForeignKeyField(Dimensao, backref='dimensao')
    valor = FloatField()


# class QuestionarioDimensao(BaseModel):
#     questionario = ForeignKeyField(Questionario, backref='questionario')
#     dimensao = ForeignKeyField(Dimensao, backref='dimensao')
#     valor = FloatField()


class Grupo(BaseModel):
    titulo = CharField()
    ordem = IntegerField()
    questionario = ForeignKeyField(Questionario, backref='questionario')
    dimensao = ForeignKeyField(Dimensao, backref='dimensao')

    def perguntas(self):
        return (Pergunta
                .select(Pergunta)
                .join(Grupo, on=(Grupo.id == Pergunta.grupo_id))
                .order_by(Pergunta.ordem))


class Pergunta(BaseModel):
    titulo = CharField()
    tipo = IntegerField()
    ordem = IntegerField()
    grupo = ForeignKeyField(Grupo, backref='grupo')
    questionario = ForeignKeyField(Questionario, backref='questionario')
    created = DateTimeField()


class Pessoa(BaseModel):
    nome = CharField()
    email = CharField()
    genero = CharField()
    idade = CharField()
    tempo = CharField()
    escolaridade = CharField()
    experiencia = CharField()
    formacaoInovacao = CharField()
    unidade = ForeignKeyField(Unidade, backref='unidade')
    area = ForeignKeyField(Area, backref='area')
    # cargo = CharField()
    cargo = ForeignKeyField(Cargo, backref='cargo')
    questionario = ForeignKeyField(Questionario, backref='questionario')
    created = DateTimeField()


class Resposta(BaseModel):
    valor = TextField()
    pergunta = ForeignKeyField(Pergunta, backref='pergunta')
    questionario = ForeignKeyField(Questionario, backref='questionario')
    pessoa = ForeignKeyField(Pessoa, backref='pessoa')
    created = DateTimeField()
