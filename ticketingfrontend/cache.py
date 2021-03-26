#placeholder for redis accessing interfaces


class CacheService:

    verification ={}
    user= {}
    tickets = {}
    ticket = {}
    posts = {}


    def get_verification(self, search_str):

        if search_str not in self.verification:
            return None

        return self.verification[search_str]

    def set_verification(self, search_str, response):

        self.verification[search_str] = response


    def get_user(self, user_id):

        if user_id not in self.user:
            return None

        return self.user[user_id]

    def set_user(self, user_id, response):

        self.user[user_id]=response

    def get_tickets(self, search_str):

        if search_str not in self.tickets:
            return None

        return self.tickets[search_str]

    def set_tickets(self, search_str, response):

        self.tickets[search_str] = response

    def get_ticket(self, ticket_id):
        if ticket_id not in self.ticket:
            return None

        return self.ticket[ticket_id]

    def set_ticket(self, ticket_id, response):
        self.ticket[ticket_id] = response

    def get_posts(self, ticket_id):
        if ticket_id not in self.posts:
            return None

        return self.posts[ticket_id]

    def set_posts(self, ticket_id, response):
        self.posts[ticket_id] = response

    def clear_posts(self, ticket_id):
        self.posts.pop(ticket_id, None)

    def clear_tickets(self, search_str):
        self.tickets.pop(search_str, None)