from statistics import quantiles
from time import sleep
from flask import Flask, jsonify, render_template, redirect, url_for, request, g, session, flash
from hashlib import sha512
from database import *
from auth import *
from utils import *
from datetime import date, datetime
from models import *
import os
import csv
# import numpy
import math
# from flask_wtf.csrf import CSRFProtect

# from models import User


# variaveis de "ambiente flask"
debug = True
resetar_db = False

SECRET_KEY = 'TapW9SJJopd4mOM36173M5r2J1l1EhySGKcnNcO52JPUe5Qc+VTpbdTFt+d0tdwBF54FXs8tUaFaFoSg3wLR'
app = Flask(__name__)
app.secret_key = SECRET_KEY
# csrf = CSRFProtect(app)


@app.template_filter('is_following')
def is_following(from_user, to_user):
    return from_user.is_following(to_user)


@app.before_request
def before_request():
    g.db = db
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if session.get('autenticad'):
        session.pop('_flashes', None)
        return redirect(url_for('panel_questionarios'))
    if request.method == 'POST' and request.form['username']:
        try:
            pw_hash = sha512(
                request.form['password'].encode('utf-8')).hexdigest()
            user = User.get(
                (User.username == request.form['username']) &
                (User.password == pw_hash))
        except User.DoesNotExist:
            flash('Usuário ou senha incorretos, tente novamente')
            error = 'Usuário ou senha incorretos, tente novamente'
        else:
            auth_user(user)
            session.pop('_flashes', None)
            if 'admin' in session.get('permissao'):

                return redirect(url_for('panel_questionarios'))
            else:
                return redirect(url_for('panel_questionarios'))

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('autenticad', None)
    flash('Você esta deslogado. Até mais!')
    return redirect(url_for('index'))


@app.route('/panel')
@login_required
def panel():
    return render_template('admin.html')


@app.route('/panel/dimensoes')
@acesso_required('admin')
def panel_dimensoes():
    dimensoes = Dimensao.select().order_by(Dimensao.ordem)
    return object_list('list_dimensoes.html', dimensoes, 'list', titulo="Dimensões")


@app.route('/panel/grupos')
@acesso_required('admin')
def panel_grupos():
    grupos = Grupo.select().join(Dimensao).order_by(Dimensao.ordem, Grupo.ordem)
    return object_list('list_grupos.html', grupos, 'list', titulo="Grupos")


@app.route('/panel/questionarios', methods=["GET", "POST"])
@acesso_required('admin')
def panel_questionarios():
    if request.method == 'POST':
        form = request.form
        jaCadastrado = Questionario.select().where(
            Questionario.titulo == form['titulo'] and Questionario.ano == form['ano'])
        if jaCadastrado:
            flash("Já existe um questionário cadastrado com esse titulo e ano!")
        else:
            questionario = Questionario(
                titulo=form['titulo'].strip().lower(),
                ano=int(form['ano']),
                descricao=form['descricao'].strip().lower(),
                status=form['status'].strip().upper(),
                inicio=datetime.strptime(form['inicio'], '%d/%m/%Y'),
                fim=datetime.strptime(form['fim'], '%d/%m/%Y'),
                created=datetime.now())
            questionario.save(force_insert=True)

            flash('Questionário Cadastrado')
        # error = 'Usuário ou senha incorretos, tente novamente'
        questionarios = Questionario.select().order_by(Questionario.created.desc())
        return object_list('list_questionarios.html', questionarios, 'list', titulo="Questionários")
    else:
        query = f"select q.ano || ' - ' || q.titulo, count(*) from questionario q join pessoa p on q.id=p.questionario_id group by q.id;"
        respostas_by_ano = db.execute_sql(query).fetchall()
        respostas = []
        for res in respostas_by_ano:
            respostas.append({'axis': res[0], 'value': res[1]})

        query = f"select c.nome, count(*) from questionario q join pessoa p on q.id=p.questionario_id join cargo c on c.id=p.cargo_id group by p.cargo_id;"
        cargo_by_respostas = db.execute_sql(query).fetchall()
        cargo = []
        for res in cargo_by_respostas:
            cargo.append({'axis': res[0], 'value': res[1]})

        gerais = []
        questionarios = Questionario.select().order_by(Questionario.created.desc())

        for quest in questionarios:
            geral = filtrarAll(
                quest.ano, None, None, None)
            gerais.append(geral)

        return object_list('list_questionarios.html', questionarios, 'list', titulo="Questionários", gerais=gerais, respostas_by_ano=respostas, cargo_by_respostas=cargo)


