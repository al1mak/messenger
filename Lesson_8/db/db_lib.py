from db.db import Client, ClientContact


class Storage:

    def __init__(self, session):
        self.session = session

    def add_client(self, name):
        new_client = Client(name)

        if self.is_client(name) is True:
            print('Такой клиент уже существует')
        else:
            self.session.add(new_client)
            self.session.commit()

    def remove_client(self, name):
        client = self.get_client(name)
        self.session.delete(client)
        self.session.commit()

    def get_client(self, name):
        client = self.session.query(Client).filter(Client.Name == name).first()
        return client


    def get_clients(self):
        clients = self.session.query(Client).all()
        return clients

    def is_client(self, username):
        """Проверка, что клиент уже есть"""
        result = self.session.query(Client).filter(Client.Name == username).count() > 0
        return result

    def add_contact(self, client_username, contact_username):
        """Добавление контакта"""
        contact = self.get_client(contact_username)
        if contact:
            client = self.get_client(client_username)
            if client:
                cc = ClientContact(client_id=client.ClientId, contact_id=contact.ClientId)
                self.session.add(cc)
                self.session.commit()
            else:
                # raise NoneClientError(client_username)
                pass
        else:
            raise print('Contact {} does not exist'.format(client_username))

    def del_contact(self, client_username, contact_username):
        """Удаление контакта"""
        contact = self.get_client(contact_username)
        if contact:
            client = self.get_client(client_username)
            if client:
                cc = self.session.query(ClientContact).filter(
                    ClientContact.ClientId == client.ClientId).filter(
                    ClientContact.ContactId == contact.ClientId).first()
                self.session.delete(cc)
                self.session.commit()
            else:
                # raise NoneClientError(client_username)
                pass
        else:
            raise print('Contact {} does not exist'.format(contact_username))

    def get_contacts(self, client_username):
        """Получение контактов клиента"""
        client = self.get_client(client_username)
        result = []
        if client:
            # Тут нету relationship поэтому берем запросом
            contacts_clients = self.session.query(ClientContact).filter(ClientContact.ClientId == client.ClientId)
            for contact_client in contacts_clients:
                contact = self.session.query(Client).filter(Client.ClientId == contact_client.ContactId).first()
                result.append(contact)
        return result