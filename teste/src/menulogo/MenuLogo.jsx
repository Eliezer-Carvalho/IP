import { useState } from 'react';
import logo from "./logos/IP_LogomarcaPrincipal_RGB-Cor.png";
import "./MenuLogo.css" 


function MenuLogo () {

    return (
        <div className = 'menu'>

            <img className = 'logo' src = {logo} alt = "Infraestruturas de Portugal"/>
            
            <h1 style = {{fontFamily: "Outfit, sans-serif"}}> Rag </h1>
            <p style = {{fontFamily: "Outfit, sans-serif"}}> Agentic  </p>
            
           
            

        </div>
    );
}


export default MenuLogo;
