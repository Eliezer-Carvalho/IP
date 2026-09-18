import yaml
import gradio as gr

from transformers import AutoTokenizer, AutoModelForCausalLM
import outlines

from pydantic import BaseModel
import torch
import json

import sqlite3


"""
Esta classe trata da parte da Camada Semântica.
"""

class Semantic_Layer:

    def __init__ (self):
 
        self.device = "cuda" if torch.cuda.is_available () else "cpu"
        self.SEMANTIC_QUERY = None

        self.TOKENIZER = None
        self.SLM = None

        self.DB_PATH = r"C:\Users\Admin\Desktop\ip\Automatic Speech Recognition\v2\Backend\AssobioAuditoria\DatabaseAssobioAuditoria\SQLDatabaseAssobio.db"

        with open (r"C:\Users\Admin\Desktop\ip\Automatic Speech Recognition\v2\Backend\AssobioChat\SemanticLayerModel.yaml", "r", encoding = "utf-8") as f:
            self.SEMANTIC_MODEL = yaml.safe_load (f)

        with open (r"C:\Users\Admin\Desktop\ip\Automatic Speech Recognition\v2\Backend\AssobioChat\SYSTEM_PROMPT_SMLAYER.md", "r", encoding = "utf-8") as f:
            self.SYSTEM_PROMPT = f.read ()


    def GRADIO_SEMANTIC_LAYER_ACTIVE (self, ESTADO):

        #print (ESTADO)

        if ESTADO == "Camada Semântica: OFF":
            return gr.update (value = "Camada Semântica: ON", variant = "primary"), True

        elif ESTADO == "Camada Semântica: ON":
            return gr.update (value = "Camada Semântica: OFF", variant = "primary"), False


    def SEMANTIC_LAYER (self, PROMPT):

        if self.SLM == None:

            self.TOKENIZER = AutoTokenizer.from_pretrained (r"C:\Users\Admin\Desktop\models\Language Models\CPU\Mistral 7B Q4 BnB")
            self.SLM = AutoModelForCausalLM.from_pretrained (r"C:\Users\Admin\Desktop\models\Language Models\CPU\Mistral 7B Q4 BnB", device_map = self.device, dtype = torch.float16)

        class Format_Constraint (BaseModel):
            function: str
            cols: str

        CONSTRAINT = outlines.from_transformers (self.SLM, self.TOKENIZER)

        MENSAGENS = [
            {"role": "system", "content": f"{self.SYSTEM_PROMPT}" f"{self.SEMANTIC_MODEL}"},
            {"role": "user", "content": PROMPT}
        ]

        MENSAGENS = self.TOKENIZER.apply_chat_template (MENSAGENS, tokenize = False, add_generation_prompt = True)

        self.SEMANTIC_QUERY = CONSTRAINT (MENSAGENS, output_type = Format_Constraint, max_new_tokens = 50)
        self.SEMANTIC_QUERY = json.loads (self.SEMANTIC_QUERY)
        

    def QUERY_COMPILER (self, DATABASE):

        FUNCTION = self.SEMANTIC_QUERY ["function"]
        COLS = self.SEMANTIC_QUERY ["cols"]

        SQL = None

        if self.SEMANTIC_MODEL ["FUNCTIONS"][FUNCTION]["type"] == "return_all":

            SQL = f"""
            SELECT {COLS}
            FROM {DATABASE}
            """

        if self.SEMANTIC_MODEL ["FUNCTIONS"][FUNCTION]["type"] == "return_len":

            SQL = f"""
            SELECT COUNT (*)
            FROM {DATABASE}
            """

        return SQL

    def SQL_ENGINE (self, SQL):

        CONECTOR = sqlite3.connect (self.DB_PATH)
        CURSOR = CONECTOR.cursor ()

        QUERY = CURSOR.execute (SQL).fetchall ()

        return QUERY
        