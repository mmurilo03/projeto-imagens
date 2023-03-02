import tkinter as Tk
import psycopg2
import os

connect = psycopg2.connect(dbname = "projetoimagens", user = "postgres", password = "1234", host = "localhost")


class App(Tk.Tk):

    def __init__(self, *args, **kwargs):

        Tk.Tk.__init__(self, *args, **kwargs)        

        self.geometry("700x700+100+50")

        
    def switch(self ,new_screen):
        new_screen.pack()
        new_screen.tkraise()


class Fundo(Tk.Canvas):

    def __init__(self,master):

        Tk.Canvas.__init__(self, master, width = 700, height = 700)

        self.master = master

        #Imagem de Fundo
        self.imagem = Tk.PhotoImage(file = "Papel de parede.png")
        self.create_image(350 ,350, image = self.imagem)
        self.place(x = 0, y = 0)


class Login(Tk.Frame):

    def __init__(self,master):

        Tk.Frame.__init__(self, master, bg = "white")
        
        self.master = master
        
        #Nome do usuário
        self.nome = Tk.Label(self, text = "Nome de usuário", font = ("Verdana, 15"), bg = "white")
        self.nome.pack()

        self.nome_entry = Tk.Entry(self, font = ("Verdana, 15"), width = 40)
        self.nome_entry.pack()

        #Senha do usuário
        self.senha = Tk.Label(self, text = "Senha do usuário", font = ("Verdana, 15"), bg = "white")
        self.senha.pack()

        self.senha_entry = Tk.Entry(self, font = ("Verdana, 15"), width = 40)
        self.senha_entry.pack()

        #Botao criar
        self.botao = Tk.Button(self, text = "Criar usuário", font = ("Verdana, 15"), command = self.criar)
        self.botao.pack()

        #Botao entrar
        self.botao = Tk.Button(self, text = "Entrar", font = ("Verdana, 15"), command = self.entrar)
        self.botao.pack()

        #Mostrar Frame
        self.pack()

        


    def criar(self):

        nome_usuario = self.nome_entry.get()
        senha_usuario = self.senha_entry.get()

        if len(nome_usuario) < 1 or len(senha_usuario) < 1 :
            print("O campo de nome e de senha deve ter pelo menos 1 caractere")

        else:
            try:

                cur = connect.cursor()
                cur.execute("SELECT nome, senha FROM usuario WHERE nome = %s and senha = %s;", (nome_usuario, senha_usuario))

                if len(cur.fetchall()) != 0 :
                    print("Perfil com o nome de usuário digitado já está em uso")

                else:
                    cur.execute("INSERT INTO usuario VALUES (%s, %s);", (nome_usuario, senha_usuario))
                    connect.commit()

                    print("Perfil criado com sucesso")

                cur.close()

            except:

                print("erro criar")
                cur.close()

    def entrar(self):

        nome_usuario = self.nome_entry.get()
        senha_usuario = self.senha_entry.get()
        
        try:

            cur = connect.cursor()
            cur.execute("SELECT nome, senha FROM usuario WHERE nome = %s and senha = %s;", (nome_usuario, senha_usuario))

            if len(cur.fetchall()) != 0:
                cur.close()
                self.master.switch(Tela_principal(self.master, nome_usuario))
                self.pack_forget()

            else:
                cur.close()
                print("Perfil não encontrado")

        except:

            print("erro entrar")
            cur.close()

        
