# Queries Banco de Dados

from dao import *


'''
|===================================================|
|                    |HOSPEDE|                      |
|===================================================|
'''

class Hospede:

    def __init__(self):
        self.db = Database()
        self.cnx = None

    
    # ================================================ Adicionar Hóspede
    def addHospede(self, nome, email, telefone, cpf):
        if not nome or len(nome) < 3:
            raise ValueError("Erro. Nome deve ter ao menos 3 caracteres.")
        
        if not cpf or len(cpf) != 11 or not cpf.isdigit():
            raise ValueError("CPF inválido.")
        
        query = f'''
                INSERT INTO hospedes (nome, email, telefone, cpf) VALUES 
                    ('{nome}', '{email}', '{telefone}', '{cpf}')
                '''
        
        self.db.connect() #Se conecta ao banco de dados através da função Connect no arquivo dao.py
        self.db.executeQuery(query) #Executa a ação através da função executeQuery no arquivo dao.py
        self.db.disconnect()

    
    # ================================================ Remover Hóspede
    def delHospede(self, id):
        query = f'''
                DELETE FROM Hospedes 
                WHERE
                    id = {id}
                '''
        self.db.connect()
        self.db.executeQuery(query)
        self.db.disconnect()
        

    # ================================================ Editar Hóspede
    def updHospede(self, nome, email, telefone, cpf):
        query = f'''
                UPDATE Hospedes
                SET
                    nome = '{nome}',
                    email = '{email}',
                    telefone = '{telefone}',
                    cpf = '{cpf}'
                WHERE
                    id = {id}
                '''
        self.db.connect()
        self.db.executeQuery(query)
        self.db.disconnect()

    
    # ================================================ Listar Hóspedes
    def listHospede(self):
        query = '''
                SELECT * FROM Hospedes
                '''

        self.db.connect()
        values = self.db.fetchAll(query)
        self.db.disconnect()

        return values
    

    # ================================================ Buscar Hóspede por ID
    def getHospedeById(self, id):
        query =f'''
                SELECT * FROM Hospedes
                WHERE
                    id = {id}
                '''
        self.db.connect()
        result = self.db.fetchOne(query)
        self.db.disconnect()

        return result
    

'''
|===================================================|
|                    |QUARTO|                       |
|===================================================|
'''

class Quarto:
    def __init__(self):
        self.db = Database()

    
    # ================================================ Adicionar Quarto
    def addQuarto(self, numero, tipo, valor_diaria, status):
        if not numero:
            raise ValueError("Erro. Número do quarto é obrigatório.")
        
        if not tipo:
            raise ValueError("Erro. Tipo do quarto é obrigatório.")
        
        if not valor_diaria:
            raise ValueError("Erro. Valor da diária é obrigatório.")
        
        if not status:
            raise ValueError("Erro. Status do quarto é obrigatório.")

        query = f'''
                INSERT INTO quartos (numero, tipo, valor_diaria, status) 
                VALUES 
                    (
                        '{numero}', 
                        '{tipo}', 
                        '{valor_diaria}', 
                        '{status}'
                    )
                '''
        
        self.db.connect()
        result = self.db.executeQuery(query) 
        self.db.disconnect()

        return result

    
    # ================================================ Remover Quarto
    def delQuarto(self, id):
        query = f'''
                DELETE FROM Quartos 
                WHERE
                    id = {id}
                '''
        self.db.connect()
        self.db.executeQuery(query)
        self.db.disconnect()
        

    # ================================================ Editar Quarto
    def updQuarto(self, id, numero, tipo, valor_diaria, status):
        query = f'''
                UPDATE Quartos
                SET
                    nome = '{numero}',
                    email = '{tipo}',
                    telefone = '{valor_diaria}',
                    cpf = '{status}'
                WHERE
                    id = {id}
                '''
        self.db.connect()
        result = self.db.executeQuery(query)
        self.db.disconnect()

        return result
    
    # ================================================ Listar Quartos
    def listQuartos(self):
        query = f'''
                SELECT * FROM Quartos
                '''
        self.db.connect()
        result = self.db.fetchAll(query)
        self.db.disconnect()

        return result
    

    # ================================================ Buscar Quarto por ID
    def getQuartoById(self, id):
        query =f'''
                SELECT * FROM Quartos
                WHERE
                    id = {id}
                '''
        self.db.connect()
        result = self.db.fetchOne(query)
        self.db.disconnect()

        return result
    

