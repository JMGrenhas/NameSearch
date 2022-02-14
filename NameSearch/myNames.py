'''
  myNames.py - Biblioteca de tratamento de nomes de pessoas e empresas: normalização e pesquisa. Foco na grafia portuguesa.
  
  Na normalização, são feitas transformações que devem ser entendidas apenas com o racional de facilitar a procura.
'''
import re

from .jg_base_iter import (ApFP, ATail, ListaContidaEm, RemoveVaziosLista,
                              TiraDupEsp, camelCase2lowcase, strip_accents)

# Função parcial que transforma, numa grafia normalizada, palavras completas de nomes, se bem que em minúsculas e sem acentos.
# Racional: facilitar comparações em pesquisas.
# === Pares (key, value) para normalizar strings.
aFP_NameNorm1 = (("baptista", "batista"), ("joseph", "jose"), ("lourdes", "lurdes"),
                 ("manoel", "manuel"), ("manoela", "manuela"), ("victor", "vitor"))

# Função parcial que elimina partículas de ligação comuns. Preposições.
# Na normalização, serão substituídas depois de aFP_NameNorm1.
aFP_Prepo = (("e", ""), ("das", ""), ("dos", ""), ("de", ""),
             ("da", ""), ("do", ""), ("em", ""), ("na", ""), ("no", ""))

G_aPrepoDe = ["de", "da", "das", "do", "dos"]
G_aPrepo2 = ["e", "ou", "em", "na", "nas", "no", "nos"]
G_aPrepo = [] + G_aPrepoDe + G_aPrepo2

# === Grafemas substituídos para facilitar a procura, seja por grafia antiga ou por variantes de grafia.
# Notas:
#   - Alguns contemplados mais abaixo por aGrafemasRE, como "th".
#   - Carateres duplicados poderiam ser tratados por RemoveCarsDup(), mas esta tb. apanha coisas como numeração romana, ex: "ii" seria "i", etc.
aGrafemas = (("ck", "c"), ("k", "c"), ("ll", "l"), ("nn", "n"),
             ("ph", "f"), ("pp", "p"), ("y", "i"), ("z", "s"))


# === Grafemas por regex.
aGrafemasRE = []
# CUIDADO (Python 3.08): re.sub() não se dá bem com tuplos de tuplos/listas. Tem de ser lista de tuplos/listas.
# Palavras acabadas em "z" => "s". Ex.: "thomaz" => "thomas".
#aGrafemasRE = [[r"(\w+)z$", r"\1s"]]

# Palavras acabadas em "th" => "te". Ex.: "elisabeth", "lisbeth".
aGrafemasRE += [[r"(\w+)th$", r"\1te"]]
# Palavras com th e mais algum caráter, "th" => "t". Ex.: "Agatha" => "Agata"
aGrafemasRE += [[r"th(\w+)", r"t\1"]]

# Abreviaturas por tipo de arruamento (ou artéria), conforme recomendação CTT e mais algumas -- cf. https://pt.wikipedia.org/wiki/Lista_de_abreviaturas_recomendadas_pelos_CTT -- mas em minúsculas, sem acentos.
aAbrevArruamento = (("alameda", "al"), ("avenida", "av"), ("azinhaga", "az"),
                    ("bairro", "br"), ("beco", "bc"), ("calc", "cc"),
                    ("calcada", "cc"), ("calcadinha", "ccnh"), ("caminho", "cam"),
                    ("casa", "cs"), ("conjunto", "cj"),
                    ("escadas", "esc"), ("escadinhas", "escnh"),
                    ("estrada", "estr"),
                    ("jardim", "jd"), ("largo", "lg"),
                    ("lt", "lot"), ("loteamento", "lot"),
                    ("parque", "pq"), ("patio", "pat"),
                    ("pr", "pc"), ("praca", "pc"), ("praceta", "pct"),
                    ("prolongamento", "prl"), ("quadra", "qd"),
                    ("rotunda", "rot"), ("rua", "r"),
                    ("transversal", "transv"), ("trav", "tv"), ("travessa", "tv"),
                    ("urbanizacao", "urb"), ("vila", "vl"), ("zona", "zn"))

