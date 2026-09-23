import laya

"""
Esta class surge como implementação de um Model Routing usando um System One Model que tem como principal
objetivo retornar texto estruturado que sirvam como apoio para a tomada de decisão.

#https://huggingface.co/convaiinnovations/laya
#https://docs.typesafe.ai/concepts/system-one

"""

class System_One_Model_Routing:

    def __init__ (self):

        self.Laya = None

    def Model_Routing (self, TRANS):

        if self.Laya is None:

            self.Laya = laya.load (r"C:\Users\Admin\Desktop\models\System One Models\Laya", device = "cuda")

        STATE = TRANS

        CONTRACTS = {

            "DECISION": {
                "type": "choice",
                "instructions": ("You should select the most appropriate hardware to perform a concise and thorough audit based on the complexity of the transcript."
                                "You should take into account the complexity and length of the sentence."),

                "criteria": {
                    "GPU": ("Model inference will be performed on a GPU."),
                    "CPU": ("Model inference will be performed on a CPU.")
                }
            }
        }

        DECISION = self.Laya.predict (STATE, CONTRACTS)

        return (DECISION["answers"]["DECISION"]["choice"])



"""
x = System_One_Model_Routing ()


for y in range (5):

    z = time.time ()

    x.Model_Routing (" Boa tarde, estou-lhe a ligar aqui por causa do T1 que vocês têm. O senhor está a ver alguma placa, é isso? O meu sobrinho é que me trouxe isto aqui para casa, que é mesmo ali nos prazeres, mesmo ali na rua, ali do cemitério. O meu sobrinho deu-me aqui o ID do anúncio. Isto é que é importante, diga-me lá o ID. 503. 503. Tracinho. Um zero. Porque ele diz que é para aqui que eu tenho que vir, que tenho que comprar este. Ai, que horror. Diga. O senhor deu-me bem o número de 53 Ds. É, é esse. Que é um T1, como esse sobrinho diz que é para aí que eu tenho que ir. É para aí que o senhor tem que ir. Sim. Pode chegar a hora, não é? Então, era agora em janeiro, agora... É para aí.")

    t = time.time () - z
    print (t)

Resultados:

CPU
38.112754583358765
CPU
0.1778240203857422
CPU
0.18289852142333984
CPU
0.18429088592529297
CPU
"""