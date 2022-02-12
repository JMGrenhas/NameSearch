'''
  myStrings.py - fs. sobre strings.
  Preferencialmente, não deve ter dependências de outros módulos.

-----
Dicas:
Exemplos do (python) format():
  txt = "For only {price:.2f} dollars!".format(
      price = 49) == "For only 49.00 dollars!"
'''
import os.path
import re
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


def MyLeftSplit(cStr, cCar):
    '''
    Se cCar não existir em cStr ou for vazio, retorna ('', cStr), senão retorna o que estiver antes e depois de cCar.
    '''
    if cCar and (i := cStr.find(cCar)) != -1:  # Encontrou cCar" => retorna o que está antes e depois.
        cLeft = cStr[: i].strip()
        cResto = cStr[i+1:].strip()
    else:
        cLeft = ""
        cResto = cStr

    return cLeft, cResto


def NumericSufixSplit(cID, nPad: int = None):
    '''
    Separa e retorna os carateres do início e o sufixo numérico no fim.
    Parms.:
      - cID: str -- ID a separar.
      - [nPad]: int -- Tamanho para encher o sufixo com zeros à esquerda.
    Resultado:
      - cIni: str -- carateres de cID antes do sufixo numérico.
      - cDigs: str -- dígitos no fim de cID.
    '''
    cDigs = ''  # Sufixo numérico.

    if cID[-1].isdigit():
        # Acaba em dígito => separar o <início> dos <dígitos do fim>, para fazer um pad0 aos dígitos, para depois ordenar em função da parte numérica.
        cIni = ''  # Parte antes do sufixo numérico.

        for nC in range(len(cID), 0, -1):  # Do fim para o início.
            if cID[nC-1].isdigit():
                # Enquanto apanhar dígitos no fim, coleciona.
                cDigs = cID[nC-1] + cDigs
            else:  # Já se apanhou algo != dígito => o resto vai para cIni.
                cIni = cID[:nC]
                break

        if nPad:
            cDigs = cDigs.zfill(nPad)  # <=> cDigs.rjust(nPad, '0')
    else:
        cIni = cID

    return cIni, cDigs


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
    SUM. NatSlice - "natural slice". Extrai e retorna substring conforme parâmetros. Atenção: O posicionamento é por nºs naturais e vai de 1 a len().
      Também funciona com listas. É equivalente ao SubStr() do Xbase++.

    Parms.:
      - cStr: String de entrada.
      - nPos: INT. Posição inicial em cStr:
          * Desde o início: valores de 1 a len().
          * Desde o fim: valores de -1 a -len().
      - [nTam] (VPD: até ao fim): Nº positivo de carateres a extrair.

    Resultado: STR.
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


def IsStrNum(literal):
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


def text_to_id(text, lLower=False, lStripAccents=False):
    '''
    SUM.- Gera um ID a partir duma string qualquer, que pode até ter pontuação, apóstrofos e apas. Preserva diacríticos e "case".

    Parms.:
      - text: String a converter.
      - [lLower] (False): Indica se converte para minúsculas.
      - [lStripAccents] (False): Indica se converte diacríticos para ascii.

    Resultado: string
    Notas: Recorre a text_to_alphanum_id().

    Exemplos:
    1) text_to_id("Montréal, über, 12.89, Mère, Françoise, noël, 889", True, True)
      >>> 'montreal_uber_1289_mere_francoise_noel_889'
    2)
      #txt = "O'Hara?!, Áá-Éé-Àà-Èè-Ãã-Õõ, Çç-êô, Üürê, 12.25 9 2º II"
      text_to_id(txt, False, False)  # => "OHara_Áá_Éé_Àà_Èè_Ãã_Õõ_Çç_êô_Üürê_1225_9_2º_II"
      text_to_id(txt, False, True)   # => "OHara_Aa_Ee_Aa_Ee_Aa_Oo_Cc_eo_Uure_1225_9_2_II"
      text_to_id(txt, True, False)   # => "ohara_áá_éé_àà_èè_ãã_õõ_çç_êô_üürê_1225_9_2º_ii"
      text_to_id(txt, True, True)    # => "ohara_aa_ee_aa_ee_aa_oo_cc_eo_uure_1225_9_2_ii"
    '''
    if lLower:
        text = text.lower()

    if lStripAccents:
        # Substituir espaços e hífens por "_".
        text = re.sub('[ -]+', '_', text)
        text = strip_accents(text)
        text = re.sub('[^0-9a-zA-Z_]', '', text)
    else:
        text = text_to_alphanum_id(text)

    return text


def text_to_alphanum_id(text):
    '''
    SUM.- Gera um ID a partir duma string qualquer, que pode até ter pontuação, apóstrofos e apas. Preserva diacríticos e "case".
    '''
    text = re.sub('[ -]+', '_', text)  # Substituir espaços e hífens por "_".
    res = ""
    for c in text:  # Para cada caráter na string...
        if c == "_" or c.isalnum():
            res += c
    return res


def TiraDupEsp(cStr: str) -> str:
    '''
    SUM.- Numa string, converte todo o espaçamento duplo/triplo/etc. em simples: "  "-->" ".
    '''
    while "  " in cStr:
        cStr = cStr.replace("  ", " ")
    return cStr


# Be careful with multiple spaces, and empty strings
# for empty words w[0] would cause an index error,
# but with w[:1] we get an empty string as desired
def cap_sentence(s):
    '''
    SUM.- Capitalizar a 1ª letra de cada palavra.
    '''
    return ' '.join(w[:1].upper() + w[1:] for w in s.split(' '))


def cap_sentence2(s):
    '''
    SUM.- Capitalizar a 1ª letra de cada palavra.
    '''
    return ''.join((c.upper() if i == 0 or s[i-1] == ' ' else c) for i, c in enumerate(s))


def EscapeQuotesInExp(cExp: str):
    '''
    Envolve com aspas ou apóstrofos, protegendo aspas e apóstrofos no conteúdo dum literal.
    Racional: Evitar erros de parsing em strings, como por exemplo em queries SPARQL.
    '''
    if '"' in cExp:  # Contém aspas
        cExp = cExp.replace("'", "\\'")  # escape «'»
        cExp = "'" + cExp + "'"  # Delimitar c/ «'»

    elif "'" in cExp:
        cExp = cExp.replace('"', '\\"')  # escape «"»
        cExp = '"' + cExp + '"'
    else:
        cExp = '"' + cExp + '"'
    return cExp


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

    #print(cStr, "<-- camelCase2lowcase_word")
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

    #print(cStrOut, "FIM <-- camelCase2lowcase_word")
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
    #print(acStr, "<-- camelCase2lowcase, ini")

    for n in range(0, len(acStr)):
        acStr[n] = camelCase2lowcase_word(
            acStr[n], lSkip_if1stUpper, lPreserve_1stUpper)

    #print(acStr, "<-- camelCase2lowcase, fim")
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
    SUM.- Ordena uma tabela de strings até à terceira coluna, independente de maiúsculas e diacríticos.
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

# testes
#print(SortedTable(["bb", "Ân", "zanadu", "aa", "õ", "ontem"]))
#print(SortedTable([["bb", "cc", "b", "b"], ["bb", "cc", "a", "b"], ["bb", "Ân", "a", "b"], ["aa", "b", "a", "b"]]))