# Abreviaturas por tipo de alojamento, conforme recomendação CTT -- mas em minúsculas, sem acentos.
aAbrevAlojamento = (("cave", "cv"), ("direito", "dto"), ("esquerdo", "esq"),
                    ("frente", "ft"), ("fundos", "fds"),
                    ("habitacao", "hab"), ("loja", "lj"),
                    ("res-do-chao", "rc"), ("r/c", "rc"),
                    ("sobreloja", "slj"), ("subcave", "scv"))

# Abreviaturas por tipo de porta, conforme recomendação CTT -- mas em minúsculas, sem acentos.
aAbrevPorta = (("apartamento", "apto"), ("bloco", "bl"), ("edif", "edf"),
               ("edificio", "edf"), ("lote", "lt"), ("torre", "tr"), ("vivenda", "vv"))

# Abreviaturas por título, conforme recomendação CTT -- mas em minúsculas, sem acentos.
aAbrevTitulo = (("alferes", "alf"), ("almirante", "alm"), ("arquitecto",	"arq"),
                ("arquiteto",	"arq"), ("brigadeiro", "brig"), ("capitao",	"cap"),
                ("comandante", "cmdt"), ("comendador", "comend"),
                ("conselheiro", "cons"), ("coronel", "cel"), ("dom", "d"),
                ("doutor", "dr"), ("doutora", "dra"), ("duque", "dq"),
                ("embaixador", "emb"),
                ("engenheira", "enga"), ("engenheiro", "eng"),
                ("general", "gen"), ("infante", "inf"), ("marques", "mq"),
                ("presidente", "pres"),
                ("professor", "prof"), ("professora", "profa"),
                ("sao", "s"), ("santa", "sta"), ("santo", "sto"),
                ("sargento", "sarg"), ("tenente", "ten"), ("visconde", "visc"))

# Abreviaturas diversas, conforme recomendação CTT -- mas em minúsculas, sem acentos.
# "sem numero" => feita em NormGrafiaMorada()
aAbrevDivCtt = (("associacao", "ass"), ("instituto", "inst"), ("lugar", "lug"), ("ministerio", "min"),
                ("projetada", "proj"), ("sala", "sl"), ("s/n", "sn"), ("sociedade", "soc"), ("universidade", "univ"))


def Name_List_Search(acNameList: list, cSearch: str,
                     lGet1: bool = False, lInitials: bool = True) -> list:
    '''
    Efetua a procura numa lista de nomes, dado o nome de uma pessoa ou organização.
    Camada sobre Name_List_Search_unfolded, com os mesmos parâmetros, para simplificar resultado.
    Parms.:
      - acNameList: Lista de procura.
      - cSearch: Valor de procura.
      - [lGet1] (False): Indica se retorna logo após encontrar um valor.
      - [lInitials] (True): Indica se é permitida a unificação pelas iniciais (primeiro caráter) de cSearch. Só irá ocorrer esta pesquisa se cSearch, depois de normalizada, tiver mais de uma palavra. Lembre-se que a normalização retira certas palavras como "de", "da", etc..

    Resultado: Lista de cadeias de unificação.
    '''
    aTable1, aTable2, aPalPrc = Name_List_Search_unfolded(
        acNameList, cSearch, lGet1, lInitials)

    return aTable1 + aTable2


