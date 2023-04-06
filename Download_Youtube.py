import io
from pytube import YouTube
from PIL import ImageTk, Image
import tkinter as tk
import awesometkinter as atk
from tkinter import messagebox
import requests
from pytube.exceptions import RegexMatchError

janela = tk.Tk()
janela.title("Download Video Youtube")
janela.geometry("550x700")
janela.resizable(False, False)
janela.config(bg="#333333")
frame = atk.Frame3d(janela)
frame.grid(row=5, column=2, padx=5, pady=10, sticky='w', columnspan=6)
frame.configure(width=500)
frame_titulo = atk.Frame3d(janela)
frame_titulo.grid(row=2, column=2, padx=5, pady=5, sticky='w', columnspan=6)
frame_titulo.configure(width=500)

#abre a imagem e redimensiona e cria um variavel imagem_topo_tela que será exibida como label no topo da tela
logo_youtube = Image.open("download.png")
logo_youtube.resize((100, 100))
imagem_topo_tela = ImageTk.PhotoImage(logo_youtube)


#Realiza a Busca da Thumbnail e titulo do video que será colocado  na tela assim que for clicado em Download
def buscar_thumbnail():
    url = caminho_text.get()
    # Faz o tratamento de possiveis erros utilizando Try Exception
    try:
        yt = YouTube(url)
        thumb = yt.thumbnail_url
        response = requests.get(thumb)
        img_data = response.content
        img_url = Image.open(io.BytesIO(img_data))
        img_url = img_url.resize((500, 500))
        tumb = ImageTk.PhotoImage(img_url)
        #Pega o titulo do video para fixar na tela para o usário
        titulo = yt.title
        titulo = f'Titulo do Video: {titulo}'
        #Cria a Label e posiciona na tela
        titulo = tk.Label(frame, text=titulo, bg='yellow', fg='black', font=("Arial", 7))
        titulo.grid(row=8, column=0, padx=10, pady=5, sticky='w', columnspan=1)

        #Cria a laber da imagem e possiciona na tela
        imagem = tk.Label(frame, image=tumb, width=500, height=400)
        imagem.grid(row=10, column=0, padx=10, pady=5, sticky='w', columnspan=1)
        #Chama a Função que faz a confirmação com usuário.
        confirmar_download()
        #Trata o erro caso retorno for RegexMatchError , chamando a mensagem na tela de ERRO
    except RegexMatchError as erro:
        messagebox.showerror("ERRO ", "Link digitado é invalido ou está vazio, Tente novamente")

#Função que faz o download do audio do video utilizando o Pytube
#O Audio é salvo no Diretorio Download
def fazer_download_audio():
    url = caminho_text.get()
    yt = YouTube(url)
    local_arquivo = "C:/Downloads/"
    stream = yt.streams.filter(only_audio=True).first()
    stream.download(output_path=local_arquivo, filename_prefix='audio_')
    messagebox.showinfo('Mensagem', 'Download realizado com Sucesso')
    #Depois que o Download é realizado a Tela fecha.
    janela.destroy()


def fazer_download():
    url = caminho_text.get()
    yt = YouTube(url)
    local_arquivo = "C:/Downloads/"
    yt.streams.get_highest_resolution().download(local_arquivo)
    messagebox.showinfo('Mensagem', 'Download realizado com Sucesso')
    janela.destroy()



def confirmar_download():
    msg = "DOWNLOAD EM ANDAMENTO ...(C:/Downloads/)"
    mensagem = tk.Label(frame, text=msg, bg='yellow',fg='black', font=("bold Arial", 10))
    mensagem.grid(row=7, column=0, padx=1, pady=5, sticky='n', columnspan=1)
    retorno = messagebox.askokcancel('Download', 'Confirma o Download do Video?')
    if retorno:

        fazer_download_audio()
    else:
        caminho_text.delete(0,tk.END)





# Cria o label
l_titulo= tk.Label(frame_titulo, image=imagem_topo_tela, width=500, height=50)
l_titulo.grid(row=0, column=2, padx=10, pady=10, sticky='w', columnspan=1)

l_caminho= tk.Label(frame, text="Inserir Link do Video", bg="red" , fg='black',font=("bold Arial", 12))
l_caminho.grid(row=5, column=0, padx=10, pady=2, sticky='w', columnspan=1)
caminho_text = tk.Entry(frame)
caminho_text.grid(row=6, column=0, padx=1, pady=5, sticky='w', columnspan=1)
caminho_text.configure(width=85)
botao = atk.Button3d(frame , text="Fazer Download", command=buscar_thumbnail)
botao.grid(row=7, column=0, padx=10, pady=5, sticky='w', columnspan=1)


janela.mainloop()