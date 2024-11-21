import tkinter as tk
from PIL import Image, ImageTk  # Para carregar e redimensionar as imagens
import time

# Dados do jogo
fases = {
    1: {"titulo": "A Chave do Começo", "descricao": "Ao acordar, você se encontra em uma sala desconhecida...", "item": "chave", "jpg": "assets\image\sala_desconhecida.jpg"},
    2: {"titulo": "O Escudo da Proteção", "descricao": "O corredor leva a uma caverna escura...", "item": "tocha", "jpg": "assets\image\caverna_escura.jpg"},
    3: {"titulo": "O Coração do Vento", "descricao": "A passagem secreta leva a um jardim encantado...", "item": "chave do portão", "jpg": "assets\image\jardim.jpg"},
    4: {"titulo": "A Corrente do Tempo", "descricao": "Você chega a uma sala misteriosa com uma mesa e uma carta.", "item": "pista da carta", "jpg": "assets\image\carta.jpg"},
    5: {"titulo": "O Teste Final", "descricao": "Você chega ao topo de uma torre e encontra um baú dourado.", "item": "chave do baú", "jpg": "assets\image\ultima_fase.jpg"},
}

# Mensagens específicas para cada item
mensagens_itens = {
    "chave": "Você usou a chave para abrir a porta.",
    "tocha": "Você usou a tocha para iluminar a caverna.",
    "chave do portão": "Você usou a chave para abrir o portão.",
    "pista da carta": "Você leu a pista da carta que te levou para algum lugar.",
    "chave do baú": "Você abriu o baú e conseguiu e conseguiu escapar!"
}

# Adicionando os enigmas
enigmas = {
    1: {"pergunta": "O que é sempre à frente, mas nunca pode ser visto?", "resposta": "futuro"},
    2: {"pergunta": "Quanto mais você tira, maior fica. O que é?", "resposta": "buraco"},
    3: {"pergunta": "O que tem chaves, mas não abre portas?", "resposta": "piano"},
    4: {"pergunta": "O que quanto mais você tem, menos você vê?", "resposta": "escuro"},
    5: {"pergunta": "O que pode encher uma sala, mas não ocupa espaço?", "resposta": "luz"},
    6: {"pergunta": "O que sempre chega, mas nunca chega?", "resposta": "amanhã"},
    7: {"pergunta": "O que é leve como uma pluma, mas até o homem mais forte não consegue segurar?", "resposta": "respiração"},
    8: {"pergunta": "O que pode ser quebrado, mas nunca pode ser tocado?", "resposta": "promessa"},
    9: {"pergunta": "O que corre, mas nunca anda?", "resposta": "agua"},
    10: {"pergunta": "O que é maior que Deus, mais maligno que o diabo, os pobres têm e os ricos precisam?", "resposta": "nada"},
}

# Variáveis do jogo para lidar com os enigmas
enigma_resolvido = []  # Lista para armazenar os enigmas resolvidos


# Variáveis do jogo
fase_atual = 1
inventario = []
botao_confirmar = None  # Armazena o botão de confirmação
temporizador_ativo = True
# Lista para armazenar os botões
botoes = []

# Função do temporizador
def iniciar_temporizador():
    """Inicia o temporizador de 4 minutos e exibe a contagem regressiva."""
    global tempo_restante
    tempo_restante = 4 * 60  # 4 minutos em segundos
    atualizar_temporizador()

def atualizar_temporizador():
    """Atualiza o tempo exibido no canto inferior direito."""
    global tempo_restante, temporizador_ativo
    if not temporizador_ativo:  # Interrompe o temporizador se desativado
        return

    minutos = tempo_restante // 60
    segundos = tempo_restante % 60
    tempo_texto = f"{minutos:02}:{segundos:02}"

    # Atualiza o texto do temporizador no Canvas
    canvas.itemconfig(tempo_label, text=tempo_texto)

    # Se o tempo acabar, exibe a tela preta
    if tempo_restante > 0:
        tempo_restante -= 1
        root.after(1000, atualizar_temporizador)  # Atualiza a cada segundo
    else:
        tela_final()

def tela_final():
    """Exibe a tela preta com a mensagem final quando o tempo acabar e remove todos os elementos da tela."""
    # Apaga todos os elementos da tela (botões, inputs, labels, etc.)
    canvas.delete('all')
    
    # Cria a tela preta com a mensagem final
    canvas.create_rectangle(0, 0, 1200, 700, fill="black", outline="black")
    canvas.create_text(600, 350, text="O tempo acabou! Você perdeu!", font=("Arial", 36, "bold"), fill="white")

