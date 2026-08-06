<h1> O que Docker resolve ? </h1>

Imaginemos que eu desenvolvo uma aplicação Python com imensas dependências, na minha máquina tudo funciona porque é a máquina raiz do projeto. <br>
Mas eu agora quero enviar para um amigo para ele usar a aplicação na sua máquina, <b>já não funciona</b>! <br>
Isto pode acontecer por vários motivos mas os mais comuns é a instalação de dependências com versões diferentes, versão do Python diferente ... <br>

<b> Docker</b> resolve exatamente isto criando um ambiente isolado com todas as dependências que a aplicação precisa para funcionar. <br>
O Docker empacota código, dependências, runtime e configurações. Assim desta maneira, corre igual em todos os computadores.



<h1> Arquitetura do Docker </h1>

Docker CLI -> Docker Daemon -> Images -> Containers

<ul>
    <li> Docker CLI -> É o CLI do Docker </li>
    <li> Docker Daemon -> É a Engine do Docker </li>
    <li> Images -> Templates </li>
    <li> Container -> São images em execução </li>
</ul>


<h1> Container </h1>

Um Container é o processo isolado. É a caixa onde fica todas as dependências. <br>
Consiste num processo Linux que contêm filesystem próprio, rede própria, utilizadores próprios e processos próprios. <br>

É diferente de uma <b>Máquina Virtual</b>, um VM transporta tudo, sistema operativo, filesystem etc.. <b>É muito mais pesado!</b> <br>


<table>
        <tr>
            <th> Virtual Machine </th>
            <th> Docker </th>
        </tr>
    
        <tr>
            <td> Sistema Operativo Completo </td>
            <td> Apenas Aplicação </td>
        </tr>
    
        <tr>
            <td> GB de Tamanho </td>
            <td> MB de Tamanho </td>
        </tr>
    
        <tr>
            <td> Arranque em Minutos </td>
            <td> Arranque em Segundos </td>
        </tr>
    
        <tr>
            <td> Mais Isolamento </td>
            <td> Menos Isolamento </td>
        </tr>
        
        <tr>
            <td> Mais Consumo </td>
            <td> Muito Leve </td>
        </tr>
</table>
    


<h1> Imagem </h1>



<h1> Imagem </h1>

Uma Imagem corresponde ao resultado da execução de um Docker File. <br>
O Docker File é a receita, e o bolo é o que chamamos de Imagem. 


<h1> Docker File </h1>

<b> Docker File </b> é o conjunto de instruções que diz como construir uma Imagem.


<table>
    <tr>
        <th> FROM </th>
        <th> WORKDIR </th>
        <th> COPY </th>
        <th> RUN </th>
        <th> CMD </th>
    </tr>

    <tr>
        <td> Seleciona a Imagem Base </td>
        <td> Define a pasta onde os comandos vão ser executados </td>
        <td> Copia ficheiros do Computador para a Imagem </td>
        <td> Executa comandos </td>
        <td> Comando executado quando o container inicia </td>
    </tr>
</table>



<img src = "https://media.geeksforgeeks.org/wp-content/uploads/20260408182110268940/docker_image.webp">



<h1> Docker Cheatsheet </h1>


<table>
    <tr>
        <th> Descarregar imagem </th>
        <th> Construir imagem </th>
        <th> Executar </th>
        <th> Listar containers </th>
        <th> Listar todos </th>
        <th> Ver imagens </th>
        <th> Ver logs </th>
        <th> Parar </th>
        <th> Remover container </th>
        <th> Remover imagem </th>
    </tr>




<h1> Docker Containers e Dados </h1>


<h3> Bind Mount </h3>

Ao criar um Container podemos querer usar dados que estão dentro do nosso computador, como modelos de IA entre outros. <br>
Para isso, usamos <b> Bind Mount</b>. <br>
Bind Mount liga uma pasta pessoal do computador ao Container. <br>


<h3> Docker Volumes </h3>

Podemos também usar Docker Volumes para hospedar os nossos dados no Docker e depois ligamos ao Container.


<h3> COPY Dockerfile </h3>

Se forem dados com alguns MB, podemos também passar direto para o Container.



