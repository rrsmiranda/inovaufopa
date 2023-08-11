***PREPARAR PROJETO

secret-key
```cmd
openssl rand -base64 63
```

Install dependencias do projeto
```cmd
python3 -m venv venv
pip install -r requirements.txt

sudo apt install sqlite3
```


***CRIAR BANCO
user: admin
senha admin
```cmd
cd infra
sqlite3 base.db
INSERT INTO USER (USERNAME, PASSWORD,EMAIL,PERMISSAO,CREATED) VALUES ('admin', 'c7ad44cbad762a5da0a452f9e854fdc1e0e7a52a38015f23f3eab1d80b931dd472634dfac71cd34ebc35d16ab7fb8a90c81f975113d6c7538dc69dd8de9077ec','admin@mail.com','admin','2022-04-03 22:49:38.208686');
INSERT INTO USER (USERNAME, PASSWORD,EMAIL,PERMISSAO,CREATED) VALUES ('usuario', 'd9e94fd2b4c5522e5bb7996aa4df48a3f6b8f1b0c3e7fadb5fcc724e3ab6d85dc401b0a2789fe56c209b80e86102b218ff74ff8614f315599a180691846138b6','usuario@mail.com','usuario','2022-04-03 22:49:38.208686');

INSERT INTO QUESTIONARIO (TITULO,ANO,DESCRICAO, CREATED) VALUES ('MENSURACAO DA INOVAÇÃO EM SETORES DA UFOPA','2022','A Mensuração da Cultura de Inovação mede a maturidade do desenvolvimento de uma instituição o caminho rumo à inovação. Provendo um diagnóstico dos pontos fortes e das lacunas da instituição, e oferece uma orientação aos gestoes para tomarem medidas concretas com o fim de criarem e melhorarem uma cultura de inovação. Esta avaliação consiste em 54 perguntas fechadas e uma avaliação final. ','2022-04-03 22:49:38.208686');

INSERT INTO PERGUNTA (TITULO,QUESTIONARIO_ID,TIPO,CREATED) VALUES ('Nome',1,1,'2022-04-03 22:49:38.208686');
INSERT INTO PERGUNTA (TITULO,QUESTIONARIO_ID,TIPO,CREATED) VALUES ('EMAIL',1,1,'2022-04-03 22:49:38.208686');
INSERT INTO PERGUNTA (TITULO,QUESTIONARIO_ID,TIPO,CREATED) VALUES ('UNIDADE',1,2,'2022-04-03 22:49:38.208686');
INSERT INTO PERGUNTA (TITULO,QUESTIONARIO_ID,TIPO,CREATED) VALUES ('Profissao',1,2,'2022-04-03 22:49:38.208686');
INSERT INTO PERGUNTA (TITULO,QUESTIONARIO_ID,TIPO,CREATED) VALUES ('Genero',1,2,'2022-04-03 22:49:38.208686');
INSERT INTO PERGUNTA (TITULO,QUESTIONARIO_ID,TIPO,CREATED) VALUES ('O que acha de tal coisa?',1,3,'2022-04-03 22:49:38.208686');
INSERT INTO PERGUNTA (TITULO,QUESTIONARIO_ID,TIPO,CREATED) VALUES ('O que acha de outra coisa?',1,3,'2022-04-03 22:49:38.208686');

```
***Usando sha512 

```python
  import hashlib

  input = 'admin'
  hash = hashlib.sha512( str( input ).encode("utf-8") ).hexdigest()
  print(hash)
```

run
source venv/bin/activate
```cmd
  gunicorn --worker-tmp-dir /dev/shm -b 0.0.0.0:5001 --threads 1 app:app
```
