from django.db import connections


class LookerDb:
    def __init__(self, connection_name, db_settings):
        self.connection_name = connection_name
        self.db_settings = db_settings

    def establish_connection(self):
        connections.databases[self.connection_name] = self.db_settings
        connections.ensure_defaults(self.connection_name)

    def execute_query(self, query):
        with connections[self.connection_name].cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
        return results
