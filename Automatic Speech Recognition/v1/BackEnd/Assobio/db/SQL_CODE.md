<h1> Algum código SQL </h1>

<h3> E se eu não sei o nome da tabela ? </h3>

```sql
SELECT name
FROM sqlite_master
WHERE type = 'table'
```
<hr>

<h3> E se eu quiser ver o nome das colunas da minha tabela ? </h3>

```sql
SELECT name
FROM pragma_table_info('nome da tabela')
```
<hr>