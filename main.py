import mysql.connector
from mysql.connector import Error
from datetime import datetime
from kivy.app import App
from kivy.properties import StringProperty, ObjectProperty
from kivy.config import Config

HOST = "br544.hostgator.com.br"
DBA = "shile329_controlstock"
USR = "shile329_admin"
PASS = "@Cometa120258"

"""
con = mysql.connector.connect(host=HOST, database=DBA, user=USR, password=PASS)

if con.is_connected():
    db_info = con.get_server_info()
    print("Conecato! :"+db_info)
    cursor = con.cursor()
    cursor.execute("select database();")
    linha = cursor.fetchone()
    print("BD:", linha)
else:
    print("Falha ao conectar ao BD")
"""


largura = 1080/3
altura = 1920/3

Config.set('graphics', 'resizable', True)
Config.set('graphics', 'width', str(int(largura)))
Config.set('graphics', 'height', str(int(altura)))


# FUNCAO APRA FORMATACAO DO PESO
def format_num(number):
    """Função formatar texto 1.000.000"""
    return "{:,}".format(number)


class Shi(App):
    # VAR PARA TRASNFERIR PARA KIVY
    digs_inp = StringProperty('0g')
    # VAR
    soma = ''
    mask = ''
    categoria = 'Shimeji Branco'

    # ADICIONA NUMEROS A TELA
    def add_nums(self, va1):

        # TRAVA QUANTIDADE DE DIGITOS
        if len(self.soma) < 6:
            # ADICIONA N° EM ORDEM DE DIGITACAO
            self.soma = self.soma + str(va1)
            # FORMATA TEXTO
            self.mask = format_num(int(self.soma))
            # IMPRIMI TEXTO NA TELA
            self.digs_inp = str(self.mask + 'g')
        else:
            pass

    # APAGAR PESO DA TELA
    def apagar_nums(self):
        # APAGA VARIAVEL SOMA
        self.soma = self.soma[:-1]

        # IMPRIMI TEXTO NA TELA
        if self.soma == '':
            self.digs_inp = str('0g')
        else:
            # FORMATA TEXTO
            self.mask = format_num(int(self.soma))
            self.digs_inp = str(self.mask+'g')

    # SELECIONA CATEGORIAS
    def select_categoria(self, res):

        self.root.ids.spc.ids.menu_branco.active = False
        self.root.ids.spc.ids.menu_porto.active = False
        self.root.ids.spc.ids.menu_shimofury.active = False
        self.root.ids.spc.ids.menu_salmao.active = False

        if res == 'branco':
            self.root.ids.spc.ids.menu_branco.active = True
            self.categoria = 'Shimeji Branco'
        elif res == 'porto':
            self.root.ids.spc.ids.menu_porto.active = True
            self.categoria = 'Porto Belo'
        elif res == 'shimofury':
            self.root.ids.spc.ids.menu_shimofury.active = True
            self.categoria = 'Shimofuri'
        elif res == 'salmao':
            self.root.ids.spc.ids.menu_salmao.active = True
            self.categoria = 'Shimneji Salmão'

    # TROCA TELA E ATUALIZADA BARRA BRANCO
    def chang_screen(self, va1):
        # TROCA TELA
        self.root.ids.ScreenControl.current = va1
        # APAGAR BARRA INFERIOR DOS BOTOES
        self.root.ids.menu_id.ids.bt_pesagem.active = False
        self.root.ids.menu_id.ids.bt_historico.active = False

        if va1 == "t1":
            # SETA BARRA NO BOTAO SELECIONADO
            self.root.ids.menu_id.ids.bt_pesagem.active = True
        else:
            self.root.ids.menu_id.ids.bt_historico.active = True
            # AO TROCAR A TELA ZERA LCD
            self.digs_inp = "0g"
            self.soma = ''
            self.mask = ''
            self.mostar_historico()

    def envia_peso(self):
        data_atual = datetime.now()
        data_atual = data_atual.strftime('%d/%m/%Y %H:%M')
        # print(self.categoria, self.digs_inp, data_atual)
        try:
            _con = mysql.connector.connect(host=HOST, database=DBA, user=USR, password=PASS)
            _inserir = "INSERT INTO `Coletas` (`id`, `data`, `peso`, `tipo`) VALUES (NULL, '"+data_atual+"', '"+self.digs_inp+"', '"+self.categoria+"');"
            _cursor = _con.cursor()
            _cursor.execute(_inserir)
            _con.commit()
            print(_cursor.rowcount, " registros inseridos na tabela!")
            _cursor.close()
        except Error as erro:
            print("Falha:{}".format(erro))
        finally:
            if _con.is_connected():
                _cursor.close()
                print("Conexão encerrada!")

    def mostar_historico(self):
        # self.root.ids.id_box.add_widget(Histo)
        print("Carregar BD")



# EXECUTA PROGRAMA
if __name__ == '__main__':
    Shi().run()
