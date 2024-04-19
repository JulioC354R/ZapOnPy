# ZapOnPy

**Chatbot utilizando bibliotecas como PyAutoGui para automação**

## Descrição:

O ZapOnPy é um chatbot desenvolvido em python e utiliza recursos selenium e outros recursos de automação dentro do Whatsapp web, originalmente foi pensado com objetivo de administrar grupos de RPG de whatsapp. 
Futuramente conforme lido com os problemas no código, acumulo conhecimentos e experiência, pretendo expandir o bot para clientes como pequenas lanchonetes, de forma a facilitar seus pedidos, eu pretendo incrementar nesse bot banco de dados, integração com chatgpt e mais.

Planejo deixar o código de forma open source, para
curiosos como eu e qualquer pessoa interessada em contribuir com meu projeto.

O projeto será dividido em duas etapas, a primeira será a criação do chatbot para o RPG, a segunda será a adaptação, implementação e testes do produto final.

# FAQs

### Onde posso usar o chatbot?

Atualmente estou desenvolvendo para ser compatível com o Windows e também sistemas Linux.

### Ele tem modo Headless?

O modo Headless é um modo que o navegador funciona sem interface gráfica, poupando recursos e sendo mais úteis para uso em servidores, porém devido a problemas a execução usando o modo headless e certas limitações como não poder escrever na mensagem caracteres em UTF-8 e também a demora para escrever mensagens longas, decidi utilizar um modo "FAKE HEADLESS".

### Como funciona esse Fake Headless?
Ao iniciar o bot tem a opção de utilizar o modo Headless ou não, ao dar True como parâmetro para o modo Headless, o navegador vai ser iniciado com interfaçe gráfica, porém no linux ele vai ter interface gráfica virtual e no Windows eu movi a Janela do navegador para uma área inacessível pelo mouse evitando assim atrapalhar o uso do usuário durante a execução do programa, entretanto deve-se lembrar que utilizo o pyperclip para executar o programa de forma mais rápida e eficaz, então é possível que ao mexer na área de transferência como copiar ou colar itens durante a execução do programa possa acarretar em eventos inesperados.

### Funciona na núvem e em servidores?

Sim, mas para o funcionamento é preciso instalar uma biblioteca para simular uma interface gráfica no caso do Linux. 

# Instalação e configuração:

Este projeto foi feito com base no whatsapp web, para o pleno funcionamento dele é preciso de algumas configurações:

## Instalar as bibliotecas Python:
Use esses comandos no terminal estando na pasta do projeto.
```
pip install selenium
pip install pyperclip
pip install opencv-python
pip install pyzbar
pip install qrcode
pip install pygetwindow
pip install pyvirtualdisplay 
```
## Comandos para Linux:
Use esses comandos no terminal estando na pasta do projeto.
```
sudo apt-get install libzbar0
sudo apt-get install xvfb
chmod +x ./driver/chromedriver
```




## Baixar navegador chrome e o webdriver compatíveis: 

Verifique a versão do chrome do seu computador e baixe aqui os webdrivers compatíveis:

[Chrome Driver para versões mais novas](https://googlechromelabs.github.io/chrome-for-testing/#stable)

[Todas as versões](https://chromedriver.chromium.org/downloads)

Para deixar o Chrome mais rápido e sem animações do whatsapp Abra o Google Chrome.
Vá para as configurações do Chrome digitando chrome://settings/ na barra de endereços e pressionando Enter.
Role para baixo e clique em "Avançado".
Na seção "Acessibilidade", ative a opção "Reduzir movimento".






# Funções RPG

## Na primeira fase focado em auxiliar e administrar grupos de RPG de whatsapp planejo implementar as seguintes funções:





## ✅To Do List

## Criando a base:

- [x] Criar métodos para enviar mensagem.
- [x] Criar método para checar novas mensagens.
- [x] Criar métodos para enviar mídia.
- [x] Criar métodos para ler ultima mensagem.
- [x] Criar métodos para enviar mensagem por contato/grupo.
- [x] Criar métodos para detectar de quem recebeu a mensagem.
- [x] Criar sistema de cadastro de novos usuários no RPG (fichas).
- [x] Funções de interação entre ADM e sistema.
- [ ] Criar métodos para enviar enquetes.
- [x] Criar métodos para ler todas as novas mensagens de uma conversa.
- [ ] Criar métodos para ler dado de enquetes.
- [ ] Criação do escopo do projeto.
- [ ] Criar Grupos separados: Ficha, On, Off, Midia, Loja, Campanha, ADMS, Duelos, Avisos.
- [ ] Criar comandos simples de administração de grupos.
- [ ] Estudar e Integrar banaco de dados para armazenar os dados dos usuários.
- [ ] Criar sistema de inventário.
- [ ] Funções de aprovação e reprovação de cenas.
- [ ] Função de contabilizar e armazenar cenas, tendo elas ID para que os usuários possam acessar posteriormente.
- [ ] Função de contabilizar dinheiro, itens dos usuários, quantidade de XP e etc.
- [ ] Criar Loja de itens que alterna diariamente.
- [ ] Criar sistema de mídia.
- [ ] Verificação de atividade dos usuários.
- [ ] Eventos de Multiplicar XP sendo decidido pelos ADMs,
- [ ] Função de Calendário e armazenamento de dados sobre eventos
- [ ] Criar sistema de gacha (contendo itens mais aprimorados com baixa chance de ganho)
- [ ] Integrar ChatGPT
- [ ] Auto usar itens citados nas cenas escritas (será explicito como um comando e será lido pelo sistema)
- [ ] Gerar diárias automáticas pelo chatGPT
- [ ] Criar sistema de duelos (Dar adm na sala aos dois participantes e ao chat)
- [ ] Adicionar sistema de relógio, contar tempo de cena e permitir pausa.
- [ ] Sistema de Níveis e Experiência para Usuários
- [ ] Sistema de Conquistas ou Distinções para Usuários Ativos
- [ ] Sistema de Moderação Automática para Conteúdo Inadequado
- [ ] Melhorar Interface de Usuário (UI) e Experiência de Usuário (UX)
- [ ] Implementar um Sistema de Suporte Automático ao usuário.
- [ ] Sistema de títulos únicos a usuários, desbloqueando após certas condições.
- [ ] Contabilizar batalhas, vitórias, campanhas que participou e etc.
- [ ] Implementar torneio quinzenal.
- [ ] Criar Sistema de Avaliação e Comentários para Cenas.
- [ ] Criar Ferramentas de Análise e Relatórios para Administradores.
- [ ] Desenvolver um Mecanismo Anti-Spam e Anti-Abuso.
- [ ] Adicionar Interações Divertidas ou Jogos Aleatórios.
- [ ]  Implementar Módulo de Aprendizado de Máquina para Personalização
- [ ]  Desenvolver Sistema de Feedback dos Usuários.

# Ideias a serem consideradas:

Utilizar multi instâncias de navegador para assim ter vários bots do whatsapp para atender a uma demanda maior.
talvez criar sistema de sessões (o bot fica na conversa até que o cliente saia ou fique sem responder por 5 min) isso pode ser um pouco complicado em horários de pico mas vale a pena tentar
Criar uma API para fazer a comunicação entre o banco de dados e o chatbot



</details>