def Name_List_Search_unfolded(acNameList: list, cSearch: str,
                              lGet1: bool = False, lInitials: bool = True):
    '''
    Efetua a procura numa lista de nomes, dado o nome de uma pessoa ou organização. Retorna duas listas de unificação e uma de controlo.
    Parms.:
      - acNameList: Lista de procura.
      - cSearch: Valor de procura.
      - [lGet1] (False): Indica se retorna logo após encontrar um valor.
      - [lInitials] (True): Indica se é permitida a unificação pelas iniciais (primeiro caráter) de cSearch. Só irá ocorrer esta pesquisa se cSearch, depois de normalizada, tiver mais de uma palavra. Lembre-se que a normalização retira certas palavras como "de", "da", etc..

    Resultado:
      - aTable1: lista strings => tabela de unificação preferencial
      - aTable2: lista strings => tabela de unificação secundária, pela 1ª e última inicial.
      - aPalPrc:
          lGet1 = False => Lista de palavras normalizadas de cSearch que foram usadas na procura. Tipicamente, servirá para mostrar na janela de Debug.
          lGet1 = True => Lista de uma posição com o resultado eleito.
    '''
    aPalPrc = NormGrafiaNome_List(cSearch)
    # Há palavras != de preposições "de".
    lMaisNorm = bool(cSearch and aPalPrc)

    if not lMaisNorm:
        # cSearch só contém palavras descartadas pela normalização (ex.: "da").
        aPalPrc = NormGrafiaNome_List(cSearch, lMaisNorm)

    if not lInitials or not lMaisNorm:
        # Evitar demasiados resultados sem interesse.
        cIniciais = ""
        c1aUltIniciais = ""
    else:
        cIniciais, c1aUltIniciais = DaStrComIniciais(aPalPrc)

    # ---
    # Expressão regex para encontrar, mesmo que aPalPrc contenha abreviaturas ou iniciais.
    # Ex.: procurar "joao r silva" deverá encontrar "joao rodrigo silva".
    cPrc = r'.* '.join(aPalPrc)
    regex = re.compile(cPrc)  # , re.I)

    # ---
    found1 = found2 = found3 = found4 = None
    aTable1 = []
    aTable2 = []
    for cNome in acNameList:
        cNomeNorm = NormGrafiaNome_Str(cNome, lMaisNorm)

        if regex.search(cNomeNorm):  # Encontrou.
            # print(regex.search(cNomeNorm))
            aTable1.append(cNome)
            if lGet1:
                found1 = cNome
                break  # sai logo pq é a unificação mais forte
        else:
            acTestar = NormGrafiaNome_List(cNome, lMaisNorm)
            # A lista aPalPrc está contida em acTestar.
            # Racional: para o caso de haver palavras trocadas -- ex.: "joao grenhas manuel".
            if ListaContidaEm(aPalPrc, acTestar):
                aTable1.append(cNome)
                if lGet1:
                    found2 = cNome

            # Todas as iniciais das palavras escolhidas coincidem. Ex.: Procurar "joao regado grenhas".
            elif cIniciais and cIniciais == " ".join(DaIniciaisLista(acTestar)):
                aTable1.append(cNome)
                if lGet1:
                    found3 = cNome

            # As iniciais escolhidas coincidem.
            elif c1aUltIniciais and c1aUltIniciais == " ".join(Da1aUltIniciais(acTestar)):
                aTable2.append(cNome)
                if lGet1:
                    found4 = cNome
    if lGet1:
        if found1:
            aPalPrc = [found1]
        elif found2:
            aPalPrc = [found2]
        elif found3:
            aPalPrc = [found3]
        elif found4:
            aPalPrc = [found4]
        else:
            aPalPrc = None

    # O resultado é um tuplo mesmo no caso lGet1, pq o linter confunde-se com funções a retornarem coisas muito diferentes...
    return aTable1, aTable2, aPalPrc


def RemoveCarsDup(cStr: str):
    '''
    Remove carateres alfabéticos replicados, consecutivos, duma string.
    Não age sobre dígitos.
    '''
    if not cStr:
        return cStr

    cOut = cStr[0]
    for nI in range(1, len(cStr)):
        # Se for diferente do anterior, adiciona.
        if not cStr[nI].isalpha() or cStr[nI] != cStr[nI-1]:
            cOut += cStr[nI]

    return cOut


