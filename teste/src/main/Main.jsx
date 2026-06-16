import { useEffect, useState } from "react";
import './Main.css'

function Main () {
    /* Mensagens que aparecem na box como input*/
    const exemplo_input = [
    "Qual é a principal missão da Infraestruturas de Portugal ?",
    "É verdade que a Infraestruturas de Portugal tem mais de 1500km de via eletrificada ?",
    "Qual é o ano de fundação da Infraestruturas de Portugal ?",
    "A Infraestruturas de Portugal contribui para a mobilidade das pessoas e das mercadorias ?",
    "Porque é que a Infraestruturas de Portugal é considerada uma entidade única no contexto internacional ?",
    "Que desafios a Infraestruturas de Portugal enfrenta com o crescimento do tráfego e da mobilidade ?",
    "Como pode a Infraestruturas de Portugal influenciar a “coesão territorial” do país ?",
    "Como a Infraestruturas de Portugal garante continuidade do serviço em caso de obras ?",
    ""

    ];

    const [idx = randomNumberInRange (0, exemplo_input.length), setIdx] = useState(0); /* Índice das letras */
    const [text, setText] = useState(""); /* Excertos selecionados */

    /* Função que seleciona um número random */
    const randomNumberInRange = (min, max) => {
        return Math.floor(Math.random()
            * (max - min + 1)) + min;
    };
    
    useEffect (() => {
        
        let letra = 0;
        setText("")
        
        const excerto = exemplo_input[idx];

        const typing = setInterval(() => {
        
        setText(excerto.slice(0, letra + 1));
        letra ++;

        if (letra >= excerto.length){
            clearInterval(typing);
            
            setTimeout (() => {
                setIdx(() => randomNumberInRange(0, exemplo_input.length - 1));
            }, 2500)
        }
    }, 35);

        return () => clearInterval(typing); 

    }, [idx]);
    
    
    const [message, setMessage] = useState("")

    return (

    <div className = "container">

        <h1 className = "welcome"> Pronto para Ligar Destinos ? </h1>
        <input className = "input_text" type = "text" value = {message} onChange = {(msg) => setMessage (msg.target.value)} placeholder = {text}/>
        <button className = "button"> + </button>
        <p className = "footer"> Em desenvolvimento.. </p>

    </div>
    );
}

export default Main;