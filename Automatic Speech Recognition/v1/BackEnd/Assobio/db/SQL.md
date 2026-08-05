SQL - Structured Query Language é a linguagem utilizada para comunicar com bases de dados.





**CRUD são as 4 operações principais**



**Create**

Criar tabelas



"""

**CREATE** **TABLE** clientes (id **INTEGER,** nome **TEXT**) 

"""

\##########################################################





**Insert**

Inserir dados



"""

**INSERT INTO** clientes **VALUES** (23, 'Ana')

"""

\##########################################################





**Read**

Ler dados



""" Selecionar Tudo """

**SELECT \* FROM** clientes

"""



""" Selecionar algumas colunas """

**SELECT** id, nome **FROM** clientes 

"""



""" Renomear Colunas """

**SELECT** nome **AS** cliente, idade **AS** anos **FROM** clientes

\##########################################################





**Update**

Atualizar dados



"""

**UPDATE** clientes **SET** nome = "Eliezer" **WHERE** id = 1

"""

\##########################################################





**Delete**

Eliminar dados



"""

**DELETE FROM** clientes **WHERE** id = 1

"""

\##########################################################





**Where**

Selecionar dados 



""" Filtragem """

**SELECT \* FROM** clientes **WHERE** id > 10

"""



""" Múltipla Filtragem """

**SELECT \* FROM** clientes **WHERE** id > 10 **AND** nome = "Sara"



**SELECT \* FROM** clientes **WHERE** id > 10 **OR** nome = "Sara"



**SELECT \* FROM** clientes **WHERE NOT** nome = "Sara"

"""

\##########################################################



**Operadores**



> - Maior

< - Menor

>= - Maior ou Igual

= - Igual

<> - Diferente de

\##########################################################





**Like**

Selecionar por texto



""" Começa por: """

**WHERE** nome **LIKE** "A%"

"""



""" Termina em: """

**WHERE** nome **LIKE** "%a"

"""



""" Contém: """

**WHERE** nome **LIKE** "%silva%"

"""

\##########################################################





**In**

Selecionar especificamente



"""

**WHERE** nome **IN** ("Eliezer", "Ana")

"""

\##########################################################





**Between** 

Entre



"""

**WHERE** id **BETWEEN** 20 **AND** 30

"""

\##########################################################







**Order By**

Ordenar



"""

**SELECT \* FROM** clientes **ORDER BY** id

"""



""" Decrescente """

**SELECT \* FROM** clientes **ORDER BY** id **DESC**

"""

\##########################################################







**Limit**

Limitar o número de linhas



"""

**SELECT \* FROM** clientes **LIMIT** 10

"""

\##########################################################







**Count**

Número de linhas - tipo len



"""

**SELECT COUNT(\*) FROM** clientes

"""

\##########################################################









**Distinct**

Eliminar dups



"""

**SELECT DISTINCT** nome **FROM** clientes

"""

\##########################################################







**Group By**

Fundamental para ML.

Imagina milhões de vendas e queremos saber quantos clientes por cidade por exemplo.





"""

**SELECT** cidade **COUNT(\*) AS** clientes **FROM** clientes **GROUP BY** cidade

"""

\##########################################################







**Join**

Merge de tabelas

































































































































































































































