def NormGrafiaID(cID, lTira_d: bool = False):
    '''
    Retorna uma lista de palavras entre espaços, ou uma string, com grafia normalizada para comparações.
    Parâmetros:
      - cID: String contendo um ID. Pode começar por ":".
      - [lTira_d] (False): Indica se retira a última palavra caso seja começada por "d" e um dígito. Motivo: ajudar a pesquisa por iniciais, em que o "d" iria iludir como inicial de nome.
    '''
    # Normalizar cID:
    n2p = cID.find(":")  # Procurar prefixo.
    if n2p != -1:  # => Descartar prefixo.
        cID = cID[n2p+1:]  # Tira ":" e o que está antes.

    cID = cID.lower()
    cID = strip_accents(cID)

    cID = cID.replace("_", " ")
    cID = cID.replace("-", " ")

    # Separar palavras de cID:
    aWord = cID.split(' ')
    if aWord:
        if lTira_d:
            # Retirar último termo se começar por "d" e for seguido de dígitos (convenção para indicar um ano ou data de nascimento, esta sem "-" pelo meio).
            cTail = ATail(aWord)
            # Nos ID da classe Pessoa, indica a data de nascimento
            if cTail and len(cTail) >= 2 and cTail[0] == "d" and cTail[1].isdigit():
                aWord.pop()
        else:
            cTail = ATail(aWord)
            # Tratar grupos (regex=>) "d?99xx".
            cTail = NormDtNasc(cTail, lProtegePto=True, lTiraCarD=False)

            if cTail != ATail(aWord):  # Ocorreu normalização => assumir.
                aWord[len(aWord)-1] = cTail

        aWord = NameNorm_List(aWord)
        # *******************
        # Repõe pontos protegidos em NormDtNasc(cTail, lProtegePto=True, lTiraCarD=False)
        if not lTira_d:
            for n in range(0, len(aWord)):
                aWord[n] = aWord[n].replace("<%>", ".")
    return aWord


def NameNorm_List(acStr: list, lRuas: bool = False, lMaisNorm: bool = True) -> list:
    '''
    Retorna uma lista de palavras, numa grafia normalizada para comparações (converte nomes antigos ou com estrangeirismos, etc.).
    Parâmetros:
      - acStr: Lista de palavras, possivelmente referente a nomes de pessoas.
      - [lRuas] (False): Indica se estamos a normalizar nomes de ruas.
    '''
    '''
    Notas:
      - Ver tb. NameNorm_Str().
    '''
    acStr = _NameNormList(acStr, lRuas, lMaisNorm)

    acStr = RemoveVaziosLista(acStr)  # Acabamento
    return acStr


def NameNorm_Str(acStr: list, lRuas: bool = False, lMaisNorm: bool = True):
    '''
    Retorna uma string (sem duplo espaçamento), com nomes de pessoas, numa grafia normalizada para comparações (converte nomes antigos ou com estrangeirismos).
    Parâmetros:
      - acStr: Lista de strings.
      - [lRuas] (False): Indica se estamos a normalizar nomes de ruas.
    '''
    '''
    Notas:
      - Ver tb. NameNorm_List.
    '''
    acStr = _NameNormList(acStr, lRuas, lMaisNorm)

    cStr = TiraDupEsp(" ".join(acStr))  # Acabamento
    return cStr


def _NameNormList(acStr: list, lRuas: bool = False, lMaisNorm: bool = True):
    '''
    Retorna uma lista de palavras, com nomes de pessoas, numa grafia normalizada para comparações (converte nomes antigos ou com estrangeirismos).
      A lista retornada pode conter elementos "".

    Parâmetros:
      - acStr: Lista de strings.
      - [lRuas] (False): Indica se estamos a normalizar nomes de ruas.
      - [lMaisNorm] (True): Indica se efetua a normalização de preposições (partículas de ligação "de", "da", etc.), que serão substituídas (retiradas) conforme aFP_Prepo.
    '''
    for nI in range(0, len(acStr)):
        # Normalização de palavras inteiras
        acStr[nI] = ApFP(aFP_NameNorm1, acStr[nI], acStr[nI])

        if lMaisNorm and acStr[nI] in G_aPrepo:
            acStr[nI] = ""

        # Inibiu-se -- Normalização de grafemas 1 (letras duplicadas). Problema: tb. apanha coisas como numeração romana, ex: "ii" seria "i", etc.. Era: acStr[nI] = RemoveCarsDup(acStr[nI])

        # Normalização de grafemas 2 (configuração aGrafemas)
        for nJ in range(0, len(aGrafemas)):  # Ex.: "ph" => "f"
            acStr[nI] = acStr[nI].replace(aGrafemas[nJ][0], aGrafemas[nJ][1])

        # Sinais:
        # Apesar de já feito em BasicNameNorm.
        acStr[nI] = acStr[nI].replace(",", " ")
        acStr[nI] = acStr[nI].replace(".", " ")

        # Normalização de grafemas 3 (regex)
        for nJ in range(0, len(aGrafemasRE)):
            acStr[nI] = re.sub(aGrafemasRE[nJ][0],
                               aGrafemasRE[nJ][1], acStr[nI])

        # Repetir normalização de palavras inteiras 1. (2 não, para não remover iniciais.)
        acStr[nI] = ApFP(aFP_NameNorm1, acStr[nI], acStr[nI])

        if len(acStr[nI]) != 2:
            acStr[nI] = acStr[nI].strip()
        # else: # Não fazer aqui strip() final: as iniciais ficam com espaço no fim, essencial para encontrar só iniciais, senão fará match com substring. Ex.: "E." => "e ". Teste: procurar "E. Pereira" deve encontrar "Josefina E. Pereira".

    if lRuas:  # Substituir palavras por abreviaturas
        for nI in range(0, len(acStr)):
            acStr[nI] = ApFP(aAbrevArruamento, acStr[nI], acStr[nI])
            acStr[nI] = ApFP(aAbrevAlojamento, acStr[nI], acStr[nI])
            acStr[nI] = ApFP(aAbrevPorta, acStr[nI], acStr[nI])
            acStr[nI] = ApFP(aAbrevTitulo, acStr[nI], acStr[nI])
            acStr[nI] = ApFP(aAbrevDivCtt, acStr[nI], acStr[nI])

    return acStr


