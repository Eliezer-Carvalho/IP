from openai import OpenAI


cliente = OpenAI (
    base_url = "http://127.0.0.1:8080",
    api_key = "local" 
)

response = cliente.chat.completions.create (
    model = "amalia_q2K",
    messages = [
        {
            "role": "user",
            "content": "Extrai os dados destas pessoas em formato JSON: João, 25 anos, Engenheiro Informático | Eliezer, 23 anos, AI Engineer"
        }
    ],
    response_format = {
        "type": "json_object",

        "properties": {
            "NOME": {
                "type": "string"
            }
        },
    
        "required": ["NOME"],
    
        "additionalProperties": False
    }
)


print (response)


'''response_format = {
        ''"type": "json_object",
        "schema": {

            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "NOME": {
                        "type": "string"
                    },
                    "IDADE" : {
                        "type": "integer"
                    },
                    "PROFISSÃO" : {
                        "type": "string"
                    }
                },

                "required": [
                    "NOME",
                    "IDADE"
                ],

                "additionalProperties": False
            }
        }   
    }
)'''


'''
Assim funciona com uns

    response_format = {
    "type": "json_object",

    "properties": {
        "NOME": {
            "type": "string"
        }
    },

    "required": ["NOME"],

    "additionalProperties": False
    }
)'''


'''    
response_format = {
        ''"type": "json_object",
        "schema": {

            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "NOME": {
                        "type": "string"
                    },
                    "IDADE" : {
                        "type": "integer"
                    },
                    "PROFISSÃO" : {
                        "type": "string"
                    }
                },

                "required": [
                    "NOME",
                    "IDADE"
                ],

                "additionalProperties": False
            }
        }   
    }
)
'''