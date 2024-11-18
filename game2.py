# from IPython.display import display, Image
# from classes.SingletonWindow import SingletonWindow
# from classes.DynamicScreen import DynamicScreen as TelaDinamica
# import tkinter as tk

# janela = SingletonWindow()

# # Inicia a aplicação
# janela.start()


import tkinter as tk
from PIL import Image, ImageTk  # Para carregar e redimensionar as imagens

# Dados do jogo
fases = {
     1: {"descricao": "Ao acordar, você se encontra em uma sala desconhecida...", "item": "chave", "jpg": "C:/projetos python/Escape/assets/image/sala_desconhecida.jpg"},
    2: {"descricao": "O corredor leva a uma caverna escura...", "item": "tocha", "jpg": "C:/projetos python/Escape/assets/image/caverna_escura.jpg"},
    3: {"descricao": "A passagem secreta leva a um jardim encantado...", "item": "chave do portão", "jpg": "C:/projetos python/Escape/assets/image/jardim.jpg"},
    4: {"descricao": "Você chega a uma sala misteriosa com uma mesa e uma carta.", "item": "pista da carta", "jpg": "C:\projetos python\Escape\assets\image\carta.jpg"},
    5: {"descricao": "Você chega ao topo de uma torre e encontra um baú dourado.", "item": "chave do baú", "jpg": "C:/projetos python/Escape/assets/image/jardim.jpg"},
}

# Variáveis do jogo
fase_atual = 1
inventario = []

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
    canvas.itemconfig(titulo_label, text=f"Fase {fase_atual}: {fase['descricao']}", font=("Arial", 24, "bold"))
    atualizar_mensagem("O que você quer fazer?")

def atualizar_mensagem(texto):
    """Atualiza o label de mensagens."""
    canvas.itemconfig(mensagem_label, text=texto)

def examinar_ambiente():
    """Examina o ambiente e coleta o item."""
    global fase_atual
    if fases[fase_atual]["item"] not in inventario:
        inventario.append(fases[fase_atual]["item"])
        atualizar_mensagem(f"Você encontrou {fases[fase_atual]['item']}!")
    else:
        atualizar_mensagem("Não há mais nada para explorar aqui.")

def interagir_objeto():
    """Interage com os objetos no ambiente."""
    global fase_atual
    if fases[fase_atual]["item"] in inventario:
        if fase_atual < len(fases):
            fase_atual += 1
            atualizar_interface()
        else:
            atualizar_mensagem("Parabéns! Você completou o jogo!")
            # Desabilita os botões ao final do jogo
            for btn in botoes:
                btn.config(state="disabled")
    else:
        atualizar_mensagem(f"Você precisa de {fases[fase_atual]['item']} para continuar.")

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

# Lista para armazenar os botões
botoes = []

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

# Inicializa a interface
atualizar_interface()
criar_botoes()

# Inicia o loop principal da interface
root.mainloop()






# # Adiciona a tela dinâmica
# tela_dinamica = TelaDinamica(janela.root, janela)
# janela.add_frame("TelaDinamica", tela_dinamica)

# # Define a tela inicial
# janela.show_frame("TelaDinamica")



# # Caminho para o GIF (Substitua pelo caminho correto do seu GIF no Google Colab)
# gif_1 = "C:/projetos python/Escape/assets/gif/bau.gif"
# # gif_1 = "assets/gif/meu_gif_looping(1).gif"
# gif_2 = "C:/projetos python/Escape/assets/gif/tocha.gif"
# # gif_2 = "assets/gif/toxa.gif"
# gif_url = "https://url/do/seu/gif.gif"