def MoradaSplit(cMorada):

    acStr = cMorada.split(",")

    for i in range(0, len(acStr)):
        acStr[i] = acStr[i].strip()

    return acStr


def NormGrafiaMorada(cNome: str, lElementos: bool = False):
    '''
    Normaliza a grafia duma morada. Retorna uma lista de palavras, ou uma string, com grafia normalizada para comparações.
    Parâmetros:
      - cNome: String contendo o nome.
      - [lElementos] (False): Indica se retorna apenas a parte do arruamento. (Não está em uso?)
    '''
    cNome = cNome.lower()
    cNome = strip_accents(cNome)  # Tudo em minúsculas, sem acentos.

    # --- Fazer substituições próprias do âmbito.
    # Subst. de abrev. Tem de se fazer aqui pq tem duas pals.
    cNome = cNome.replace("sem numero", "sn")

    if lElementos:
        cNome = cNome.replace(" - ", ", ")
        acStr = MoradaSplit(cNome)
        aNomes = [acStr[0]]
    else:
        cNome = cNome.replace(" - ", " ")
        cNome = cNome.replace(",", " ")
        cNome = cNome.replace(";", " ")

        aNomes = cNome.split()

    aNomes = NameNorm_List(aNomes, True)
    return aNomes


def DaIniciaisLista(acNome, nCarat=1):
    '''
    Retorna lista com iniciais das palavras da lista.
    Parms.:
    - acNome: Array de palavras.
    - [nCarat] (1): Nº máximo de carateres a extrair no início de cada palavra.
    '''
    aIniciais = []
    for pal in acNome:
        aIniciais.append(pal[:nCarat])
    return aIniciais


def Da1aUltIniciais(acNome):
    '''
    Retorna lista com iniciais da 1ª e última palavra.
    '''
    aIniciais = []
    if acNome:
        aIniciais.append(acNome[0][0])
        if len(acNome) > 1:
            aIniciais.append(acNome[-1][0])
    return aIniciais


def DaStrComIniciais(aPalPrc):
    '''
    Dada uma lista de palavras, retorna duas strings de iniciais a usar em pesquisas.
    '''
    if len(aPalPrc) == 1:
        # só uma palavra => não procurar a inicial, para evitar demasiados resultados sem interesse.
        c1aUltIniciais = ""
        cTodasIniciais = " ".join(
            DaIniciaisLista(aPalPrc, 3))  # 3 1ºs carateres
    else:
        c1aUltIniciais = " ".join(Da1aUltIniciais(aPalPrc))
        cTodasIniciais = " ".join(DaIniciaisLista(aPalPrc))

    return cTodasIniciais, c1aUltIniciais


