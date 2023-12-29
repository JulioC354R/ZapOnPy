from options import *
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

bot = ZOP(True, True)
comm = Comandos(bot)

while True:

    time.sleep(2)
    bot.search_contact("Julio Developer")
    # bot.react_a_message(complete, React_options.HEART)
    bot.send_message_on_chat("""𝓦𝓮𝓵𝓬𝓸𝓶𝓮 𝓽𝓸 𝓽𝓱𝓮 𝓐𝓮𝓼𝓽𝓱𝓮𝓽𝓲𝓬 𝓌𝓸𝓻𝓵𝓭! ꧁#𝟙꧂ ✨

𝕰𝖘𝖙𝖆 é 𝔰𝔬 𝔟𝔢𝔞𝔲𝔱𝔦𝔣𝔲𝔩! ★༄ᶦᶰᵈ᭄

𝓢𝓸𝓶𝓮 𝓯𝓪𝓷𝓬𝔂 𝓬𝓱𝓪𝓻𝓪𝓬𝓽𝓮𝓻𝓼:awdwdawf
                             fefe
                             fesf
                             Efs/
                             g
                             [.g
                             Gp[e
                             EO GNue
                             
                             ]]

1. 𝓐 𝓵𝓲𝓯𝓮 𝓬𝓱𝓪𝓷𝓰𝓮𝓼 𝓲𝓼 𝓵𝓲𝓴𝓮 𝓻𝓲𝓭𝓲𝓷𝓰 𝓪 𝓫𝓲𝓬𝔂𝓬𝓵𝓮. 🚴‍♂️
2. 𝓞 𝓬𝓸𝓷𝓱𝓮𝓬𝓲𝓶𝓮𝓷𝓽𝓸 é 𝓸 𝓾𝓷𝓲𝓬𝓸 𝓽𝓮𝓼𝓸𝓾𝓻𝓸 𝓺𝓾𝓮 𝓷𝓪̃𝓸 𝓹𝓸𝓭𝓮 𝓼𝓮𝓻 𝓻𝓸𝓾𝓫𝓪𝓭𝓸.
3. 𝓤𝓶 𝓼𝓶𝓲𝓵𝓮 é 𝓸 𝓾𝓷𝓲𝓬𝓸 𝓽𝓮𝓼𝓸𝓾𝓻𝓸 𝓺𝓾𝓮 𝓷ã𝓸 𝓹𝓸𝓭𝓮 𝓼𝓮𝓻 𝓻𝓮𝓵𝓪𝓬𝓪𝓸 𝓪̀ 𝓯𝓮. 😃❤️

𝓐𝓺𝓾𝓲 𝓮𝓼𝓽á 𝓾𝓶 𝓵𝓲𝓷𝓴 𝓲𝓷𝓽𝓮𝓻𝓮𝓼𝓼𝓪𝓷𝓽𝓮 𝓹𝓪𝓻𝓪 𝓿𝓸𝓬ê 𝓮𝔁𝓹𝓵𝓸𝓻𝓪𝓻!
[ChatGPT 𝓭𝓪 𝓞𝓹𝓮𝓷𝓐𝓘](https://www.openai.com)

𝓔𝓼𝓹𝓮𝓻𝓪𝓶𝓸𝓼 𝓺𝓾𝓮 𝓿𝓸𝓬ê 𝓪𝓬𝓱𝓮 𝓾𝓽𝓲𝓵𝓲𝔃𝓪𝓻𝓶𝓸𝓼 𝓼𝓾𝓪 𝓲𝓷𝓽𝓮𝓻𝓪çã𝓸! 𝓢𝓮 𝓽𝓲𝓿𝓮𝓻 𝓶𝓪𝓲𝓼 𝓹𝓮𝓻𝓰𝓾𝓷𝓽𝓪𝓼, 𝓼𝓮𝓷𝓽𝓪-𝓼𝓮 𝓪 𝓿𝓸𝓬ê 𝓮𝓼𝓽á 𝓪𝓭𝓸𝓻𝓪𝓻. 🚀
                             
Ae pessoal, recebi isso aqui por e-mail a um tempo atrás, então já vou adiantando que é coisa velha e o texto é gigante, se não quiser não leia e espere um resumo ou comentários do pessoal. Não tem muita graça mas to postando pois alguém pode gostar e como o boteco tá meio parado mesmo, aqui vai o texto:

Meu nome é Afonso Soares de Melo, e resolvi contar algo que se passou comigo: Estava sentado no meu escritório quando lembrei de uma chamada telefônica que tinha que fazer. Encontrei o número e disquei. Atendeu-me um cara mal humorado dizendo:
- Fale!!!
- Bom dia. Poderia falar com Andréa? O cara do outro lado resmungou algo que não entendi e desligou na minha cara. Não podia acreditar que existia alguém tão grosso. Depois disso, procurei na minha agenda o número correto da Andréa e liguei. O problema era que eu tinha invertido os dois últimos dígitos do seu número. Depois de falar com a Andréa, observei o número errado ainda anotado sobre a minha mesa. Decidi ligar de novo. Quando a mesma pessoa atendeu, falei:
- Você é um Fdp!!! Desliguei imediatamente e anotei ao lado do número a expressão "Fdp" e deixei o papel sobre a minha agenda. Assim, quando estava nervoso com alguém, ou em um mau momento do dia, ligava prá ele, e quando atendia, lhe dizia "Você é um Fdp" e desligava sem esperar resposta. Isto me fazia sentir realmente muito melhor. Ocorre que a Telepar introduziu o novo serviço "bina" de identificação de chamadas, que me deixou preocupado e triste porque teria que deixar de ligar para o "Fdp". Então, tive uma idéia: disquei o seu número de telefone, ouvi a sua voz dizendo "Alô " e mudei de identidade:
- Boa tarde, estou ligando da área de vendas da Telepar, para saber se o senhor conhece o nosso serviço de identificador de chamadas "bina".
- Não estou interessado! - disse ele, e desligou na minha cara. O cara era mesmo mal-educado. Rapidamente, disquei novamente:
- Alô?
- É por isso que você é um Fdp!!! e desliguei. Aqui vale até uma sugestão: se existe algo que realmente está lhe incomodando, você sempre pode fazer alguma coisa para se sentir melhor: simplesmente disque o número de algum outro Fdp que você conheça, e diga para ele o que ele realmente é. Acontece que eu fui até o shopping, no centro da cidade, comprar umas camisas. Uma senhora estava demorando muito tempo para tirar o carro de uma vaga no estacionamento. Cheguei a pensar que nunca fosse sair. Finalmente seu carro começou a mover-se e a sair lentamente do seu espaço. Dadas às circunstâncias, decidi retroceder meu carro um pouco para dar à senhora todo o espaço que fosse necessário: "Grande!" pensei, "finalmente vai embora". Imediatamente, apareceu um Vectra preto vindo do outro lado do estacionamento e entrou de frente na vaga da senhora que eu estava esperando. Comecei a tocar a buzina e a gritar:

- Ei, amigo. Não pode fazer isso! Eu estava aqui primeiro! - O fulano do Vectra simplesmente desceu do carro, fechou a porta, ativou o alarme e caminhou no sentido do shopping, ignorando a
minha presença, como se não estivesse ouvindo. Diante da sua atitude, pensei: "Esse cara é um grande Fdp! Com toda certeza tem uma grande quantidade de Filhos da puta neste mundo!". Foi aí que percebi que o cara tinha um aviso de "VENDE-SE" no vidro do Vectra. Então,
anotei o seu número telefônico e procurei outra vaga para estacionar. Depois de alguns dias, estava sentado no meu escritório e acabara de desligar o telefone após ter discado o número do meu velho amigo e dizer "Você é um Fdp" (agora já é muito fácil discar pois tenho o seu número na memória do telefone), quando vi o número que havia anotado do cara do Vectra
preto e pensei: "Deveria ligar para esse cara também". E foi o que fiz. Depois de um par de toques alguém atendeu:
- Alô.
- Falo com o senhor que está vendendo um Vectra preto?
- Sim, é ele.
- Poderia me dizer onde posso ver o carro?
- Sim, eu moro na Rua XV, n° 527. É uma casa amarela e o Vectra está estacionado na frente.
- Qual e o seu nome?

- Meu nome e Eduardo Cerqueira Marques - diz o cara.
- Qual a hora é mais apropriada para encontrar com você, Eduardo?
- Pode me encontrar em casa à noite e nos finais de semana.
- É o seguinte Eduardo, posso te dizer uma coisa?
- Sim.
- Eduardo, você é um grande Fdp!!! - e desliguei o telefone. Depois de desligar, coloquei o número do telefone do Eduardo (que parecia não ter "bina", pois não fui importunado depois que falei com ele) na memória do meu telefone. Agora eu tinha um problema: eram dois "Filhos da puta" para ligar. Após algumas ligações ao par de "Filhos da puta" e desligar-lhes, a coisa não era tão divertida como antes. Este problema me parecia muito sério e pensei em
uma solução: em primeiro lugar, liguei para o "Fdp 1". O cara, mal-educado como sempre, atendeu:
- Alô - e então falei:
- Você é um Fdp - mas desta vez não desliguei. O "Fdp 1" diz:

- Ainda está aí, desgraçado?

- Siiimmmmmmmm, amorrrrrr!!! - respondi rindo.

- Pare de me ligar, seu filho da mãe - disse ele, irritadíssimo.

- Não paro nããão, Filho da ******* querido!!!
- Qual é o teu nome, lazarento? - berrou ele, descontrolado! Eu, com voz séria de quem também está bravo, respondi:
- Meu nome é Eduardo Cerqueira Marques, seu Filho da Puta. Porquê???
- Onde você mora, que eu vou aí te pegar, desgraçado? - gritou ele.

- Você acha que eu tenho medo de um Fdp? Eu moro na Rua XV, n°527, em uma casa amarela, e o meu Vectra preto está estacionado na frente, seu palhaço fdp. E agora, vai fazer o quê???? - gritei eu.
- Eu vou até aí agora mesmo, cara. É bom que comece a rezar, porque você já era. - rosnou ele.
- Uuiii! É mesmo? Que medo me dá, Fdp. Você é um bosta! E eu estou na porta da minha casa te esperando!!! - e desliguei o telefone na cara dele. Imediatamente liguei para o "Fdp 2".
- Alô - diz ele.

- Olá, grande Fdp!!! - falei.
- Cara, se eu te encontrar vou...
- Vai o quê? O que você vai fazer??? Seu Fdp!
- Vou chutar a sua boca até não ficar nenhum dente, cara!!!
- Acha que eu tenho medo de você, Fdp? Vou te dar uma grande oportunidade de tentar chutar minha boca, pois estou
indo para tua casa, seu Fdp!!! E depois de arrebentar sua cara, vou quebrar todos os vidros desta porcaria de Vectra que você tem. E reze pra eu

não botar fogo nessa casa amarelinha de bicha. Se for homem, me espera na porta em 5 minutos, seu Fdp!!! - e bati o telefone no gancho. Logo, fiz outra ligação, desta vez para a polícia. Usando uma voz afetada e chorosa, falei que estava na Rua XV, n° 527, e que ia matar o meu namorado homossexual assim que ele chegasse em casa. Finalmente peguei o telefone e liguei o programa da CNT "Cadeia" do Alborguetti, para reportar que ia começar uma briga de um marido que ia voltando mais cedo para casa para pegar o amante da mulher que morava na Rua XV, n° 527. Depois de fazer isto, peguei o meu carro e fui para Rua XV, n° 527, para ver o espetáculo. Foi demais, observar um par de "Filhos da puta" chutando-se na frente de duas equipes de reportagem, até a chegada de 3 viaturas e um helicóptero da polícia, levando os dois algemados e arrebentados para a delegacia.

Moral da história? - Não tem moral nenhuma! Foi de sacanagem mesmo... E vê se atende o telefone educadamente, pois posso ser eu ligando para você por engano...

""")

    # last_message_out = bot.get_messages_elements(Msg_options.IN)[-1]
    # complete = bot.find_message_complete_element(last_message_out)
    # bot.react_a_message(complete, React_options.HEART)
    time.sleep(0.5)
    # bot.send_file_in_input(Input_options.DOCUMENT, r"C:\Users\julyo\Music\[AMV] Kizumonogatari - Castle(MP3_160K).mp3", "Se liga no som")
    bot.close_chat()
    # campo = bot.find_field(Field_options.MESSAGE)
    # time.sleep(1)
    # campo.send_keys("Favoritado", Keys.ENTER)

    time.sleep(500000)
    # bot.forward_message(-1, ["Julio Developer", "𝙱𝙸𝚉𝙰𝚁𝚁𝙴 𝙳𝙴𝚂𝚃𝙸𝙽𝚈 – 𝑭𝑰𝑪𝑯𝑨𝑺"])
    # bot.close_chat()