# Funções do jogo
def atualizar_interface():
    """Atualiza a interface com os dados da fase atual."""
    global fase_atual
    fase = fases[fase_atual]

    # Atualiza a imagem de fundo
    img = Image.open(fase["jpg"]).resize((1200, 700))  # Ajusta a imagem ao tamanho da tela
    img_tk = ImageTk.PhotoImage(img)
    canvas.itemconfig(bg_img, image=img_tk)
    canvas.image = img_tk

    # Atualiza o título e descrição da fase
    texto_titulo = f"Fase {fase_atual}: {fase['titulo']}"
    texto_descricao = fase["descricao"]
    canvas.itemconfig(
        titulo_label, 
        text=f"{texto_titulo}\n{texto_descricao}", 
        font=("Arial", 24, "bold"),
        justify="center"  # Centraliza o texto no canvas
    )
    atualizar_mensagem("O que você quer fazer?")


def atualizar_mensagem(texto):
    """Atualiza o label de mensagens com novos estilos."""
    # Altera o estilo do texto, cor e alinhamento
    font = ("Arial", 20, "normal")  # Usando fonte Arial, tamanho 18, com o estilo passado (normal, bold, etc.)
    canvas.itemconfig(
        mensagem_label, 
        text=texto,
        font=font,
        fill="#FFFF00",  # A cor será passada como argumento (padrão é amarelo)
        justify="center",  # Alinhamento centralizado
    )

def examinar_ambiente():
    """Examina o ambiente e coleta o item."""
    global fase_atual
    if fases[fase_atual]["item"] not in inventario:
        inventario.append(fases[fase_atual]["item"])
        atualizar_mensagem(f"Você encontrou {fases[fase_atual]['item']}!")
    else:
        atualizar_mensagem("Não há mais nada para explorar aqui.")

# Função para gerenciar o estado dos botões
def gerenciar_estado_botoes(habilitar=True):
    """Habilita ou desabilita os botões de ação."""
    estado = "normal" if habilitar else "disabled"
    for btn in botoes:
        btn.config(state=estado)

# Função para criar o botão de confirmação
def botao_proxima_fase():
    """Cria um botão para confirmar a ida para a próxima fase."""
    btn_confirmar = tk.Button(
        root,
        text="Confirmar",
        font=("Arial", 12, "bold"),
        bg="#4CAF50",  # Verde claro
        fg="white",    # Texto branco
        activebackground="#45A049",  # Verde escuro
        relief="flat",  # Sem borda
        bd=0,           # Remove as bordas pretas
        cursor="hand2",  # Cursor tipo "mão"
        command=avancar_fase
    )
    
    # Posições o botão logo abaixo da mensagem (mensagem_label)
    canvas.create_window(600, 650, window=btn_confirmar)  # Ajuste a posição de acordo com a altura dos outros elementos
    return btn_confirmar

# Modificar a função avançar_fase para garantir que o fluxo continue corretamente
def avancar_fase():
    """Avança para a próxima fase, após resolver um enigma."""
    global fase_atual, botao_confirmar
    if fase_atual < len(fases):
        fase_atual += 1
        atualizar_interface()
        criar_botoes()
    else:
        # Fim do jogo - completou todas as fases
        atualizar_mensagem("Parabéns! Você completou o jogo!")
        
        # Desabilitar todos os botões ao completar o jogo
        gerenciar_estado_botoes(habilitar=False)
        
        # Parar o temporizador
        global temporizador_ativo
        temporizador_ativo = False
        
        # Remover os botões principais ao finalizar
        for btn in botoes:
            btn.destroy()  # Remove cada botão principal da tela
        botoes.clear()  # Limpa a lista de botões

    if botao_confirmar:
        botao_confirmar.destroy()  # Remove o botão após uso
        botao_confirmar = None

    # Reativa os botões principais apenas se ainda houver fases
    if fase_atual <= len(fases):
        gerenciar_estado_botoes(habilitar=True)


# Modificar a função interagir_objeto
def interagir_objeto():
    """Interage com os objetos no ambiente e exibe o enigma se necessário."""
    global fase_atual, botao_confirmar, temporizador_ativo
    item_necessario = fases[fase_atual]["item"]

    if item_necessario in inventario:
        if fase_atual not in enigma_resolvido:
            # Exibir o enigma se não foi resolvido
            exibir_enigma(fase_atual)
        else:
            # Caso o enigma já tenha sido resolvido, continua o fluxo
            mensagem = mensagens_itens.get(item_necessario, "Você usou um item.")
            if fase_atual == len(fases):  # Última fase
                atualizar_mensagem(f"{mensagem} Parabéns! Você completou o jogo!")
                temporizador_ativo = False  # Pausa o temporizador
                gerenciar_estado_botoes(habilitar=False)  # Desabilita os botões
            else:
                if not botao_confirmar:  # Evita múltiplos botões de confirmação
                    atualizar_mensagem(f"{mensagem} Pronto para avançar?")
                    botao_confirmar = botao_proxima_fase()
                    gerenciar_estado_botoes(habilitar=False)  # Desabilita os botões principais
    else:
        atualizar_mensagem(f"Você precisa de {item_necessario} para continuar.")

