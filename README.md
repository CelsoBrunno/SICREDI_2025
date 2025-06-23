# Sistema de Gestão Sicredi

Sistema de gestão desenvolvido em Python/Flask para controlar reservas de equipamentos e ambientes da Sicredi.

## 📋 Funcionalidades

### Para Gestores

- **Gerenciar Analistas**: Criar, editar, ativar/desativar analistas
- **Gerenciar Ambientes**: Cadastrar e administrar salas e ambientes
- **Gerenciar Equipamentos**: Controlar equipamentos mobilizados e imobilizados
- **Aprovar Reservas**: Aprovar ou rejeitar solicitações de reserva
- **Dashboard**: Visualizar estatísticas e resumo do sistema

### Para Analistas

- **Reservar Equipamentos**: Solicitar reserva de equipamentos disponíveis
- **Acessar Ambientes**: Solicitar reserva de salas e ambientes
- **Acompanhar Reservas**: Visualizar status das suas solicitações
- **Dashboard**: Ver resumo das suas reservas

## 🏗️ Estrutura do Projeto

```
sicredi/
├── app/
│   ├── db/
│   │   ├── database.py          # Configuração do banco SQLite
│   │   └── sicredi.db          # Banco de dados (criado automaticamente)
│   ├── main/
│   │   ├── gestor.py           # Lógica de negócio do gestor
│   │   └── analista.py         # Lógica de negócio do analista
│   ├── routes/
│   │   ├── gestor.py           # Rotas antigas (não usadas)
│   │   └── analista.py         # Rotas antigas (não usadas)
│   └── utils/
│       └── auth.py             # Sistema de autenticação
├── templates/
│   ├── Gestor/
│   │   ├── dashboard.html      # Dashboard do gestor
│   │   ├── GerenciarAnalistas/ # Templates para gerenciar analistas
│   │   ├── GerenciarAmbientes/ # Templates para gerenciar ambientes
│   │   ├── GerenciarReservas/  # Templates para gerenciar reservas
│   │   ├── EquipamentosMobilizados/    # Templates equipamentos mobilizados
│   │   └── EquipamentosImobilizados/   # Templates equipamentos imobilizados
│   ├── Analista/
│   │   ├── dashboard.html      # Dashboard do analista
│   │   ├── ReservaEquipamento/ # Templates para reservar equipamentos
│   │   └── AcessoAmbientes/    # Templates para acessar ambientes
│   ├── index.html              # Página inicial
│   ├── login.html              # Página de login
│   └── error.html              # Página de erro
├── static/
│   ├── css/                    # Arquivos CSS
│   ├── js/                     # Arquivos JavaScript
│   └── img/                    # Imagens
├── run.py                      # Arquivo principal da aplicação
├── requirements.txt            # Dependências do projeto
└── README.md                   # Este arquivo
```

## 🚀 Como Executar

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Inicializar Banco de Dados

```bash
python app/db/database.py
```

### 3. Executar a Aplicação

```bash
python run.py
```

### 4. Acessar o Sistema

Abra o navegador e acesse: `http://localhost:5000`

## 👤 Usuários do Sistema

### Gestor Padrão

- **Email**: gestor@sicredi.com
- **Senha**: gestor2025

### Analistas

Os analistas devem ser criados pelo gestor através do sistema.

## 🗄️ Banco de Dados

O sistema utiliza SQLite com as seguintes tabelas:

### usuarios

- Armazena gestores e analistas
- Campos: id, nome, email, senha (criptografada), tipo, ativo, datas

### ambientes

- Armazena salas e ambientes disponíveis
- Campos: id, nome, descrição, capacidade, equipamentos, ativo, datas

### equipamentos

- Armazena equipamentos mobilizados e imobilizados
- Campos: id, nome, descrição, tipo, código_patrimônio, status, localização, ativo, datas

### reservas

- Armazena todas as reservas (equipamentos e ambientes)
- Campos: id, usuario_id, equipamento_id, ambiente_id, data_inicio, data_fim, status, observações, datas

### sessoes

- Controla sessões ativas dos usuários
- Campos: id, usuario_id, token, data_expiracao, ativo, data_criacao

## 🔐 Sistema de Autenticação

- **Senhas**: Criptografadas com SHA-256
- **Sessões**: Controladas com tokens únicos
- **Expiração**: Sessões válidas por 8 horas
- **Permissões**: Decorators para controlar acesso (login_required, gestor_required, analista_required)

## 📊 Status de Reservas

- **pendente**: Aguardando aprovação do gestor
- **aprovada**: Aprovada pelo gestor
- **rejeitada**: Rejeitada pelo gestor
- **cancelada**: Cancelada pelo analista

## 🛠️ Status de Equipamentos

- **disponivel**: Disponível para reserva
- **reservado**: Reservado por algum usuário
- **manutencao**: Em manutenção
- **indisponivel**: Indisponível por outros motivos

## 🎨 Interface

- **Framework CSS**: Tailwind CSS
- **Fonte**: Inter (Google Fonts)
- **Cores**: Paleta da Sicredi (verde #3b8114, #64c832)
- **Responsivo**: Design adaptativo para diferentes telas

## 📝 Comentários no Código

Todo o código Python está comentado explicando:

- Função de cada método
- Parâmetros esperados
- Valores de retorno
- Lógica de negócio implementada

## 🚨 Importantes

- **Não altere** os templates com nome "teste.html" - são apenas cópias para referência
- O sistema automaticamente cria dados de exemplo ao inicializar o banco
- Todas as reservas precisam de aprovação do gestor
- Analistas só podem ver e gerenciar suas próprias reservas

## 📞 Suporte

Para dúvidas ou problemas, verifique:

1. Se todas as dependências estão instaladas
2. Se o banco de dados foi inicializado corretamente
3. Se a porta 5000 está disponível
4. Os logs no terminal para mensagens de erro

---

**Desenvolvido com ❤️ para a Sicredi**
