# Módulo NameSearch
Pasta de construção do módulo NameSearch (Python), com recurso ao flit.

Receita:

1. Atualizar .py na pasta NameSearch (abrir __init__.py e atualizar versão).
2. $ flit build                         <-- construir instalação na pasta dist/ >
3. $ pip install .                      <-- instalar NameSearch no meu sistema, posicionado na pasta deste README.md>
4. Testar teste/tst.py


# Pastas

- dist: Pasta que o flit cria com os ficheiros de instalação wheel e tar.gz.
- NameSearch: Pasta das fontes.
  - __init__.py -- módulo de entrada, originalmente myNames.py
- teste: Testes ao módulo depois de instalado (`pip install .`).


# Ferramentas

## Flit
Cf. PyPI --> $ pip install -U flit
Para criar um projeto novo: $ flit init
Documentação flit: https://flit.readthedocs.io/_/downloads/en/latest/pdf/

(Para publicar o módulo no PyPI, com credenciais: $ flit publish)