def AbreviaNomeID(cNome, n1o=2):
    '''
    Abrevia um nome de pessoa, tipicamente desde a palavra n1o até ao penúltimo, para geração de ID de pessoas.
    Parms.:
      - cNome: Nome a abreviar.
      - [n1o] (2): Nº (natural) do nome onde se pretende começar a abreviar.
    '''
    cNome = re.sub('[-]+', ' ', cNome)  # Substituir hífens por " ".
    acNome = cNome.split()

    n1o -= 1  # Pq abaixo se indexa a partir do zero, e n1o é um natural.
    nPalsAte = len(acNome)  # Até onde abreviar (nº natural).
    # Abreviar
    if acNome[0].lower() == "maria":
        # 1º nome muito comum => deixamos este e o seguinte.
        pass
    else:
        n1o -= 1

    if nPalsAte > 2 and acNome[-1].lower() in ("júnior", "junior", "sénior", "senior"):
        # Nomes terminados em "Júnior", "Sénior": não é nome de batismo, é uma classificação => abreviamos e deixamos de abreviar o anterior.
        acNome[-1] = acNome[-1][0]
        nPalsAte -= 1

    for nI in range(0, len(acNome)):
        # Tirar "de", "da", etc.
        acNome[nI] = ApFP(aFP_Prepo, acNome[nI].lower(), acNome[nI])

    for nI in range(0, nPalsAte):
        if nI > n1o and nI < nPalsAte-1 and acNome[nI]:
            acNome[nI] = acNome[nI][0]

    cNome = TiraDupEsp(' '.join(acNome))
    return cNome


def BasicNameNorm(cNome):
    '''
    Normalização básica duma string, a pensar em pesquisas.
    Retira pontos de algumas abreviaturas ("Lda.", "S.A.") e endereços de email.
    '''
    # Nota: esta linha ajuda a encontrar coisas como ":joão" e "anb:joão".
    cNome = camelCase2lowcase(cNome, False)
    cNome = cNome.lower()  # Já feito em camelCase2lowcase

    cNome = strip_accents(cNome)  # Tudo em minúsculas, sem acentos.

    if cNome[:2] == "e ":  # 24/12
        # O "e" está no início. Do seguinte modo não será descartado:
        cNome = "e. " + cNome[2:]

    # === Fazer substituições próprias de nomes.
    # cNome = re.sub(r",", " ", cNome) # v ant
    cNome = cNome.replace(",", " ")  # Ajuda à substituições seguintes.
    cNome += " "  # Ajuda à substituições seguintes

    # "lda" (inc. <-- "ldª") = limitada
    cNome = re.sub(r"\blda\b", "lda", cNome)

    # "ld.a" (inc <-- "ld.ª") = limitada
    cNome = re.sub(r"\bld.a", "lda", cNome)

    # "s.a.r.l." = sociedade anónima de responsabilidade limitada
    cNome = re.sub(r"\bs\.a\.r\.l\.\s", "sarl", cNome)
    cNome = re.sub(r"\bs\.a\.\s", "sa", cNome)  # "s.a." = sociedade anónima

    # --- Endereço de email => separar palavras.
    # Não convém tirar/substituir pontos a eito, para preservar nomes abreviados com iniciais, que a normalização subsequente iria eliminar.
    # Ex.: Se for "Luzia E." queremos "Luzia E". Como era a pensar nos endereços de email, ajustou-se com regex.

    # #$$# cf. javascript mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/

    cNome = re.sub(r"(\w+)[\.-]?(\w+)@(\w+)\.(\w+)", r"\1-\2 \3 \4", cNome)

    # === As subst. seguintes são para viabilizar a separação de palavras:
    # --- Substituir determinados carateres por espaço.
    cNome = cNome.replace("-", " ")  # Ex.: "Pós-de-Mina".
    cNome = cNome.replace("_", " ")

    # --- Proteger "do Ó" para não haver match com iniciais. Tem de ser depois da substituição dos "_".
    # \b é "boundary", para apanhar palavras inteiras => "do Óculo" não faz match.
    cNome = re.sub(r"\bdo o\b", "do_o", cNome)
    # ---

    # --- A revelar-se inconveniente, pelo menos será necessário fazer «.replace(":", ": ")». Ex.: "anb:joão_m" deve permitir encontrar "anb:joão".
    cNome = cNome.replace(":", " ")
    # ---
    cNome = cNome.replace("(", " ")  # Ex.: "(194x)", "(194.)"
    cNome = cNome.replace(")", " ")
    return cNome


