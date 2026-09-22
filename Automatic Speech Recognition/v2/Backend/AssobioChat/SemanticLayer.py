import yaml

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
        self.QUERY = None

        self.TOKENIZER = None
        self.SLM = None

        self.DB_PATH = r"C:\Users\Admin\Desktop\ip\Automatic Speech Recognition\v2\Backend\AssobioAuditoria\DatabaseAssobioAuditoria\SQLDatabaseAssobio.db"

        with open (r"C:\Users\Admin\Desktop\ip\Automatic Speech Recognition\v2\Backend\AssobioChat\SystemPrompts\SemanticModel.yaml", "r", encoding = "utf-8") as f:
            self.SEMANTIC_MODEL = yaml.safe_load (f)

        with open (r"C:\Users\Admin\Desktop\ip\Automatic Speech Recognition\v2\Backend\AssobioChat\SystemPrompts\SYSTEM_PROMPT_SMLAYER.md", "r", encoding = "utf-8") as f:
            self.SYSTEM_PROMPT = f.read ()


    def SEMANTIC_QUERY (self, PROMPT):

        if self.SLM == None:

            self.TOKENIZER = AutoTokenizer.from_pretrained (r"C:\Users\Admin\Desktop\models\Language Models\CPU\Mistral 7B Q4 BnB")
            self.SLM = AutoModelForCausalLM.from_pretrained (r"C:\Users\Admin\Desktop\models\Language Models\CPU\Mistral 7B Q4 BnB", device_map = self.device, dtype = torch.float16)

        class Format_Constraint (BaseModel):
            operation: str
            columns: str

        CONSTRAINT = outlines.from_transformers (self.SLM, self.TOKENIZER)

        MENSAGENS = [
            {"role": "system", "content": f"{self.SYSTEM_PROMPT}" f"{self.SEMANTIC_MODEL}"},
            {"role": "user", "content": PROMPT}
        ]

        MENSAGENS = self.TOKENIZER.apply_chat_template (MENSAGENS, tokenize = False, add_generation_prompt = True)

        self.QUERY = CONSTRAINT (MENSAGENS, output_type = Format_Constraint, max_new_tokens = 50)
        self.QUERY = json.loads (self.QUERY)
        

    def QUERY_COMPILER (self, DATABASE):

        OPERATION = self.QUERY ["operation"]
        COLS = self.QUERY ["columns"]
        print (OPERATION, COLS)

        SQL = None

        if self.SEMANTIC_MODEL ["OPERATIONS"][OPERATION]["type"] == "return_all":

            SQL = f"""
            SELECT {COLS}
            FROM {DATABASE}
            """

        if self.SEMANTIC_MODEL ["OPERATIONS"][OPERATION]["type"] == "return_len":

            SQL = f"""
            SELECT COUNT (*)
            FROM {DATABASE}
            """

        if self.SEMANTIC_MODEL ["OPERATIONS"][OPERATION]["type"] == "mean":

            SQL = f"""
            SELECT AVG ({COLS})
            FROM {DATABASE}
            """

        if self.SEMANTIC_MODEL ["OPERATIONS"][OPERATION]["type"] == "sum":

            SQL = f"""
            SELECT SUM ({COLS})
            FROM {DATABASE}
            """

        return SQL


    def SQL_ENGINE (self, SQL):

        CONECTOR = sqlite3.connect (self.DB_PATH)
        CURSOR = CONECTOR.cursor ()

        QUERY = CURSOR.execute (SQL).fetchall ()

        return QUERY, SQL


"""
Run
"""
SML = Semantic_Layer ()

def RUN_SEMANTIC_LAYER (PROMPT, DATABASE = "Assobio"):

    SML.SEMANTIC_QUERY (PROMPT)
    SQL = SML.QUERY_COMPILER (DATABASE)
    OUTPUT_SQL, SQL_QUERY = SML.SQL_ENGINE (SQL)

    #print (OUTPUT_SQL)
    return OUTPUT_SQL, SQL_QUERY