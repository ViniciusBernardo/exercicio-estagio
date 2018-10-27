import json
from http.client import HTTPSConnection


class Fetch():

    @staticmethod
    def make_request(url, method,
                     lookup_data=None, host='api.ubiplaces.com.br'):
        """
        This function allows to make a request using the default host
        and search for a specific key in the response
        """

        connection = HTTPSConnection(host)
        connection.request(method, url)

        response = connection.getresponse()
        data = json.loads(response.read())

        if lookup_data:
            data = data.get(lookup_data)

        return data
