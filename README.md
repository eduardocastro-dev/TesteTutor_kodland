# Roguelike Adventure

Um jogo de ação do gênero Roguelike desenvolvido em Python com a biblioteca **Pygame Zero**. O jogador controla um herói que deve sobreviver a ondas de inimigos em um mundo expansivo, utilizando ataques, poções e um sistema de bloqueio para se defender.

## Principais Funcionalidades

*   **Menu Principal Interativo**: Um menu completo com partículas animadas, botões para iniciar o jogo, controlar áudio (música e sons) e sair.
*   **Mundo Expansivo**: O mapa do jogo é 3 vezes maior que a tela, com um sistema de câmera que segue o jogador.
*   **Sistema de Combate**:
    *   **Ataque**: O jogador pode atacar com sua espada para causar dano aos inimigos. A área de ataque é visualizada durante a animação.
    *   **Bloqueio**: Segurar a tecla `Shift` reduz o dano recebido.
    *   **Poções**: Use poções para restaurar a vida.
*   **Inimigos com IA**: Os zumbis detectam o jogador à distância, o perseguem e atacam quando estão próximos.
*   **Animações de Sprite**: Animações fluidas para o herói e inimigos em todos os estados (parado, andando, atacando e morrendo).
*   **HUD (Heads-Up Display)**: Interface que exibe a vida, o número de poções e a contagem de abates.
*   **Áudio Imersivo**: Música de fundo para o menu e para o jogo, com efeitos sonoros para ataques, poções e game over.
*   **Gerenciamento de Estado**: O jogo transita suavemente entre o menu, a jogatina e a tela de "Game Over".

## Como Executar o Projeto

### Pré-requisitos
*   Python 3.6 ou superior

### Instalação
1.  Clone este repositório para a sua máquina local.

2.  É altamente recomendado criar e ativar um ambiente virtual.
    ```bash
    # Criar ambiente virtual
    python -m venv .venv

    # Ativar no Windows
    .\.venv\Scripts\activate

    # Ativar no macOS/Linux
    source .venv/bin/activate
    ```

3.  Instale a única dependência necessária, o `pgzero`.
    ```bash
    pip install pgzero
    ```

4.  Execute o jogo.
    ```bash
    pgzrun main.py
    ```

## Controles

*   **Movimentação**: `W, A, S, D` ou `Setas Direcionais`
*   **Ataque**: `Barra de Espaço`
*   **Bloqueio**: `Shift Esquerdo`
*   **Usar Poção**: `E`
*   **Navegar no Menu**: `Mouse`
*   **Voltar ao Menu / Pausar**: `ESC` (durante o jogo ou na tela de game over)
*   **Reiniciar Jogo**: `R` (na tela de game over)


## Atendimento aos Requisitos do Teste

Este projeto foi desenvolvido seguindo estritamente todos os requisitos solicitados:

-   `[x]` **Bibliotecas Restritas**: Utiliza apenas `pgzero`, `math` e `random`. A classe `Rect` é importada de `pygame` conforme a exceção permitida.
-   `[x]` **Gênero do Jogo**: O projeto é um **Roguelike** com visão de cima e movimento livre.
-   `[x]` **Menu Principal**: Possui um menu principal com botões clicáveis para "Começar o jogo", "Música e sons ligados/desligados" e "Saída".
-   `[x]` **Música e Sons**: Inclui música de fundo e efeitos sonoros para ações no jogo.
-
-   `[x]` **Inimigos Múltiplos**: Existem vários inimigos (zumbis) que são perigosos para o herói.
-   `[x]` **Movimento dos Inimigos**: Os inimigos se movem de forma autônoma, perseguindo o jogador.
-   `[x]` **Classes Customizadas**: O movimento e a animação são implementados através das classes `Entity`, `Player` e `Enemy`.
-   `[x]` **Animação de Sprite**: O herói e os inimigos possuem animações de sprite (conjunto de imagens em ciclo) para os estados "parado" (`idle`) e "andando" (`walk`), além de "ataque" e "morte".
-   `[x]` **Código Limpo**: Variáveis, funções e classes utilizam nomes em inglês e o código busca seguir as convenções do PEP8.
-   `[x]` **Lógica do Jogo e Ausência de Bugs**: O jogo possui uma mecânica funcional e coesa, e os bugs conhecidos foram corrigidos.
-   `[x]` **Código Único**: O projeto foi escrito de forma independente para esta finalidade.

---
**Autor**: [Eduardo Castro]
