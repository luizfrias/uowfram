## UOWfram

Django Project designed for MAB225 discipline.

Este projeto foi criado para a disciplina de computação 2 (MAB225) da UFRJ.

Autores:

* Héron Henrique Martins Silva
* Luiz Fernando C. P. de Frias

## Instalação

Para instalar o projeto, você deve seguir os seguintes passos

```
# Criar um virtualenv
$ pip install virtualenv # Caso não tenha instalado
$ mkdir trabalho-comp2 && cd trabalho-comp2
$ virtualenv --no-site-packages env
# Ativa o virtualenv
$ source env/bin/activate 
```

Agora que você tem o virtualenv instalado, baixe este projeto onde preferir e entre na pasta.
Com o virtualenv ativado, rode:

```
$ pip install -r requirements.txt
```

Isso vai instalar todos os pacotes necessários para o projeto funcionar.
Para ver o projeto funcionando:

```
$ ./manage.py runserver
```

Esse comando inicializa um servidor local que pode ser acessado através do seguinte endereço: 127.0.0.1:8000

Pronto, agora é só usar o sistema =]

