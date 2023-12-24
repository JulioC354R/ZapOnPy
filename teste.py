from ZapOnPy import ZOP
import json
import time
from commandos import Comandos
import os
import logging
from dados import Data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
dado = Data()


ficha = '''
*Ficha do Personagem*

OBS: Ao preencher os dados coloque sempre dentro dos >   <. 

#Nome:
>aaaaaaaaaaaaaaaaaaaaaaaaaa<

#Idade:
(Mínimo 18, máximo 30)
>27<

#Aparência:
(Apenas 2D e 3D)
>Cabelos longos e negros, olhos azuis como o oceano, estatura média, vestindo roupas elegantes<

#Personalidade:
>Inteligente, corajosa, leal, mas pode ser reservada com estranhos<

#História:
(Opcional)
>Nascida em uma família de nobres, Isabella cresceu em um castelo majestoso. Aprendeu desde jovem a arte da diplomacia e da esgrima. Um dia, decidiu deixar sua vida de nobre para trás em busca de aventuras e descobertas.<

#Sexualidade:
>Heterossexual<

#Gênero:
>Feminino<

#Altura:
>165 cm<

#Peso:
>55 kg<

#Organização:
(Yakuza ou Força-11) OBS: Preencha exatamente como está aqui!
>Força-11<


*Ficha de Stand*

Nome do Stand:
>aaaaaa<

Tipo de Stand:
(Consulte o sistema de Stand)
>distancia<
Habilidade: 
(1 slot inicial para técnicas)
>o carai de asa<

!ficha'''

inventario = '''
OBS: Ao preencher os dados coloque sempre dentro dos >   <. 
#Carteira:
(2.000¥ inicialmente, independente da organização)
>8.000¥<



#Inventário: >

-Espada Longa de Aço
-Armadura de Couro Reforçada
-Anel Mágico da Sabedoria
-Poções de Cura
<

(Consulte a lista de itens iniciais do inventário)
'''

pontos = '''
OBS: Ao preencher os dados coloque sempre dentro dos >   <. 
Atributos Personagem:
#Força_Física:          >100< 
#Resistência_Geral:     >8<
#Velocidade/Agilidade:  >9<
#Pontaria/Precisão:     >100<
#Total_de_Pontos:       (automático)

Pontos disponíveis: 

Atributos Stand:
#Força_Física:          >100< 
#Resistência_Geral:     >80<
#Velocidade/Agilidade:  >9<
#Pontaria/Precisão:     >10<
#Total_de_Pontos:       (automático)

Pontos disponíveis: 

(300 pontos iniciais para distribuição)

'''


cena = """!cena player 0🧚🏻‍♀
              ⊰᯽⊱┈──╌❊╌──┈⊰᯽⊱
                         𝑬𝒍𝒂𝒓𝒂 𝑪𝒆𝒍𝒆𝒔𝒕𝒆
                         𝓓𝓻𝓮𝓪𝓶 𝓯𝓪𝓲𝓻𝔂
              ⊰᯽⊱┈──╌❊╌──┈⊰᯽⊱


• Treinamento solo.

Em meio à vastidão do bosque, Elara, a fada de asas iridescentes, dedicava-se com afinco às acrobacias de voo. Seu corpo leve e ágil desenhava arabescos no ar, num balé harmonioso com os pássaros que ali também teciam suas rotas. Era uma dança aérea, uma competição amistosa, onde cada curva e loop eram aplaudidos pelas folhas sussurrantes das árvores centenárias.

Desde a alvorada, quando o sol ainda timidamente acariciava as copas das árvores, até o crepúsculo, onde suas últimas luzes se escondiam atrás das montanhas, ela treinava. Seu voo não era somente um meio de deslocamento; era a expressão mais pura de sua essência. No entanto, como tudo que é intenso e devotado, o cansaço se abateu sobre Elara. Seus movimentos, antes repletos de vigor e precisão, começaram a se tornar lentos e pesados. As asas, que brilhavam sob o sol como pedras preciosas, agora pareciam carregar o peso do dia inteiro de esforços incessantes.

Ao final desse dia exaustivo, Elara, em sua busca por algo que pudesse revigorar seu espírito, deparou-se com um cogumelo. Não era um cogumelo comum; tinha cores vivas e uma aura quase mística. Movida por uma curiosidade inata e um desejo de escapismo, ela o consumiu, sem hesitar. Quase instantaneamente, o mundo ao seu redor começou a se transformar. As cores se intensificaram, os sons da floresta ganharam novas melodias, e as formas da natureza pareciam dançar ao ritmo de uma canção desconhecida. Elara se viu imersa em um mundo de sonhos, um universo paralelo onde a realidade se dobrava e estendia de maneiras inimagináveis.

Nesse mundo, as regras da física não se aplicavam. Elara podia voar mais alto e mais rápido do que jamais fizera. Ela atravessava nuvens que se transformavam em figuras fantásticas, conversava com estrelas que contavam segredos do universo, e dançava com as sombras que se moviam ao seu próprio comando. Era um mundo maluco, onde cada momento trazia uma nova surpresa, uma nova aventura. Elara sentiu-se livre, desprendida das amarras da realidade, explorando possibilidades que nunca ousara imaginar. Essa viagem onírica, entretanto, tinha seu preço. A fada começou a sentir uma leveza excessiva, como se estivesse se desfazendo, se tornando parte daquele sonho etéreo.

Conforme a noite avançava, o encanto do mundo dos sonhos começou a desvanecer. Elara, agora inundada por uma sensação de serenidade e cansaço, sentiu suas pálpebras pesarem. Aos poucos, ela foi se deixando levar pelo chamado do sono, enquanto o mundo dos sonhos se esvaía como névoa ao amanhecer. Quando finalmente adormeceu, Elara estava de volta ao seu lar na floresta, envolta pela segurança das árvores e pela tranquilidade da noite. Seus sonhos, embora menos vívidos que a experiência vivida, ainda carregavam ecos daquela jornada fantástica. E assim, no silêncio reconfortante do bosque, a fada descansava, recuperando-se para mais um dia de voo e descobertas."""


logging.basicConfig(
    filename='BotAutoPy.log',  # Nome do arquivo de log
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

bot = ZOP(True, False)
comm = Comandos(bot)

while True:

    new_messages = bot.check_new_messages()
    if new_messages:
        msgs = bot.get_messages_in()
        print(msgs)
        bot.forward_message(-1, ["Julio Developer", "𝙱𝙸𝚉𝙰𝚁𝚁𝙴 𝙳𝙴𝚂𝚃𝙸𝙽𝚈 – 𝑭𝑰𝑪𝑯𝑨𝑺"])
        bot.close_chat()
