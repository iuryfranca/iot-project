# Gerenciamento de Gado com RFID

Este projeto tem como objetivo criar um site simples para o gerenciamento de gado e controle de animais utilizando RFID. Ele permite que fazendeiros e gerentes controlem dados essenciais sobre os animais de forma prática e organizada.

## Tecnologias Utilizadas

- **Python**: Linguagem principal do backend.
- **Django**: Framework web utilizado para o desenvolvimento do backend.
- **Tailwind CSS**: Framework CSS para estilização rápida e responsiva do frontend.

## Funcionalidades

1. **Login**: Sistema de autenticação seguro para acesso de usuários autorizados.
2. **Dashboard**: Exibe um painel com as principais informações e estatísticas dos animais cadastrados.
3. **Cadastro de Gado**: Permite o registro e o controle de informações individuais dos animais, incluindo identificação por RFID.
4. **Gerenciamento de Vacinação**: Controle completo do histórico de vacinas, com agendamento e alertas de vacinação.
5. **Gerenciamento de Maternidade**: Registro e acompanhamento do histórico reprodutivo e de maternidade dos animais.

## Como Executar o Projeto

### Pré-requisitos

- Python 3.x
- Django
- Node.js e npm (para compilação do Tailwind CSS)

### Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu_usuario/nome_do_projeto.git

   ```

2. Instale as dependências do Python:

   ```bash
   pip install -r requirements.txt

   ```

3. Instale e configure o Tailwind CSS seguiindo esses passos [Como instalar Tailwind CSS no Django](https://django-tailwind.readthedocs.io/en/latest/installation.html)

### Executando o Projeto

1. Aplique as migrações do Django:

   ```bash
   python manage.py migrate

   ```

2. Inicie o servidor de desenvolvimento:

   ```bash
   python manage.py runserver

   ```

3. Inicie o servidor de CSS do tailwind:

   ```bash
   npx tailwindcss -i ./static/src/input.css -o ./static/src/output.css --watch

   ```

### Agadecimentos

Este projeto foi desenvolvido com o objetivo de ser uma solução prática e fácil de usar para gerenciamento de gado e controle de animais utilizando RFID.
