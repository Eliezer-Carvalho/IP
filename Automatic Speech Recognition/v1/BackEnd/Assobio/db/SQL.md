<h1> SQL - Structured Query Language </h1>
<p> Linguagem utilizada para comunicar com bases de dados. </p>
<hr>

<h3> CREATE </h3>
Criar tabelas

```sql
CREATE TABLE clientes (id INTEGER, nome TEXT) 
```
<hr>



<h3> INSERT </h3>
Inserir dados

```sql
INSERT INTO clientes VALUES (23, 'Ana')
```
<hr>



<h3> READ </h3>
Selecionar tudo

```sql
SELECT * FROM clientes
```

Selecionar algumas colunas
```sql
SELECT id, nome FROM clientes 
```

Renomear colunas
```sql
SELECT nome AS cliente, idade AS anos FROM clientes
```
<hr>




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

































































































































































































































































