import { useEffect, useState } from "react";
import './Main.css'

function Main () {
    /* Mensagens que aparecem na box como input*/
    const exemplo_input = [
    "Qual é a principal missão da Infraestruturas de Portugal ?",
    "É verdade que a Infraestruturas de Portugal tem mais de 1500km de via eletrificada ?",
    "É verdade que a Infraestruturas de Portugal gere as redes rodoviária e ferroviária nacionais?",
    "Será que a IP apenas planeia infraestruturas sem qualquer intervenção na sua execução?",
    "Não será a IP uma peça central na forma como o país garante mobilidade e acessibilidade em larga escala?"
    ];

    const [idx, setIdx] = useState(0); /* Índice das letras */
    const [text, setText] = useState(""); /* Excertos selecionados */

    useEffect (() => {
        
        let letra = 0;
        setText("")

        const typing = setInterval(() => {
        
        setText(exemplo_input[idx].slice(0, letra + 1));
        letra ++;

        if (letra >= exemplo_input[idx].length){
            clearInterval(typing);
            
            setTimeout (() => {
                setIdx((ultimo) => (ultimo + 1) % exemplo_input.length);
            }, 2000)
        }}, 35);

        return () => clearInterval(typing); 

    }, [idx]);
    
    
    const [message, setMessage] = useState("")

    return (

    <div className = "x">
    <div className = "background-glow">

        <h1 className = "welcome"> Pronto para Ligar Destinos ? </h1>
        <input className = "barra" type = "text" value = {message} onChange = {(msg) => setMessage (msg.target.value)} placeholder = {text}/>
        <button className = "button"> + </button>

        <p className = "footer"> Em desenvolvimento.. </p>
    </div>
    </div>
    );
}

export default Main;