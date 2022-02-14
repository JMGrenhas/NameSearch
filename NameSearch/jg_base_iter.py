'''
  jg_base_iter.py - fs. básicas sobre iteráveis, incluindo strings.
  
  Preferencialmente, só deve ter dependências de módulos python.
'''
import os.path
#import re
import unicodedata


def Alltrim(cStr: str) -> str:
    return cStr.strip()


def Left(cStr, nTam):
    '''
    SUM. Left - Extrai e retorna substring à esquerda.

    Parâmetros:
      - cStr: String de entrada.
      - nTam: Nº de carateres a extrair de cStr, à esquerda, valores de 1 a len().
          * -1 => "".

    Resultado: STR.
    Exemplos:
      Left( 'abcdef', 0 ) # '«»'
      Left( 'abcdef', 2 ) # '«ab»'
      Left( 'abcdef', 11 )+"»") # '«abcdef»'
      Left( 'abcdef', -2) # '«»'
    '''
    if nTam <= 0:  # Salvaguarda.
        return ""
    return cStr[: nTam]


def Right(cStr, nTam):
    '''
    SUM. Right - Extrai e retorna substring à direita.

    Parâmetros:
      - cStr: String de entrada.
      - nTam: Nº de carateres a extrair de cStr, à direita, valores de 1 a len().
          * -1 => "".

    Resultado: STR.

    Notas:
      - Tb. funciona sobre listas mas retorna uma lista.
    Exemplos:
      Right( 'abcdef', 2 ) # '«ef»'
      Right( 'abcdef', 1 ) # '«f»'
      Right( 'abcdef', 11 )+"»") # '«abcdef»'
      Right( 'abcdef', 0 ) # '«»'
      Right( 'abcdef', -2) # '«»'
    '''
    if nTam <= 0:  # Salvaguarda.
        return ""
    return cStr[-nTam:]


def NatSlice(cStr, nPos, nTam=-1):
    '''
    "Natural slice" -- Retorna uma substring conforme parâmetros. Atenção: O posicionamento é por números naturais.
      Também funciona com listas.

    Parms.:
      - cStr: String de entrada.
      - nPos: INT sem zero. Posição inicial em cStr:
          * Desde o início: valores de 1 a len(cStr).
          * Desde o fim: valores de -1 a -len(cStr).
      - [nTam] (VPD: até ao fim): Nº positivo de carateres a extrair.

    Resultado: STR.
    Notas:
      - É equivalente ao SubStr() do Xbase++.
    Exemplos:
      - NatSlice( 'abcdef', 2, 3 ) == 'bcd'
      - NatSlice( 'abcdef', 2 ) == 'bcdef'
      - NatSlice( ['a', 'b', 'c', 'd', 'e', 'f'], 2, 3 ) == ['b', 'c', 'd']
      - NatSlice( 'abcdef', 2 ) == 'bcdef'
    '''
    if nTam == -1:
        nTam = len(cStr)
    if nPos < 0:
        # -1 <=> Do último caráter para a esquerda, até <nTam>.
        if nPos+1 == 0:
            return cStr[nPos+1-nTam:]
        else:
            return cStr[nPos+1-nTam: nPos+1]
    return cStr[nPos-1: nPos-1+nTam]


def IsStrNum(literal: str):
    '''
    Indica se uma string referente a um literal só contém dígitos, a menos do ponto decimal.
    Parms.:
      - literal: String. Ex.: "12", "12.25", ".25" retornam True. "1,25" retorna False.
    Notas:
      - Depois, pode testar-se <if "." in literal>, para saber se tem um ponto decimal.
      - Ver tb. isdecimal (do Python).
    Resultado: bool
    '''
    return literal and not literal[0].isalpha() and \
        literal.replace(".", "").isnumeric()