class Tela_principal(Tk.Frame):

    def __init__(self,master,nome_usuario):

        Tk.Frame.__init__(self, master, bg = "white")

        self.nome_usuario = nome_usuario
        self.master = master

        #Botao enviar
        self.botao_enviar = Tk.Button(self, text = "Enviar arquivos", font = ("Verdana, 15"), command = self.enviar)
        self.botao_enviar.pack()

        #Botao baixar
        self.botao_baixar = Tk.Button(self, text = "Baixar arquivos", font = ("Verdana, 15"), command = self.baixar)
        self.botao_baixar.pack()

        #Botao excluir
        self.botao_excluir = Tk.Button(self, text = "Excluir arquivos", font = ("Verdana, 15"), command = self.excluir)
        self.botao_excluir.pack()

        #Botao voltar
        self.botao_voltar = Tk.Button(self, text = "Voltar para a tela de login", font = ("Verdana, 15"), command = self.voltar)
        self.botao_voltar.pack()


    def enviar(self):

        self.master.switch(Tela_enviar(self.master, self.nome_usuario))
        self.pack_forget()


    def baixar(self):

        self.master.switch(Tela_baixar(self.master, self.nome_usuario))
        self.pack_forget()

    def excluir(self):

        self.master.switch(Tela_excluir(self.master, self.nome_usuario))
        self.pack_forget()

    def voltar(self):

        self.master.switch(Login(self.master))
        self.pack_forget()


class Tela_enviar(Tk.Frame):

    def __init__(self,master,nome_usuario):

        Tk.Frame.__init__(self, master, bg = "white")

        self.nome_usuario = nome_usuario
        self.master = master

        #Endereço da imagem
        self.endereco = Tk.Label(self, text = "Endereço do arquivo", font = ("Verdana, 15"), bg = "white")
        self.endereco.pack()

        self.endereco_entry = Tk.Entry(self, font = ("Verdana, 15"), width = 40)
        self.endereco_entry.pack()

        #Nome da imagem
        self.nome_imagem = Tk.Label(self, text = "Nome do arquivo que vai ser enviado", font = ("Verdana, 15"), bg = "white")
        self.nome_imagem.pack()

        self.nome_imagem_entry = Tk.Entry(self, font = ("Verdana, 15"), width = 40)
        self.nome_imagem_entry.pack()

        #Botao enviar
        self.botao_enviar = Tk.Button(self, text = "Enviar arquivo", font = ("Verdana, 15"), command = self.enviar)
        self.botao_enviar.pack()

        #Botao voltar
        self.botao_voltar = Tk.Button(self, text = "Voltar", font = ("Verdana, 15"), command = self.voltar)
        self.botao_voltar.pack()


    def enviar(self):

        endereco = self.endereco_entry.get()
        nome_da_imagem = self.nome_imagem_entry.get()

        try:

            cur = connect.cursor()

            cur.execute("SELECT nome, nome_usuario FROM imagem WHERE nome = %s AND nome_usuario = %s;", (nome_da_imagem, self.nome_usuario))

            if len(cur.fetchall()) == 0 :

                try: 

                    arquivo = open(endereco + "\\" + nome_da_imagem, "rb")
                    arquivo2 = arquivo.read()

                    cur.execute("INSERT INTO imagem VALUES (%s, %s);", (nome_da_imagem, self.nome_usuario))
                    connect.commit()

                    cur.execute("SELECT id FROM imagem WHERE nome = %s AND nome_usuario = %s;", (nome_da_imagem, self.nome_usuario))

                    id_imagem = cur.fetchall()[0][0]
                    id_imagem = str(id_imagem)
                    

                    bk_arquivo = open("Imagens\\" + id_imagem + nome_da_imagem, "wb")
                    bk_arquivo.write(arquivo2)
                    cur.close()
                    print("Imagem enviada com sucesso")

                except:
                    cur.close()
                    print("Não existe nenhum arquivo com esse nome no diretório")

            else:
                cur.close()
                print("Já existe uma imagem com o esse nome no seu perfil")

        except:
            
            cur.close()
            print("Erro enviar")

    def voltar(self):

        self.master.switch(Tela_principal(self.master, self.nome_usuario))
        self.pack_forget()




