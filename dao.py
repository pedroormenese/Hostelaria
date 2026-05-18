# Configuração Banco de Dados

import mysql.connector
from mysql.connector import errorcode #Para importar erros específicos
from mysql.connector import Error #Para importar erros em geral

class Database:
    config = {
        'host': 'localhost',
        'database':'hotelaria',
        'user':'root',
    }


    def __init__(self):
        self.cnx = None


    # ================================================ Se conectar com o banco de dados
    def connect(self):
        try:
            self.cnx = mysql.connector.connect(**self.config) #Representa a conexão com o servidor do banco de dados
        except Error as e:
            if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Algo está errado com seu nome de usuário ou senha.")
            elif e.errno == errorcode.ER_BAD_DB_ERROR:
                print("Seu DataBase não existe ou não foi encontrado.")
            else:
                print(f"Erro: {e}")


    # ================================================ Se desconectar do banco de dados
    def disconnect(self):
        try:
            if self.cnx.is_connected():
                self.cnx.close()
                self.cnx = None

        except Error as e:
            return(e)
        

    # ================================================ Executar Query (Comando)
    def executeQuery(self, query, params=None): #Use apenas para executar uma ação no banco de dados, como criar um cliente, uma reserva, ou atualizar algo. Não use para pegar informações do banco de dados, use os métodos fetchAll ou fetchOne para isso.
        try:

            cursor = self.cnx.cursor() #Criando a instância de um cursor
            cursor.execute(query, params or ()) #Executa a ação com ou sem parâmetros
            self.cnx.commit() #Salva permanentemente a ação no banco de dados

            return cursor.lastrowid #Retorna o ID da última ação
            
        except Error as e:
            if self.cnx.is_connected:
                self.cnx.rollback() #Voltar para a "versão anterior" do banco antes da ação
            print(f"Não foi possível executar a ação.\nErro: {e}")

            raise #Interrompe completamente o fluxo do código e sobe a mensagem de erro

        finally:
            if cursor: #Se o cursor existir
                cursor.close()


    # ================================================ Retornar todas as linhas de uma consulta
    def fetchAll(self, query, params=None): #Use quando você quer pegar várias informações do banco de dados, como uma lista de clientes ou reservas
        try:

            cursor = self.cnx.cursor(dictionary=True) 
            cursor.fetchall(query, params or ())
            self.cnx.commit() 

            return cursor
            
        except Error as e:
            if self.cnx.is_connected:
                self.cnx.rollback()
            print(f"Não foi possível executar a ação.\nErro: {e}")

            raise 

        finally:
            if cursor: 
                cursor.close()


    # ================================================ Retornar apenas uma linha de uma consulta
    def fetchOne(self, query, params=None): #Use quando você quer pegar apenas uma informação do banco de dados, como um cliente específico ou uma reserva específica
        try:

            if self.cnx.is_connected:
                cursor = self.cnx.cursor(dictionary=True) 
                cursor.execute(query, params or ()) 
                self.cnx.commit() 

                return cursor
            
        except Error as e:
            if self.cnx.is_connected:
                self.cnx.rollback() 
            print(f"Não foi possível executar a ação.\nErro: {e}")

            raise 

        finally:
            if cursor: 
                cursor.close()