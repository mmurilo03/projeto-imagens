import tkinter as Tk
import telas
import psycopg2


janela = telas.App()
fundo = telas.Fundo(janela)
tela = telas.Login(janela)


janela.mainloop()