# ZapOnPy

**Chatbot utilizando bibliotecas como PyAutoGui para automação**

## Descrição:

O ZapOnPy é um chatbot desenvolvido em python e utiliza recursos selenium e outros recursos de automação dentro do Whatsapp web, originalmente foi pensado com objetivo de administrar grupos de RPG de whatsapp. 
Futuramente conforme lido com os problemas no código, acumulo conhecimentos e experiência, pretendo expandir o bot para clientes como pequenas lanchonetes, de forma a facilitar seus pedidos, eu pretendo incrementar nesse bot banco de dados, integração com chatgpt e mais.

Planejo deixar o código de forma open source, para
curiosos como eu e qualquer pessoa interessada em contribuir com meu projeto.

O projeto será dividido em duas etapas, a primeira será a criação do chatbot para o RPG, a segunda será a adaptação, implementação e testes do produto final.

# Instalação e configuração:

### Este projeto foi feito com base no whatsapp web, para o pleno funcionamento dele é preciso de algumas configurações:

- instalar as bibliotecas:
pip install selenium
pip install pyperclip
pip install opencv-python
pip install pyzbar
pip install qrcode
pip install pygetwindow
pip install pyvirtualdisplay 



- Baixar navegador chrome e o webdriver compatíveis, verifique a versão do seu computador e baixe aqui os webdrivers compatíveis:
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
- [x] Criar métodos para enviar mensagem por número.
- [x] Criar métodos para enviar mensagem por contato/grupo.
- [x] Criar métodos para detectar de quem recebeu a mensagem.
- [x] Criar sistema de cadastro de novos usuários no RPG (fichas).
- [x] Funções de interação entre ADM e sistema.
- [ ] Criar métodos para enviar enquetes.
- [ ] Criar métodos para ler todas as novas mensagens de uma conversa.
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


</details>
