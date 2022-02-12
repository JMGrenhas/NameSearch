'''
  myLists.py - fs. sobre listas. 

  Cf. myStrings.py, onde há funções aplicáveis a listas.
'''
import copy


def myListCopy(a):
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


def LinearizarLista(aLista, lTodos: bool = True):
    '''
    Retorna lista linear com os elementos do parâmetro.
    Parms.:
      - [lTodos] (True): Indica se faz recursão por todos os elementos.
    '''
    '''
    Notas:
      - Os elementos da lista de entrada podem ou não ser listas.
      - É recursiva sobre os elementos do tipo lista.
    '''
    aLinear = []
    for i in aLista:
        if type(i) == list or type(i) == tuple:
            aLinear += LinearizarLista(i, lTodos)
        elif lTodos or i:
            aLinear.append(i)

    return aLinear


def ListaSemRepetidos(aLista):
    '''
    Refaz uma lista linear sem elementos repetidos. Se a lista não for linear, não faz alteração.
    Parms.:
      - aLista: Lista linear (i.e., de elementos atómicos).
    '''
    if not aLista or type(aLista[0]) == list:
        return aLista
    return list(dict.fromkeys(aLista))


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
    for i in a1:
        if not i in a2:
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
    '''
    for n in range(0, len(acStr)):
        if acStr[n] in acParticulas:
            acStr[n] = ""

    if lRemover:
        RemoveVaziosLista(acStr)
    return acStr


def TryDictKey(yDict, key):
    try:  # (Porque key pode não estar definida em yDict, o que daria uma exceção... => cf. yDict.get(key, ""))

        item = yDict[key]  # yDict é um dicionário.
        '''
        Ex.: yDict ==
            {rdflib.term.Variable('s'): rdflib.term.URIRef('http://www.semanticweb.org/grenhasMEI/AncestorsNB#sq_01'),
        
        rdflib.term.Variable('p'): rdflib.term.URIRef('http://www.semanticweb.org/grenhasMEI/AncestorsNB#resumo'),
        
        rdflib.term.Variable('o'): rdflib.term.Literal('Pessoa: Ver ou procurar nomes')}
        '''
    except:
        item = ""
    return item


def SameContentLists(a1, a2):
    '''
    Indica se duas listas são do mesmo tamanho e têm os mesmos elementos, ainda que por ordem diferente.
    '''
    if len(a1) != len(a2):
        return False

    for e in a1:
        if e not in a2:
            return False

    for e in a2:
        if e not in a1:
            return False

    return True

"""
a1 = [1,2]
a2 = [2,1]
print(SameContentLists(a1, a2)) # True

a1 = [1,2]
a2 = [2,1,1]
print(SameContentLists(a1, a2)) # False
"""