# def mostrar_scenario(fase):
#     """Exibe o cenário atual baseado na fase."""
#     if fase == 1:
#         print("\nAo acordar, você se encontra em uma sala desconhecida, com paredes de pedra fria e um leve cheiro de mofo no ar. Ao seu redor, há apenas um baú fechado e uma porta trancada. Você se levanta, lembrando-se das palavras dos líderes em seu sonho. Qual próxima ação?")
#     elif fase == 2:
#         print("\nO corredor leva a uma caverna escura e úmida.")
#     elif fase == 3:
#         print("\nA passagem secreta leva a um jardim encantado, cheio de flores exóticas e uma fonte cristalina. No centro do jardim, há um portão trancado.")
#     print("\nO que você quer fazer?")
#     print("1 - Vasculhar tudo no ambiente")
#     print("2 - Usar o que eu achei")
#     print("3 - Ver o que tenho no meu inventário")
#     print("4 - Sair do jogo")

# def examinar_ambiente(fase, inventario):
#     """Examina o ambiente e interage com os objetos encontrados."""
#     if fase == 1:
#         if "chave" not in inventario:
#             display(Image(filename=gif_1))  # Exibe o GIF do baú
#             print("\nVocê decide examinar o baú e, para sua surpresa, encontra uma chave dentro dele.")
#             inventario.append("chave")
#         else:
#             print("\nO baú já foi examinado e não tem mais nada.")
#     elif fase == 2:
#         if "tocha" not in inventario:
#             display(Image(filename=gif_2))
#             print("\nAo meio de diversas pedras e insetos, você encontra uma tocha apagada.")
#             inventario.append("tocha")
#         else:
#             print("\nNão há mais nada na caverna.")
#     elif fase == 3:
#         if "chave do portão" not in inventario:
#             display(Image(filename=gif_3))
#             print("\nVocê encontra uma chave do portão escondida na fonte.")
#             inventario.append("chave do portão")
#         else:
#             print("\nNão há mais nada no jardim.")

# def interagir_objeto(fase, inventario):
#     """Interage com objetos no ambiente com base no que foi encontrado no inventário."""
#     if fase == 1:
#         if "chave" in inventario:
#             print("\nVocê usa a chave para abrir a porta e escapar!")
#             print("Ao girar a chave na fechadura, a porta se abre com um rangido, revelando um corredor escuro à sua frente. Você avança com cautela, sentindo a adrenalina correr em suas veias.")
#             return True, 2  # O jogador avança para a próxima fase
#         else:
#             print("\nA porta está trancada. Você precisa de uma chave para abri-la.")
#     elif fase == 2:
#         if "tocha" in inventario:
#             print("\nVocê pega a tocha e a acende, iluminando o caminho à sua frente. A luz revela uma passagem estreita que você decide seguir. A cada passo, o som de gotas de água ecoa pelas paredes da caverna, criando uma atmosfera tensa.")
#             return True, 3  # O jogador avança para a próxima fase
#         else:
#             print("\nEstá muito escuro para ver qualquer coisa. Você precisa de uma tocha.")
#     elif fase == 3:
#         if "chave do portão" in inventario:
#             print("\nCom a chave em mãos, você se aproxima do portão e o destranca, revelando um caminho que leva a um novo mundo cheio de aventuras.")
#             return True, 4  # O jogador completa o jogo
#         else:
#             print("\nO portão está trancado. Você precisa da chave do portão para abri-lo.")
#     return False, fase  # O jogador não avança de fase

# # Exemplo de uso
# fase_atual = 1
# inventario = []

# # Loop principal do jogo
# while fase_atual <= 3:
#     mostrar_scenario(fase_atual)

#     # Obtém a escolha do jogador
#     try:
#         acao = int(input("Escolha uma ação: "))

#         if acao == 1:
#             examinar_ambiente(fase_atual, inventario)
#         elif acao == 2:
#             avancar, nova_fase = interagir_objeto(fase_atual, inventario)
#             if avancar:
#                 fase_atual = nova_fase
#         elif acao == 3:
#             print("\nInventário:", inventario)
#         elif acao == 4:
#             print("\nVocê decidiu sair do jogo. Até logo!")
#             break  # Sai do jogo
#         else:
#             print("\nAção inválida. Tente novamente.")

#     except ValueError as e:
#         print(e)
#         print("\nPor favor, insira um número válido.")

# print("Fim do jogo!")