@app.route('/panel/questionarios/<id_questionario>', methods=["GET", "DELETE"])
@acesso_required('admin')
def panel_questionario(id_questionario):
    if request.method == 'DELETE':
        try:
            id = int(request.args.get('questionario_id'))

            obj = Questionario.get(Questionario.id == id)
            obj.delete_instance()

            qry = Resposta.delete().where(Resposta.questionario_id == id)
            qry.execute()

            flash('Questionário removido com sucesso!', "alert-danger")
            return "item removido"
        except:
            flash('Erro ao remover questionário!', "alert-danger")
            return "item removido"
    else:
        questionario = Questionario.select().where(
            Questionario.id == id_questionario).order_by(Questionario.created.desc())
        if len(questionario) > 0:
            questionario = questionario[0]
        return render_template('panel-questionario.html', questionario=questionario)
        # return object_list('panel-questionario.html', questionario, 'list', titulo="Questionário")


@app.route('/panel/perguntas')
@acesso_required('admin')
def panel_perguntas():
    perguntas = Pergunta.select().order_by(Pergunta.created.desc())
    return object_list('list_perguntas.html', perguntas, 'list', titulo="Perguntas")


@app.route('/panel/respostas')
@acesso_required('admin')
def panel_respostas():
    respostas = Resposta.select().join(Questionario).join(Pergunta).join(Grupo, on=(Grupo.id == Pergunta.grupo.id)).where(
        Resposta.pergunta_id == Pergunta.id and Resposta.questionario_id == Questionario.id).order_by(Grupo.ordem)
    return object_list('list_respostas.html', respostas, 'list', titulo="Respostas")
    # return object_list('list_respostas.html', respostas, 'list', titulo="Respostas", colunas=['titulo','pergunta','questionario','pessoa','created'])


@app.route('/panel/relatorio/<id_relatorio>')
@acesso_required('admin')
def panel_relatorio(id_relatorio):
    # return "Sem respostas"
    query_questionarios = Questionario.select(
        Questionario.id, Questionario.titulo, Questionario.fim).order_by(Questionario.created)
    questionarios = []
    for quest in query_questionarios:
        respostas = Resposta.select().join(Questionario).where(
            Resposta.questionario_id == quest.id).group_by(Resposta.pessoa)
        questionarios.append(
            {'titulo': quest.titulo, 'total': len(respostas), 'prazo': quest.fim})
    print(list(questionarios))
    return render_template('relatorio_respostas.html', list=questionarios, titulo="Respostas por Questionário")


# @app.route('/questionario/<form_id>/resposta/', methods=['POST'])
# def save_questionario_resposta(form_id):
#     pessoa = request.form['2']
#     respondeu = (Resposta.select().join(Questionario).where(
#         (Resposta.pessoa == pessoa) & (Questionario.id == int(form_id))))
#     if len(respondeu) > 0:
#         return render_template('alert.html', msg="Você já respondeu esse questionário!", tipo="danger")
#     for res in request.form.items():
#         resposta = Resposta()
#         resposta.pergunta_id = res[0]
#         resposta.valor = res[1]
#         resposta.questionario_id = form_id
#         resposta.pessoa = pessoa.strip().lower()
#         resposta.created = datetime.now()
#         resposta.save()
#     return render_template('alert.html', msg="Parabéns, Você respondeu ao questionário!", tipo="success")


@app.route('/questionarios')
def questionarios():
    questionarios = Questionario.select().where(Questionario.inicio >= datetime.now(
    ) and Questionario.fim >= datetime.now()).order_by(Questionario.created.desc())
    return object_list('questionarios.html', questionarios, 'list', titulo="Questionários disponíveis")


@app.route('/questionarios/<form_id>', methods=['GET', 'POST'])
def questionario(form_id):
    if request.method == 'POST':
        form = request.form
        email = form['email']
        respondeu = (Resposta.select().join(Questionario).join(Pessoa).where(
            (Pessoa.email == email) & (Questionario.id == int(form_id))))
        if len(respondeu) > 0:
            return render_template('alert.html', msg="Você já respondeu esse questionário!", tipo="danger")

        pessoa = Pessoa(
            nome=form['nome'].strip().lower(),
            email=form['email'].strip().lower(),
            genero=form['genero'],
            idade=form['idade'],
            tempo=form['tempo'],
            escolaridade=form['escolaridade'],
            experiencia=form['experiencia'],
            formacaoInovacao=form['formacaoInovacao'],
            unidade=Unidade.get_by_id(form['unidade']),
            area=Area.get_by_id(form['area']),
            cargo=Cargo.get_by_id(form['cargo']),
            questionario=Questionario.get_by_id(form_id),
            created=datetime.now())

        pessoa.save(force_insert=True)

        # id_pessoa = Pessoa.select(Pessoa.email == pessoa.email).get()
        for res in request.form.items():
            if (len(res[0]) < 3):
                # try:
                resposta = Resposta(
                    valor=str(res[1]),
                    pergunta=Pergunta.get_by_id(res[0]),
                    questionario_id=Questionario.get_by_id(form_id),
                    pessoa=Pessoa.get_by_id(pessoa.id),
                    created=datetime.now())
                resposta.save(force_insert=True)
                # except:
                #     Pessoa.delete_by_id(id_pessoa)
        return render_template('alert.html', msg="Parabéns, Você respondeu ao questionário!", tipo="success")

    else:
        questionario = Questionario.select().where(Questionario.id == int(form_id)
                                                   ).where(Questionario.inicio >= datetime.now(
                                                   ) and Questionario.fim >= datetime.now()).order_by(Questionario.created.desc())
        if len(questionario) > 0:
            questionario = questionario[0]

        unidades = Unidade.select()
        areas = Area.select()
        cargos = Cargo.select()
        return render_template('questionario.html', questionario=questionario, unidades=unidades, areas=areas, cargos=cargos, total_grupos=len(questionario.grupos())+2)


