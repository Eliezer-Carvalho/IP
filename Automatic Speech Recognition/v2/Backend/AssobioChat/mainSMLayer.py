from .SemanticLayer import Semantic_Layer

SML = Semantic_Layer ()

def RUN_SEMANTIC_LAYER (PROMPT, DATABASE = "Assobio"):

    SML.SEMANTIC_LAYER (PROMPT)
    SQL = SML.QUERY_COMPILER (DATABASE)
    OUTPUT_SQL = SML.SQL_ENGINE (SQL)

    #print (OUTPUT_SQL)
    return OUTPUT_SQL