<h1> SQL - Structured Query Language </h1>
<p> Linguagem utilizada para comunicar com bases de dados. </p>
<hr>

<h3> Fetch </h3>

<ul>
    <li> fetchone </li>
    <li> fetchall </li>
    <li> fetchmany (10) </li>
</ul>
<hr>



<h3> CREATE </h3>
Criar tabelas

```sql
CREATE TABLE clientes (id INTEGER PRIMARY KEY, nome TEXT NOT NULL) 
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



<h3> UPDATE </h3>
Atualizar dados

```sql
UPDATE clientes SET nome = 'Eliezer' WHERE id = 1
```
<hr>



<h3> DELETE </h3>
Eliminar dados

```sql
DELETE FROM clientes WHERE id = 1
```
<hr>



<h3> WHERE </h3>
Filtragem

```sql
SELECT * FROM clientes WHERE id > 10
```

Múltipla Filtragem

```sql
SELECT * FROM clientes WHERE id > 10 AND nome = 'Sara'
```
```sql
SELECT * FROM clientes WHERE id > 10 OR nome = 'Sara'
```
```sql
SELECT * FROM clientes WHERE NOT nome = 'Sara'
```
<hr>


<h3> LIKE </h3>
Começa por:

```sql
WHERE nome LIKE 'A%'
```

Termina em: 
```sql
WHERE nome LIKE '%a'
```

Contém:
```sql
WHERE nome LIKE '%silva%'
```
<hr>



<h3> IN </h3>
Selecionar especificamente

```sql
WHERE nome IN ('Eliezer', 'Ana')
```
<hr>



<h3> BETWEEN </h3> 
Entre

```sql
WHERE id BETWEEN 20 AND 30
```
<hr>

<h3> ORDER BY </h3>
Ordenar

```sql
SELECT * FROM clientes ORDER BY id
```

Decrescente
```sql
SELECT * FROM clientes ORDER BY id DESC
```
<hr>


<h3> LIMIT </h3>
Limitar o número de linhas

```sql
SELECT * FROM clientes LIMIT 10
```
<hr>

<h3> COUNT </h3>
Número de linhas

```sql
SELECT COUNT(*) FROM clientes
```
<hr>


<h3> DISTINCT </h3>
Eliminar dups

```sql
SELECT DISTINCT nome FROM clientes
```
<hr>