def sanitiza(dado):
    return "'"+str(dado).replace(",", "','")+"'"


@app.route('/verificar-resposta')
def verificarQuestionarioJaRespondido():
    questionario = request.args.get('questionario')
    email = request.args.get('email')
    print(questionario, email)
    if questionario and email:
        pessoa = Pessoa.select().where(
            Pessoa.questionario_id == questionario).where(Pessoa.email == email)
        if pessoa:
            return jsonify({'msg': 'true'})
    return jsonify({'msg': 'false'})


@app.route('/filtro')
def filtro():
    ano = request.args.get('ano')
    unidade = request.args.get('unidade')
    area = request.args.get('area')
    cargo = request.args.get('cargo')

    if ano:
        # ano = sanitiza(ano) if ano else None
        ano = ano if ano else None
    else:
        ano = str((datetime.today().year))
    unidade = sanitiza(unidade) if unidade else None
    area = sanitiza(area) if area else None
    cargo = sanitiza(cargo) if cargo else None

    lista, geral, dados_cargo, dados_area, dados_esco = filtrar(
        ano, unidade, area, cargo)

    final = {'lista': lista, 'geral': geral, 'dados_cargo': dados_cargo,
             'dados_area': dados_area, 'dados_esco': dados_esco}
    return jsonify(final)

    return render_template('public.html', data=lista)


