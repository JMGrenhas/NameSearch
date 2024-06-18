from NameSearch import Name_List_Search, Name_List_Search_unfolded

acNameList = []

acNameList += [
    "Manuel do Almada",
    "José da Carvalhosa",
    "José Maciel Pós-de-Mina Silva",
    "João_M_P_M_Silva_d19690621",
    "João Maria Grenhas",
    "João Maria Grenhas (194x)",    
    "João_M_Grenhas_d1941",
    "João_M_Grenhas_d194x",    
    "João Maria de Carvalho",
    "Maria Isolda Pereira da Mata",
    "Manuel_Almada_d1966"    
]
acNameList += [
    "Alberto Carvalho Júnior",
    "João Júnior",
    "Manuel Carvalho da Silva e do Silvo Júnior",
    "Manuel Carvalho Sénior",
    "Manuel do Ó",
    "Maria Albertina do Ó",
    "Rui Abrantes III",
    "Ruy Philippe Nery"
]
acNameList += [
    "João Rogado Grenhas",
    "João Manuel Grenhas",
    "Manuel_Almada_d1966",
    "João_M_P_M_Grenhas_d19680119",
    "João_R_Grenhas_d1941",
    "João_R_Grenhas_d194x",
    "João Rogado Grenhas (194x)",
    "Luzia__Grenhas_d1942"
]
acNameList += [
    "anb:João_M_P_M_Grenhas_d19680119",
    ":João_M_P_M_Grenhas_d19680119",
    "João_R_Grenhas_d1941",
    "João Rogado Grenhas (1941)",
    "Luzia__Grenhas 1942"
]

acNameList += [
    "anb:temAvô",
    "anb:João_M_P_M_Grenhas_d19680119",
    ":João_M_P_M_Grenhas_d19680119",
    ":J_M_P_M_Grenhas_d0000"
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