def strip_accents(text):
    """
    @en: Strip accents from input String.
    Converte diacríticos para ascii, mantendo "case".

    :param text: STR. The input string.

    Resultado: STR. The processed String.
    """
    '''
    Notas:
      - 16/04/2021 - retirado de https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-normalize-in-a-python-unicode-string

    Exemplos:
      - strip_accents(text).lower()
      - strip_accents(text.lower())
    '''
    # JG: Inibi por me parecer escusado no meu âmbito.
    # try: text = unicode(text, 'utf-8')
    # except (TypeError, NameError): # unicode is a default on python3
    #    pass
    # ---
    # text in: ex.: "O'Hara?!, Ññ Áá-Éé-Àà-Èè-Ãã-Õõ, Çç-êô, Üürê, 12.25 9 2º II"

    # Visivelmente parece inócuo, mas se não for aplicado os diacríticos desaparecem.
    text = unicodedata.normalize('NFD', text)
    # Ex.:    "O'Hara?!, Ññ Áá-Éé-Àà-Èè-Ãã-Õõ, Çç-êô, Üürê, 12.25 9 2º II"

    # --- Tratar variantes na utilização de ª e º.
    text = text.replace(".ª", "a")
    text = text.replace("ª.", "a")
    text = text.replace("ª", "a")
    text = text.replace(".º", "o")
    text = text.replace("º.", "o")
    text = text.replace("º", "o")
    # ---
    text = text.encode('ascii', 'ignore')
    # Ex.:   b"O'Hara?!, Nn Aa-Ee-Aa-Ee-Aa-Oo, Cc-eo, Uure, 12.25 9 2 II" # retirou "º"

    text = text.decode("utf-8")
    # Ex.:    "O'Hara?!, Nn Aa-Ee-Aa-Ee-Aa-Oo, Cc-eo, Uure, 12.25 9 2 II"
    text = str(text)
    return text


def StdStrNorm(cStr):
    '''
    Normalização de uma string do modo mais básico possível: lower + tirar acentos.
    '''
    cStr = cStr.lower()
    cStr = strip_accents(cStr)
    return cStr


def TiraAspas(cStr):
    '''
    Retira aspas ou plicas do início e fim da string.
    '''
    cStr = cStr.strip('\"')
    cStr = cStr.strip("\'")
    return cStr


def TiraDupEsp(cStr: str) -> str:
    '''
    SUM.- Numa string, converte todo o espaçamento duplo/triplo/etc. em simples: "  "-->" ".
    '''
    while "  " in cStr:
        cStr = cStr.replace("  ", " ")
    return cStr


def FileNameExtension(filename, lLower=True):
    """
    Retorna a extensão dum ficheiro, sem ".".
    Exemplos:
      - FileNameExtension("c:/xx.cc/aaa.PDF") == "pdf"
    """
    cExt = os.path.splitext(filename)[1][1:]
    if lLower:
        cExt = cExt.lower()
    return cExt


def camelCase2lowcase_word(cStr: str, lSkip_if1stUpper=False, lPreserve_1stUpper=False):
    '''
    Usar apenas com palavras inteiras, senão cf. camelCase2lowcase.
    Tipicamente, de cada vez que encontrar uma maiúscula, mete um espaço e converte para minúscula.
    Racional: apresentação mais legível ao utilizador.
    Parms.:
      - cStr: Palavra inteira.
      - [lSkip_if1stUpper] (False): Indica se, sendo a primeira letra maiúscula, retorna cStr tal e qual.
        Ex.: "Pessoa", "HistóriaDeInfância".
      - [lPreserve_1stUpper] (False): Indica se, sendo a primeira letra maiúscula, preserva maiúsculas, limitando-se a meter espaços. Alternativa a <lSkip_if1stUpper>.
        Ex.: "PascalCase" => "Pascal Case".
    '''
    if not cStr or (lSkip_if1stUpper and cStr[0].isupper()):
        # Ex.: nomes de classes, "HistóriaDeInfância".
        return cStr

    if cStr.isupper():  # Ex.: "IV" => "iv".
        return cStr.lower()

    cStrOut = ""
    for n in range(0, len(cStr)):
        c = cStr[n]
        if c.isupper():
            if n > 0 and cStr[n-1] != "'":
                # Não é o 1º; e casos "O'Hara" => "o'hara"
                cStrOut += " "
            if lPreserve_1stUpper:
                cStrOut += c
            else:
                cStrOut += c.lower()
        else:
            cStrOut += c

    return cStrOut


