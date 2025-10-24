Foqus - Planeamento Adaptativo de Estudos para o ENEM

1. Visão do Projeto

Este repositório contém o código-fonte do Foqus, uma plataforma web inteligente de planeamento de estudos, desenvolvida como um Trabalho de Conclusão de Curso (TCC) em Engenharia da Computação.

O Exame Nacional do Ensino Médio (ENEM) representa um desafio significativo de planeamento para milhões de estudantes anualmente. Ferramentas genéricas de organização mostram-se ineficazes por serem passivas e não incorporarem estratégias de otimização.

O Foqus resolve este problema ao automatizar a criação de planos de estudo adaptativos. Utiliza um modelo computacional embasado em ferramentas de gestão da qualidade (como o Diagrama de Pareto) para priorizar conteúdos de alta incidência e integra uma Inteligência Artificial (Google Gemini) para atuar como um tutor, diagnosticar dificuldades e adaptar o plano ao desempenho do estudante. A ferramenta visa transformar o planeamento de estudos num processo dinâmico e estratégico, reduzindo a carga cognitiva do utilizador e maximizando o seu desempenho.

2. Funcionalidades Principais

Backend (API RESTful):

Autenticação por Token: Sistema de registo, login e logout seguro (Django REST Framework).

"Cérebro" de Pareto (services.py): Algoritmo que gera um cronograma dinâmico baseado na incidência de cada assunto no ENEM.

Tutor de IA (ai_services.py): Integração com a API do Google Gemini para simplificar tópicos, gerar questões e tirar dúvidas.

Seeder de IA: Um comando de gestão (popular_base) que usa a IA para popular o banco de dados com os tópicos mais recentes do ENEM.

Endpoints de Progresso: API que calcula e retorna estatísticas de desempenho (PerfilStatsSerializer).

Frontend (SPA):

Fluxo de Onboarding: Um assistente passo-a-passo para configurar as metas do utilizador (data da prova, horas/dia).

Dashboard Diário: Apresenta as tarefas do dia geradas pelo algoritmo de Pareto.

Sessão de Foco: Ecrã com Timer Pomodoro funcional e acesso direto ao Tutor de IA.

Página de Progresso: Dashboard com estatísticas visuais do desempenho do utilizador por matéria.

Gestão de Dados Profissional: Utiliza TanStack Query para gerir o estado da API (caching, loading, errors).

Roteamento Protegido: Separação clara entre rotas públicas (Login) e privadas (Dashboard).

3. Stack Tecnológico

# Backend
Python, Django, Django REST Framework

# Frontend
Next.js 14, React 18, TypeScript

# Base de Dados
SQLite (para desenvolvimento)

# API
RESTful (com axios no frontend)

# Estilização
Tailwind CSS


# Gestão de Estado (Frontend)
TanStack Query (React Query)

# Inteligência Artificial
Google Gemini API

4. Estrutura do Repositório

O projeto segue uma estrutura de monorepo-like, separando o backend e o frontend em pastas distintas na raiz.

foqus/
├── backend/         # 📂 API em Django REST Framework
│   ├── core/        # (A nossa app principal)
│   ├── backend/     # (Configurações do projeto)
│   ├── manage.py
│   └── requirements.txt
├── frontend/        # 📂 Aplicação em Next.js / React
│   ├── src/
│   ├── package.json
│   └── next.config.ts
├── venv/            # 📂 Ambiente virtual do Python (ignorado)
└── .gitignore       # (Ignora venv/, node_modules/, .env, etc.)


5. Como Executar o Projeto (Ambiente de Desenvolvimento)

É necessário ter o Python 3.10+ e o Node.js 18+ instalados.

5.1. Backend (Django)

Abra um terminal (Terminal 1).

Navegue para a pasta raiz do projeto:

cd /caminho/para/foqus


Crie (se ainda não existir) e ative o ambiente virtual:

python3 -m venv venv
source venv/bin/activate


Navegue para a pasta do backend:

cd backend


Instale as dependências do Python:

pip install -r requirements.txt


Configure o .env:

Na pasta raiz (foqus/), crie um ficheiro .env.

Adicione as suas chaves (veja backend/settings.py para todas as variáveis):

SECRET_KEY="sua-chave-secreta-django-aqui"
GOOGLE_API_KEY="sua-chave-api-google-gemini-aqui"


Crie e Popule a Base de Dados:

# Cria as tabelas
python manage.py migrate

# Crie o seu utilizador administrador
python manage.py createsuperuser

# Use a IA para popular as Matérias e Assuntos
python manage.py popular_base


Inicie o servidor Backend:

python manage.py runserver


O backend estará a rodar em http://127.0.0.1:8000.

5.2. Frontend (Next.js)

Abra um SEGUNDO terminal (Terminal 2).

Navegue para a pasta do frontend:

cd /caminho/para/foqus/frontend


Instale as dependências do Node.js:

npm install


Inicie o servidor Frontend:

npm run dev
