# GPU Monitor

Um aplicativo distribuído para monitoramento de GPUs em rede local usando Zeroconf para descoberta automática de serviços.

## Características

- Monitoramento em tempo real de GPUs NVIDIA
- Descoberta automática de serviços na rede local
- Interface gráfica para servidor e cliente
- Exibição de informações como:
  - Nome da GPU
  - Utilização (%)
  - Memória utilizada/total
  - Temperatura

## Pré-requisitos

- Python 3.7+
- NVIDIA GPU (para o servidor)
- Bibliotecas Python listadas em `requirements.txt`

## Instalação

1. Clone o repositório:

```bash
git clone [nome_respositório]
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Uso

### Executando o Servidor

O servidor deve ser executado na máquina que possui a GPU que você deseja monitorar:

```bash
python src/main.py -s
```

### Executando o Cliente

O cliente pode ser executado em qualquer máquina na mesma rede local:

```bash
python src/main.py -c
```

## Estrutura do Projeto

```
gpu_monitor/
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── server/
│   │   ├── __init__.py
│   │   └── gpu_server.py
│   ├── client/
│   │   ├── __init__.py
│   │   └── gpu_client.py
│   └── main.py
```
