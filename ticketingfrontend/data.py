import requests
from configparser import ConfigParser
from ticketingfrontend import cache_service
import logging


class DataService:

    def __init__(self):

        config_object = ConfigParser()
        config_object.read("TicketingBackground/TicketingFrontend/ticketingfrontend/config.ini")
        path_config = config_object['PATHS']
        self.secret_key = config_object['KEYS']['api_key']
        self.get_user_url = path_config['get_user']
        self.get_ticket_url = path_config['get_ticket']
        self.get_users_url = path_config['get_users']
        self.get_tickets_url = path_config['get_tickets']
        self.get_posts_url = path_config['get_posts']
        self.save_user_url = path_config['save_user']
        self.save_ticket_url = path_config['save_ticket']
        self.save_post_url = path_config['save_post']
        self.save_relation_url = path_config['save_relation']
        self.validate_user_url = path_config['validate_user']
        self.str_search_users_url = path_config['str_search_users']

        logging.info('DataService innitialized')

    def validate_user(self, password, login='', email=''):

        # try to use cached data
        data = cache_service.get_verification(login + email + password)

        if data:
            logging.info(f"using cached- {data}")
            response = data

        # if not available query the database
        else:
            payload = {'password': password}
            if login:
                payload['login'] = login
            if email:
                payload['email'] = email
            json_request = {'secretkey': self.secret_key, 'payload': payload}
            logging.info( f"sending request {json_request}")
            raw_response = requests.post(self.validate_user_url, json=json_request)

            if raw_response.ok:
                response = raw_response.json()
            else:
                logging.warning('Validate User - response error ' + str(raw_response))
                return None, None

        user_id = response['user_id']
        valid_password = response['valid_password']

        if not data:
            # populate the cache if not used
            cache_service.set_verification(login + email + password, response)

        logging.info(f'Validate User - success {user_id} - {valid_password}')
        return user_id, valid_password

    def save_user(self, login, password, email, position, name, picture='default.jpg'):

        payload = {'login': login, 'password': password, 'email': email, 'position': position, 'name': name,
                   'picture': picture}
        json_request = {'secretkey': self.secret_key, 'payload': payload}
        requests.post(self.save_user_url, json=json_request)

    def get_user(self, user_id):

        # try to use cached data
        data = cache_service.get_user(user_id)

        if data:
            response = data

        # if not available query the database
        else:
            payload = {'user_id': user_id}
            json_request = {'secretkey': self.secret_key, 'payload': payload}

            raw_response = requests.post(self.get_user_url, json=json_request)

            if raw_response.ok:
                response = raw_response.json()
            else:
                logging.warning('Validate User - response error ' + str(raw_response))
                return None

        if not data:
            # populate the cache if not used
            cache_service.set_user(user_id, response)
        logging.info(f'Get User - success {user_id} -  {response}')
        return response

    def save_ticket(self, title, status, deadline):

        payload = {'title': title, 'status': status, 'deadline': deadline}
        json_request = {'secretkey': self.secret_key, 'payload': payload}

        raw_response = requests.post(self.save_ticket_url, json=json_request)
        if raw_response.ok:
            response = raw_response.json()
        else:
            logging.warning('Ticket Saving - response error ' + str(raw_response))
            return None
        return response

    def save_relation(self, user_id, ticket_id, role):

        payload = {'user': user_id, 'ticket': ticket_id, 'role': role}
        json_request = {'secretkey': self.secret_key, 'payload': payload}
        cache_service.clear_tickets(str(user_id)+role)
        requests.post(self.save_relation_url, json=json_request)

    def save_post(self, user_id, ticket_id, content, status_change=None):

        payload = {'author_id': user_id, 'ticket_id': ticket_id, 'content': content, 'status_change': status_change}
        json_request = {'secretkey': self.secret_key, 'payload': payload}
        cache_service.clear_posts(ticket_id)
        requests.post(self.save_post_url, json=json_request)

    def get_tickets(self, user_id, role='author'):

        # try to use cached data
        data = cache_service.get_tickets(str(user_id)+role)

        if data:
            response = data

        # if not available query the database
        else:
            payload = {'user': user_id, 'role': role}
            json_request = {'secretkey': self.secret_key, 'payload': payload}

            raw_response = requests.post(self.get_tickets_url, json=json_request)

            if raw_response.ok:
                response = raw_response.json()
            else:
                logging.warning('Get Tickets - response error ' + str(raw_response))
                return None

        if not data:
            # populate the cache if not used
            cache_service.set_user(str(user_id)+role, response)
        logging.info(f'Get User - success {user_id} -  {response}')
        return response

    def get_ticket(self, ticket_id):

        # try to use cached data
        data = cache_service.get_ticket(ticket_id)

        if data:
            response = data

        # if not available query the database
        else:
            payload = {'ticket_id': ticket_id}
            json_request = {'secretkey': self.secret_key, 'payload': payload}

            raw_response = requests.post(self.get_ticket_url, json=json_request)

            if raw_response.ok:
                response = raw_response.json()
            else:
                logging.warning('Get Ticket - response error ' + str(raw_response))
                return None

            if not data:
                # populate the cache if not used
                cache_service.set_ticket(ticket_id, response)
            return response

    def get_posts(self, ticket_id):

        # try to use cached data
        data = cache_service.get_posts(ticket_id)

        if data:
            response = data

        # if not available query the database
        else:
            payload = {'ticket': ticket_id}
            json_request = {'secretkey': self.secret_key, 'payload': payload}

            raw_response = requests.post(self.get_posts_url, json=json_request)

            if raw_response.ok:
                response = raw_response.json()
            else:
                logging.warning('Get Posts - response error ' + str(raw_response))
                return None

        if not data:
            # populate the cache if not used
            cache_service.set_posts(ticket_id, response)
        logging.info(f'Get User - success {ticket_id} -  {response}')
        return response
