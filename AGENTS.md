# AGENTS.md — Instruções rápidas para AI coding agents

Propósito: orientar agentes de IA (Copilot/JIT helpers) para trabalhar eficazmente neste repositório.

Resumo curto
- Projeto: `Back-da-dev` (pacote público `back_da_dev`).
- Objetivo do agente: executar mudanças pequenas e seguras, rodar testes e preparar patches.

Comandos rápidos (recomendado para agentes e humanos)

```bash
# criar e ativar venv (Linux/macOS)
python -m venv .venv
source .venv/bin/activate

# instalar dependências
python -m pip install -r requirements.txt
python -m pip install -e .

# rodar testes
pytest -q

# executar CLI (ajuda)
python -m back_da_dev --help
# ou rodar direto do código-fonte sem instalar:
PYTHONPATH=src python3 -m back_da_dev --help
```

O que o agente deve fazer antes de propor mudanças
- Executar a suíte de testes localmente: `pytest -q`.
- Executar o teste de empacotamento quando alterar metadados / packaging: `python -m pip wheel . -w /tmp/wheel --no-deps` (usado pelos testes em `tests/test_packaging.py`).
- Sempre preferir pequenos commits e patches atômicos (use `apply_patch` ou equivalente).
- Linkar documentação relevante em PRs: [README.md](README.md), [project.md](project.md), [fluxogram.md](fluxogram.md).

Onde olhar primeiro
- Código-fonte público: `src/back_da_dev` (exporta a API pública).
- Implementação e engine: `src/backtesting/backtesting_main.py` e `src/backtesting/modelos_pre_implementados.py`.
- Carregamento/limpeza de dados: `src/dataprocessing/load.py` e `src/dataprocessing/clean.py`.
- Tests: [tests](tests) — inclui testes de import, empacotamento e comportamento do engine.
- Dados de exemplo: `data/historical_data/` (muito grandes — não baixar automaticamente).

Conselhos práticos e convenções
- Layout de pacote: usa `src/` como raiz de código. Preserve esse layout ao modificar imports.
- Python target: `>=3.11` (veja `pyproject.toml`).
- Evite commitar dados brutos grandes. Prefira gerar pequenos fixtures de teste sob `tests/fixtures` quando necessário.
- Se mexer em CLI ou empacotamento, garanta que `python -m back_da_dev --help` funcione.

Quando pedir revisão humana
- Mudanças que afetam design de API, contratos ou o formato de saída (`.log`, CSV, JSON) devem ser sinalizadas e revisar com um mantenedor.

Contato e documentação
- Leia o README primeiro: [README.md](README.md).
- Documentação de projeto e arquitetura: [project.md](project.md) e [fluxogram.md](fluxogram.md).

---
Arquivo gerado automaticamente para acelerar agentes de programação. Peça alterações se precisar de mais regras específicas.