class Tela_baixar(Tk.Frame):

    def __init__(self,master,nome_usuario):

        Tk.Frame.__init__(self, master, bg = "white")

        self.nome_usuario = nome_usuario
        self.master = master

        #Nome da imagem
        self.nome_imagem = Tk.Label(self, text = "Nome do arquivo que vai ser baixado", font = ("Verdana, 15"), bg = "white")
        self.nome_imagem.pack()

        self.nome_imagem_entry = Tk.Entry(self, font = ("Verdana, 15"), width = 40)
        self.nome_imagem_entry.pack()

        #Local de download
        self.endereco = Tk.Label(self, text = "Local de download", font = ("Verdana, 15"), bg = "white")
        self.endereco.pack()

        self.endereco_entry = Tk.Entry(self, font = ("Verdana, 15"), width = 40)
        self.endereco_entry.pack()

        #Botao baixar
        self.botao_baixar = Tk.Button(self, text = "Baixar arquivo", font = ("Verdana, 15"), command = self.baixar)
        self.botao_baixar.pack()

        #Botao voltar
        self.botao_voltar = Tk.Button(self, text = "Voltar", font = ("Verdana, 15"), command = self.voltar)
        self.botao_voltar.pack()


    def baixar(self):

        try:
        
            endereco = self.endereco_entry.get()
            nome_da_imagem = self.nome_imagem_entry.get()

            cur = connect.cursor()
            cur.execute("SELECT nome, nome_usuario, id FROM imagem WHERE nome = %s AND nome_usuario = %s;", (nome_da_imagem, self.nome_usuario))

            id_imagem = cur.fetchall()[0][2]
            id_imagem = str(id_imagem)

            cur.execute("SELECT nome, nome_usuario, id FROM imagem WHERE nome = %s AND nome_usuario = %s;", (nome_da_imagem, self.nome_usuario))

            if len(cur.fetchall()) == 1 :
                arquivo = open("Imagens\\" + id_imagem + nome_da_imagem, "rb")
                arquivo2 = arquivo.read()

                novo_arquivo = open(endereco + "\\" + nome_da_imagem, "wb")
                novo_arquivo.write(arquivo2)

                cur.close()
                print("Imagem baixada com sucesso")

            else:
                cur.close()
                print("A imagem especificada não está vinculada a essa conta ou existe mais de uma imagem com esse nome, seja mais especifico")
                
        except:

            cur.close()
            print("Erro ao baixar a imagem")

    def voltar(self):

        self.master.switch(Tela_principal(self.master, self.nome_usuario))
        self.pack_forget()


class Tela_excluir(Tk.Frame):

    def __init__(self,master,nome_usuario):

        Tk.Frame.__init__(self, master, bg = "white")

        self.nome_usuario = nome_usuario
        self.master = master

        #Nome da imagem
        self.nome_imagem = Tk.Label(self, text = "Nome do arquivo que vai ser excluído", font = ("Verdana, 15"), bg = "white")
        self.nome_imagem.pack()

        self.nome_imagem_entry = Tk.Entry(self, font = ("Verdana, 15"), width = 40)
        self.nome_imagem_entry.pack()

        #Botao excluir
        self.botao_excluir = Tk.Button(self, text = "Excluir arquivo", font = ("Verdana, 15"), command = self.excluir)
        self.botao_excluir.pack()

        #Botao voltar
        self.botao_voltar = Tk.Button(self, text = "Voltar", font = ("Verdana, 15"), command = self.voltar)
        self.botao_voltar.pack()


    def excluir(self):

        try:

            nome_da_imagem = self.nome_imagem_entry.get()

            cur = connect.cursor()
            cur.execute("SELECT nome, nome_usuario, id FROM imagem WHERE nome = %s AND nome_usuario = %s;", (nome_da_imagem, self.nome_usuario))

            if len(cur.fetchall()) == 1 :
                cur.execute("SELECT nome, nome_usuario, id FROM imagem WHERE nome = %s AND nome_usuario = %s;", (nome_da_imagem, self.nome_usuario))

                id_imagem = cur.fetchall()[0][2]
                id_imagem = str(id_imagem)

                cur.execute("DELETE FROM imagem WHERE nome = %s AND id = %s;", (nome_da_imagem, id_imagem))
                connect.commit()
                cur.close()

                os.remove("Imagens\\" + id_imagem + nome_da_imagem)
                print("Imagem excuida com sucesso")

            else:
                cur.close()
                print("Nenhuma imagem com o nome especificado foi encontrada")

        except:
            
            cur.close()
            print("Erro ao excluir imagem")

    def voltar(self):

        self.master.switch(Tela_principal(self.master, self.nome_usuario))
        self.pack_forget()