def camelCase2lowcase(cStr: str, lSkip_if1stUpper=False, lPreserve_1stUpper=False):
    '''
    A primeira maiúscula, converte para minúscula (cf. lPreserve_1stUpper), de depois, de cada vez que encontrar uma maiúscula, mete um espaço e converte para minúscula.

    Racional: facilitar pesquisas.
    Parms.:
      - cStr: Cadeia de carateres.
      - [lSkip_if1stUpper] (False): Cf. camelCase2lowcase_word.
      - [lPreserve_1stUpper] (False): Cf. camelCase2lowcase_word.
    '''
    # if not cStr:
    #    return cStr

    cStr = cStr.replace("_", " ")  # Caso dos ID.
    acStr = cStr.split()

    for n in range(0, len(acStr)):
        acStr[n] = camelCase2lowcase_word(
            acStr[n], lSkip_if1stUpper, lPreserve_1stUpper)

    cStrOut = ' '.join(acStr)
    return cStrOut


def SortedList(aStr):
    '''
    SUM.- Ordena uma lista de strings, independentemente de maiúsculas e diacríticos.

    Ver tb.: SortedTable, que serve para o mesmo efeito.
    '''
    if aStr:
        aStr = sorted(aStr, key=lambda row: strip_accents(row).lower())
    return aStr


def SortedTable(table):
    '''
    SUM.- Ordena uma "tabela" de strings até à terceira coluna, independente de maiúsculas e diacríticos.
    Args:
      - table: Lista de str ou lista de itens indexáveis (listas ou tuplos).
    '''
    if table:
        if type(table[0]) in (list, tuple):  # As linhas são listas ou tuplos:
            if len(table[0]) == 1:
                #table = sorted(table, key=lambda tup: (strip_accents(tup[0]).lower()))
                table = \
                    sorted(table, key=lambda tup: [
                           strip_accents(tup[0]).lower()])

            elif len(table[0]) == 2:
                table = \
                    sorted(table, key=lambda tup: [strip_accents(tup[0]).lower(),
                                                   strip_accents(tup[1]).lower()])

            else:  # len(table(0)) >= 3:
                table = \
                    sorted(table, key=lambda tup: [strip_accents(tup[0]).lower(),
                                                   strip_accents(
                                                       tup[1]).lower(),
                                                   strip_accents(tup[2]).lower()])
        else:  # Lista linear de strings
            table = sorted(table, key=lambda row: strip_accents(row).lower())

    return table


def OvwFP(aaFP, chave, xCorrespondencia):
    '''
    SUM.- Reescreve, na função parcial <aaFP>, a associação «chave»->«Corresp», e retorna <aaFP>.
          Se a chave não existir, insere normalmente.
    Parâmetros:
      - aaFP: FParcial.
      - chave: Chave a inserir/reescrever.
      - xCorrespondencia: Valor a associar.
    Resultado: FParcial
    Notas:
      - Aconselha-se inserir apenas chaves do mesmo tipo.
      - Se <xCorrespondencia> for list ou dict, guarda apenas a referência, não duplica.
    '''
    nPos = None
    for n in range(0, len(aaFP)):
        if aaFP[n][0] == chave:
            nPos = n
            break

    if nPos != None:
        # => chave existe na posição aaFP[nPos][0], logo reescreve a correspondência:
        aaFP[nPos][1] = xCorrespondencia
    else:  # // não existe => insere
        aaFP.append([chave, xCorrespondencia])

    return aaFP