'''
|===================================================|
|                    |RESERVA|                      |
|===================================================|
'''

class Reserva:
    def __init__(self):
        self.db = Database()


    # ================================================ Adicionar Reserva
    def addReserva(self, hospedeId, quartoId, data_Entrada, data_Saida):
        query = f'''
                INSERT INTO Reservas (hospede_id, quarto_id, data_entrada, data_saida)
                VALUES
                    (
                    '{hospedeId}',
                    '{quartoId}',
                    '{data_Entrada}',
                    '{data_Saida}'
                    )
                '''
        
        hospedeTreatment = f'''
                            SELECT * FROM Hospedes
                            WHERE
                                id = '{hospedeId}'
                            '''
        
        quartoTreatment = f'''
                        SELECT * FROM Quartos
                        WHERE
                            id = '{quartoId}'
                        '''
        try:
            self.db.connect()

            if data_Entrada >= data_Saida:
                raise ValueError("A data de saída deve ser maior que a de entrada")

            treatments = [hospedeTreatment, quartoTreatment]
            auth = True
            for treatment in treatments:
                errorTreatment = self.db.fetchOne(treatment)
                if errorTreatment == None:
                    auth = False # id do quarto ou hospede nao existe
            
            if auth == True:
                result = self.db.executeQuery(query)
            else:
                raise ValueError("Não foi possível criar a reserva. Hóspede ou Quarto não existem ou estão indisponíveis no momento.")
            
            return result
        
        finally:
            self.db.disconnect()

    
    # ================================================ Remover Reserva
    def delReserva(self, id):
        query = f'''
                DELETE FROM Reservas
                WHERE
                    id = {id}
                '''
        
        reservaTreatment = f'''
                            SELECT * FROM Reservas
                            WHERE
                                id = {id}
                            '''
        self.db.connect()

        treatment = self.db.fetchOne(reservaTreatment)
        if treatment:
            result = self.db.executeQuery(query)
        else:
            raise ValueError("A reserva não foi encontrada.")
        
        self.db.disconnect()
        return result
    

    # ================================================ Editar reserva
    def updReserva(self, reservaId, hospedeId, quartoId, data_Entrada, data_Saida):
        query = f'''
                UPDATE Reservas
                SET
                    hospede_id = {hospedeId},
                    quarto_id = {quartoId},
                    data_entrada = {data_Entrada},
                    data_saida = {data_Saida}
                WHERE
                    id = {reservaId}
                '''
        hospedeTreatment = f'''
                            SELECT * FROM Hospedes
                            WHERE
                                id = '{hospedeId}'
                            '''
        
        quartoTreatment = f'''
                        SELECT * FROM Quartos
                        WHERE
                            id = '{quartoId}'
                        '''
        try:
            self.db.connect()

            if data_Entrada >= data_Saida:
                raise ValueError("A data de saída deve ser maior que a de entrada")

            treatments = [hospedeTreatment, quartoTreatment]
            auth = True
            for treatment in treatments:
                errorTreatment = self.db.fetchOne(treatment)
                if errorTreatment == None:
                    auth = False # id do quarto ou hospede nao existe
            
            if auth == True:
                result = self.db.executeQuery(query)
            else:
                raise ValueError("Não foi possível editar a reserva. Hóspede ou Quarto não existem ou estão indisponíveis no momento.")
            
            return result
        
        finally:
            self.db.disconnect()

    
    # ================================================ Listar Reserva
    def listReservas(self):
        query = f'''
                SELECT * FROM Reservas
                '''
        self.db.connect()
        result = self.db.fetchAll(query)

        self.db.disconnect()
        return result


    # ================================================ Buscar Reserva por ID
    def getReservaById(self, reservaId):
        query = f'''
                SELECT * FROM Reservas
                WHERE
                    id = {id}
                '''
        self.db.connect()
        result = self.db.fetchOne(query)

        self.db.disconnect()
        return result