# Função para exibir o enigma
def exibir_enigma(fase_atual):
    """Exibe o enigma e o campo de resposta."""
    enigma = enigmas[fase_atual]
    
    # Remove os botões principais
    gerenciar_estado_botoes(habilitar=False)
    
    # Exibe a pergunta
    # Exibe a pergunta com cor e fonte diferenciada
    pergunta = canvas.create_text(600, 250, text=enigma["pergunta"], font=("Arial", 22, "bold"), fill="#FFD700")  # Usando um dourado para o enigma
    
    # Campo de resposta
    resposta_input = tk.Entry(root, font=("Arial", 14))
    resposta_input_window = canvas.create_window(600, 300, window=resposta_input)

    # Função para verificar a resposta
    def verificar_resposta():
        resposta = resposta_input.get().lower()
        if resposta == enigma["resposta"]:
            enigma_resolvido.append(fase_atual)  # Marca o enigma como resolvido
            atualizar_mensagem(f"Você acertou! {mensagens_itens[fases[fase_atual]['item']]}")
            
            # Remove os elementos do enigma
            canvas.delete(pergunta)
            canvas.delete(resposta_input_window)
            botao_verificar.destroy()

            # Exibe o botão de próxima fase
            botao_confirmar = botao_proxima_fase()

        else:
            # Penaliza 10 segundos no temporizador sem acelerar a contagem
            global tempo_restante
            tempo_restante = max(0, tempo_restante - 10)  # Reduz 10 segundos diretamente

            # Atualiza o temporizador sem acelerar
            atualizar_temporizador()

            # Não remove o campo de entrada e deixa o jogador tentar novamente
            atualizar_mensagem("Resposta errada! Tente novamente.")

    # Botão para verificar a resposta
    botao_verificar = tk.Button(
        root,
        text="Verificar Resposta",
        font=("Arial", 12, "bold"),
        bg="#4CAF50",
        fg="white",
        activebackground="#45A049",
        relief="flat",
        bd=0,
        cursor="hand2",
        command=verificar_resposta
    )
    botao_verificar_window = canvas.create_window(600, 350, window=botao_verificar)


def mostrar_inventario():
    """Mostra os itens no inventário."""
    if inventario:
        atualizar_mensagem(f"Inventário: {', '.join(inventario)}")
    else:
        atualizar_mensagem("Inventário vazio.")

def sair_jogo():
    """Encerra o jogo."""
    root.quit()

# Interface gráfica
root = tk.Tk()
root.title("Escape")
root.geometry("1200x700")  # Ajusta o tamanho da janela

# Canvas principal para sobreposição
canvas = tk.Canvas(root, width=1200, height=700)
canvas.pack(fill="both", expand=True)

# Fundo da imagem
bg_img = canvas.create_image(0, 0, anchor=tk.NW)

# Título da fase
titulo_label = canvas.create_text(600, 50, text="", font=("Arial", 24, "bold"), fill="white")

# Mensagens dinâmicas com maior largura e centralizadas em relação aos botões
mensagem_label = canvas.create_text(
    600, 600,  # Centralizado horizontalmente e próximo aos botões
    text="", 
    font=("Arial", 16),  # Fonte maior para destaque
    fill="yellow", 
    width=800,  # Mais largura para caber mais texto
    justify="center"
)


# Exibir o tempo no canto inferior direito
tempo_label = canvas.create_text(1100, 650, text="04:00", font=("Arial", 22), fill="white")

# Função para criar e posicionar botões diretamente no Canvas
def criar_botoes():
    estilos = {
        "font": ("Arial", 12, "bold"),
        "bg": "#4CAF50",  # Verde claro
        "fg": "white",    # Texto branco
        "activebackground": "#45A049",  # Verde escuro
        "relief": "flat",  # Sem borda
        "bd": 0,           # Remove as bordas pretas
        "cursor": "hand2",  # Cursor tipo "mão"
        "width": 12,       # Botões mais compactos
        "height": 1
    }

    # Botões mais próximos uns dos outros
    btn_examinar = tk.Button(root, text="Examinar", command=examinar_ambiente, **estilos)
    btn_interagir = tk.Button(root, text="Usar Item", command=interagir_objeto, **estilos)
    btn_inventario = tk.Button(root, text="Inventário", command=mostrar_inventario, **estilos)
    btn_sair = tk.Button(root, text="Sair", command=sair_jogo, **estilos)

    botoes.extend([btn_examinar, btn_interagir, btn_inventario, btn_sair])

    # Posiciona os botões centralizados e compactados
    canvas.create_window(500, 650, window=btn_examinar)
    canvas.create_window(600, 650, window=btn_interagir)
    canvas.create_window(700, 650, window=btn_inventario)
    canvas.create_window(800, 650, window=btn_sair)

# Função para iniciar o jogo
def iniciar_jogo():
    atualizar_interface()
    criar_botoes()
    iniciar_temporizador()  # Inicia o temporizador ao começar o jogo

iniciar_jogo()

# Inicia o loop principal da interface
root.mainloop()