def InsFp_After(aaFP, chave, xCorrespondencia, chaveOnde):
    '''
    Insere um par [chave, xCorrespondencia] depois da posição de chaveOnde.
    '''
    for i in range(len(aaFP), 0, -1):
        if aaFP[i-1][0] == chaveOnde:
            aaFP.insert(i, [chave, xCorrespondencia])
            break
    return aaFP


def RemFP(aaFP, chave):
    '''
    Remove chave de aaFP.
    '''
    n = 0
    while n < len(aaFP):
        if aaFP[n][0] == chave:
            aaFP.pop(n)
        n += 1


def ApFP(aFP, chave, xValorPorDefeito=None):
    '''
    Aplica a Função Parcial aFP à chave.
    Dada a função parcial aFP, aplica a chave. Se encontrar, retorna a correspondência, senão retorna xValorPorDefeito.
    Parms.:
      - aFP: Lista de pares ou Tuplo de pares.
      - chave: Chave a procurar.
      - [xValorPorDefeito] (None): Valor retornado se não existir a chave.
    '''
    '''
    Exemplos:
      - aFP:
        - [["b", 2], ["a", 4]]
        - (("b",2), ("a",4))
    '''
    for e in aFP:
        if e[0] == chave:
            return e[1]
    return xValorPorDefeito


def PertenceFP(aFP, chave):
    '''
    Indica se existe na Função Parcial aFP a chave.
    Parms.:
      - aFP: Lista de pares ou Tuplo de pares.
      - chave: Chave a procurar.
    '''
    for e in aFP:
        if e[0] == chave:
            return True
    return False
import copy


def ACopy(a):
    '''
    SUM.- Retorna cópia rápida duma lista. Cuidado com listas e objetos aninhados: não serão clones -- para clonar cf. AClone.
    '''
    return a[:]


def AClone(a):
    '''
    SUM.- Retorna clone duma lista.

    Notas: +- <=> AClone() do Xbase++.
    '''
    return copy.deepcopy(a)


def ATail(a, xVPD=None):
    '''
    SUM.- Retorna o último elemento duma lista.
    '''
    if a:
        return a[-1]
    else:
        return xVPD


def HaInterseccaoListas(a1, a2):
    '''
    Indica se pelo menos um elemento é comum às duas listas.
    '''
    for i in a1:
        if i in a2:
            return True
    return False


def ListaContidaEm(a1, a2) -> bool:
    '''
    Indica se todos os elementos de a1 estão em a2. Se a1 = [], retorna True.
    '''
    for e in a1:
        if not e in a2:
            return False
    return True


def RightRemove(alist, x):
    '''
    Remove a última ocorrência de x em alist.
    '''
    for i in range(len(alist), 0, -1):  # Do fim p o início.
        if alist[i-1] == x:
            alist.pop(i-1)
            break


def RemoveVaziosLista(acStr) -> list:
    '''
    Remover elementos vazios da lista.
    '''
    # A lista pode ter de ser percorrida mais de uma vez, daí o "while".
    while True:
        lRepete = False
        for i in acStr:
            # v ant 19/12: arriscado com zeros, {}, etc...
            # if not i:
            if i == None or i == "":
                acStr.remove(i)
                lRepete = True
        if not lRepete:
            break  # Termina "while"
    return acStr


def LimpaParticulas(acStr, acParticulas, lRemover=False):
    '''
    Anula uma lista de palavras numa lista, com opção de remoção.
    Parms.:
      - acStr: Lista a tratar.
      - acParticulas: Lista de palavras a anular na lista.
      - [lRemover] (False): Indica se os itens anulados devem ser removidos da lista, senão ficam como "".
    Exs.:
      - LimpaParticulas(["em", "casa", "de"], ["de", "em"]) == ["", "casa", ""]
      - LimpaParticulas(["em", "casa", "de"], ["de", "em"], True) == ["casa"]
    '''
    for n in range(0, len(acStr)):
        if acStr[n] in acParticulas:
            acStr[n] = ""

    if lRemover:
        RemoveVaziosLista(acStr)
    return acStr