def NormDtNasc(cStr, lProtegePto=True, lTiraCarD=True):
    '''
    Normalização de um ano ou data de nascimento para pesquisas. Reconhece grupos (regex=>) "d?99..".
    Basicamente, retira parêntesis se existirem (e "d" se lTiraCarD); se houver 99xx, transforma os x em ponto (depois protegido se lProtegePto).
    Notas:
      - A haver parêntesis, poderão ser retirados em BasicNameNorm.
    '''
    # --- Tratar grupos (regex=>) "d?9999".
    # Racional: Os ID de pessoas incluem estes grupos.
    # (Nota: Os "_" são transformados em " " só mais tarde.)

    # Ex. in: "d1969", "(1969)".
    if lTiraCarD:
        # Retira a letra "d". Ex. in: "d1969", "(1969)".
        cStr = re.sub(r"(\(?(d?)(\d{2}..)\)?)", r"\3", cStr)
        # => Ex. out: "1969".
    else:
        cStr = re.sub(r"(\(?(d?)(\d{2}..)\)?)", r"\2\3", cStr)
        # => Ex. out: "d1969".

    # "x" passará a "." por ser útil em regex ao pesquisar.
    # (regex=>) "d?999x" => "d?999."
    # (regex=>) "d?99xx" => "d?99.."
    cStr = re.sub(r"(\d)(\d)(\d)x", r"\1\2\3.", cStr)
    cStr = re.sub(r"(\d)(\d)xx", r"\1\2..", cStr)

    if lProtegePto:
        # Protege-se os "." para não serem eliminados mais tarde por outra função de normalização. Assume-se que, depois de todas as normalizações, algures se recuperará os pontos (str.replace("<%>", ".")). Racional: garantir que os pontos ficam disponíveis para pesquisas regex.
        cStr = re.sub(r"(\d)(\d)(\d)\.", r"\1\2\3<%>", cStr)
        cStr = re.sub(r"(\d)(\d)\.\.", r"\1\2<%><%>", cStr)
    # --- FIM Tratar grupos (regex=>) "d?9999".

    return cStr


def NormGrafiaNome_Str(cNome: str, lMaisNorm: bool = True, lProtegePto=True, lTiraCarD=True) -> str:
    '''
    Retorna uma string, com grafia normalizada para comparações.
    Parâmetros:
      - cNome: String contendo o nome.
    '''
    cNome = NormDtNasc(cNome, lProtegePto,
                       lTiraCarD)  # Tratar grupos (regex=>) "d?9999".
    cNome = BasicNameNorm(cNome)
    res = NameNorm_Str(cNome.split(), lMaisNorm=lMaisNorm)

    # Recuperar "." que foram protegidos em NormDtNasc (para impedir que desapareçam via _NameNormList).
    res = res.replace("<%>", ".")
    return res


def NormGrafiaNome_List(cNome: str, lMaisNorm: bool = True) -> list:
    '''
    Retorna uma lista de palavras, com grafia normalizada para comparações.
    Parâmetros:
      - cNome: String contendo o nome.
    '''
    '''
    Exemplos:
      - "Agatha Elisabeth Seraphina Philippa" => ['agata', 'elisabete', 'serafina', 'filipa']
      - "João  da Silva  de O'Hara do Óculo do Ó" => ['joao', 'silva', "o'hara", 'oculo', 'do_o']
      - "Thereza" => ['tereza']
    '''
    # Tratar grupos (regex=>) "d?9999". Protege pontos.
    cNome = NormDtNasc(cNome)

    cNome = BasicNameNorm(cNome)
    res = NameNorm_List(cNome.split(), lMaisNorm=lMaisNorm)

    # Recuperar "." que foram protegidos em NormDtNasc (para impedir que desapareçam via _NameNormList).
    for n in range(0, len(res)):
        res[n] = res[n].replace("<%>", ".")

    return res
