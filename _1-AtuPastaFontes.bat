rem P gina: DOS CP850
copy C:\MEI\_PE\Disserta‡Æo_20-21\ANB-Prototype\Lib\myLists.py NameSearch\
copy C:\MEI\_PE\Disserta‡Æo_20-21\ANB-Prototype\Lib\myStrings.py NameSearch\
copy C:\MEI\_PE\Disserta‡Æo_20-21\ANB-Prototype\myNames.py NameSearch\

@echo Fazer as seguintes adaptacoes:
@echo Em myNames.py:
@echo   "from Lib.myLists" === "from .myLists"
@echo   "from Lib.myStrings" === "from .myStrings"

@pause