def filtrar(ano, unidade, area, cargo):
    dimensoes = Dimensao.select()

    anos = sanitiza(ano)

    dim_chart_geral = []
    dim_chart_unidades = []
    unidades = []
    if not unidade:
        unidades = Resposta.select(fn.Distinct(Unidade.sigla)).join(Questionario).join(Pessoa).join(
            Unidade, on=(Unidade.id == Pessoa.unidade)).where(Questionario.ano << ano.split(','))
        for un in unidades:
            dim_chart_unidades.append({'sigla': un.sigla, 'axes': []})
    else:
        unidades = db.execute_sql(
            f'select * FROM unidade where id in ({unidade})').fetchall()
        for un in unidades:
            dim_chart_unidades.append({'sigla': un[1], 'axes': []})
    # chart_area = Resposta.select(fn.Distinct(Area.nome)).join(Questionario).join(Pessoa).join(
    #     Area, on=(Area.id == Pessoa.area)).where(Questionario.ano << ano.split(','))

    # chart por Cargo
    dim_chart_cargo = []
    query_cargo = f'select c.nome, count(*) from pessoa pe join questionario q on q.id=pe.questionario_id join cargo c on c.id = pe.cargo_id where q.ano in ({anos})'

    if unidade:
        query_cargo += f" and pe.unidade_id in ({unidade})"
    if area:
        query_cargo += f" and pe.area_id in ({area})"
    if cargo:
        query_cargo += f" and pe.cargo_id in ({cargo})"

    query_cargo += ' group by pe.cargo_id;'
    res_cargo = db.execute_sql(query_cargo).fetchall()

    for row in res_cargo:
        dim = {}
        dim['axis'] = row[0]
        dim['value'] = int(row[1])
        dim_chart_cargo.append(dim)
    print('CARGOS', dim_chart_cargo)

    # chart por Area
    dim_chart_area = []
    query_area = f'select a.nome, count(*) from pessoa pe join questionario q on q.id=pe.questionario_id join area a on a.id = pe.area_id  where q.ano in ({anos})'

    if unidade:
        query_area += f" and pe.unidade_id in ({unidade})"
    if area:
        query_area += f" and pe.area_id in ({area})"
    if cargo:
        query_area += f" and pe.cargo_id in ({cargo})"

    query_area += ' group by pe.area_id;'
    res_area = db.execute_sql(query_area).fetchall()

    for row in res_area:
        dim = {}
        dim['axis'] = row[0]
        dim['value'] = int(row[1])
        dim_chart_area.append(dim)

    # chart por escolaridade
    dim_chart_esco = []
    query_esco = f'select DISTINCT pe.escolaridade , count(*) from pessoa pe join questionario q on q.id=pe.questionario_id where q.ano in ({anos})'

    if unidade:
        query_esco += f" and pe.unidade_id in ({unidade})"
    if area:
        query_esco += f" and pe.area_id in ({area})"
    if cargo:
        query_esco += f" and pe.cargo_id in ({cargo})"

    query_esco += ' group by pe.escolaridade;'
    res_esco = db.execute_sql(query_esco).fetchall()

    for row in res_esco:
        dim = {}
        dim['axis'] = row[0]
        dim['value'] = int(row[1])
        dim_chart_esco.append(dim)

    for dimensao in dimensoes:
        dim = {}
        query_geral = f'select COALESCE(AVG(r.valor),0.00) FROM resposta r join questionario q on q.id = r.questionario_id join pergunta p on p.id = r.pergunta_id join grupo g on g.id = p.grupo_id join pessoa pe on pe.id = r.pessoa_id where q.ano in ({anos}) and g.dimensao_id = {dimensao.id}'

        if unidade:
            query_geral += f" and pe.unidade_id in ({unidade})"
        if area:
            query_geral += f" and pe.area_id in ({area})"
        if cargo:
            query_geral += f" and pe.cargo_id in ({cargo});"

        valor = db.execute_sql(query_geral).fetchone()

        dim['axis'] = dimensao.titulo
        dim['value'] = round(float(valor[0]), 1)
        dim_chart_geral.append(dim)

        query = f'select un.sigla,	COALESCE(AVG(r.valor), 0.00) FROM resposta r join pessoa pe on pe.id = r.pessoa_id join unidade un on un.id = pe.unidade_id join questionario q on q.id = r.questionario_id join pergunta p on p.id = r.pergunta_id join grupo g on g.id = p.grupo_id where q.ano in ({anos}) and g.dimensao_id = {dimensao.id}'
        if unidade:
            query += f" and un.id in ({unidade})"
        if area:
            query += f" and pe.area_id in ({area})"
        if cargo:
            query += f" and pe.cargo_id in ({cargo})"
        query += ' group by un.id;'
        resultado = db.execute_sql(query)

        for row in resultado.fetchall():
            for u in dim_chart_unidades:
                if u['sigla'] == row[0]:
                    u[dimensao.titulo] = round(float(row[1]), 1)
                    u['axes'].append(
                        {"axis": dimensao.titulo, "value": round(float(row[1]), 1)})
    dim_chart_geral = [{'axes': dim_chart_geral}]
    return dim_chart_unidades, dim_chart_geral, dim_chart_cargo, dim_chart_area, dim_chart_esco


def filtrarAll(ano, unidade, area, cargo):
    dimensoes = Dimensao.select()

    ano = str(ano)

    dim_chart_geral = []
    for dimensao in dimensoes:
        dim = {}
        query_geral = f'select COALESCE(AVG(r.valor),0.00) FROM resposta r join questionario q on q.id = r.questionario_id join pergunta p on p.id = r.pergunta_id join grupo g on g.id = p.grupo_id join pessoa pe on pe.id = r.pessoa_id where q.ano in ({ano}) and g.dimensao_id = {dimensao.id};'

        valor = db.execute_sql(query_geral).fetchone()

        dim['axis'] = dimensao.titulo
        dim['value'] = round(float(valor[0]), 1)
        dim_chart_geral.append(dim)

    dim_chart_geral = {'axes': dim_chart_geral}
    print('dadpsGerais', dim_chart_geral)
    return dim_chart_geral


@app.route('/')
def index():
    ano_questionarios = Questionario.select(
        Questionario.ano).group_by(Questionario.ano)
    unidades = Unidade.select()
    areas = Area.select()
    cargo = Cargo.select()
    lista, geral, dados_cargo, dados_area, dados_esco = filtrar(
        '2022', None, None, None)
    return render_template('public.html', data=lista, geral=geral, dados_cargo=dados_cargo, dados_area=dados_area, dados_esco=dados_esco, unidades=unidades, areas=areas, ano_questionarios=ano_questionarios, cargo=cargo)


@app.route('/error')
def error():
    return render_template('alert.html', msg="Acesso não permitido", tipo="danger")


if __name__ == '__main__':

    if resetar_db:
        create_tables()
    app.run(debug=debug, host='0.0.0.0', port=8087)
