<h1> Algum código SQL </h1>

<h3> E se eu não sei o nome da tabela ? </h3>

```sql
SELECT name
FROM sqlite_master
WHERE type = 'table'
```