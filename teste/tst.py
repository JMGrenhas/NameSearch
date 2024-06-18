from NameSearch import Name_List_Search, Name_List_Search_unfolded

acNameList = []

# As cadeias "estranhas" são identificadores de ontologia
acNameList += [
    "José da Carvalhosa",
    "João Júnior",
    "João Maciel Pós-de-Mina Garcia",
    "João Maciel Garcia",
    "João Rosado Garcia",
    "João Rosado Garcia (194x)",    
    "João_M_Garcia_d1941",
    "João_M_Garcia_d194x",    
    "João Maria de Carvalho",
    "Maria Isabel Pereira da Mata",
    "Manuel do Almada",
    "Manuel_Almada_d1966",
    "Alberto Carvalho Júnior",
    "Manuel Carvalho da Silva e do Silvo Júnior",
    "Manuel Carvalho Sénior",
    "Manuel do Ó",
    "Maria Albertina do Ó",
    "Rui Abrantes III",
    "Ruy Philippe Nery"
]
acNameList += [
    "João_M_P_M_Garcia_d19690621",
    ":João_M_P_M_Garcia_d19690621",
    "anb:João_M_P_M_Garcia_d19690621",
    "anb:temAvô",
    ":J_M_P_M_Garcia_d0000"
]

acNameList += ["Aqui, em Guimarães, onde... "
]

#cSearch = "grenhas (1942)"
#cSearch = "grenhas (1941)"
#cSearch = "grenhas (194x)"
#cSearch = "grenhas (194.)"
#cSearch = "grenhas (19xx)"
#cSearch = "grenhas (196.)"
#cSearch = "(196.)"
#cSearch = "(196x)"

#cSearch = "anb:temAvô"
#cSearch = ":temAvô"
#cSearch = "temAvô"
#cSearch = "tem Avô"
#cSearch = "Avô"
#cSearch = "anb:tem"
#cSearch = "anb:joão"

#cSearch = "j grenhas (194x)"
cSearch = "guimaraes"
#cSearch = "j gre"

lSo_1o = False
lUsarIniciais = True

# ---
tab1, tab2, aCtrl = Name_List_Search_unfolded(
    acNameList, cSearch, lSo_1o, lUsarIniciais)

print("\n--- F. Name_List_Search_unfolded")
print("Lista onde procurou tem tamanho =", len(acNameList))
print("Procurou-se", "«"+cSearch+"»", "; lUsarIniciais:", lUsarIniciais)
print("Resultados:")
print("aCtrl:", aCtrl)
print("melhor==>", len(tab1), "--", tab1)
print("outros==>", len(tab2), "--", tab2)

# ---
res = Name_List_Search(
    acNameList, cSearch, lSo_1o, lUsarIniciais)

print("\n--- F. Name_List_Search")
print("Lista onde procurou tem tamanho =", len(acNameList))
print("Procurou-se", "«"+cSearch+"»", "; lUsarIniciais:", lUsarIniciais)
print("Resultados:")
print("res:", res)

# ---
lUsarIniciais=False
res = Name_List_Search(
    acNameList, cSearch, lSo_1o, lUsarIniciais)

print("\n--- F. Name_List_Search")
print("Lista onde procurou tem tamanho =", len(acNameList))
print("Procurou-se", "«"+cSearch+"»", "; lUsarIniciais:", lUsarIniciais)
print("Resultados:")
print("res:", res)
