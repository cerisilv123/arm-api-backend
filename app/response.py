from flask import jsonify

class Response:
    def __init__(self, message, status_code=200, data=[]):
        """
        Constructor for initializing the class with a message, data, and an optional status code.
        Success responses will always have status code 200 so it is set by default.

        Args:
            message (str): Message associated with the response.
            data (Any): Data payload of the response.
            status_code (int, optional): HTTP status code (default is 200).
        """
        self.message = message
        self.data = data
        self.status_code = status_code

    def return_error_response(self): 
        """
        Helper function to generate JSON error response.

        Parameters:
            error_message (str): The error message to be included in the response.
            status_code (int): The HTTP status code for the error.

        Returns:
            tuple: A tuple containing the JSON error response and the appropriate HTTP status code.
        """
        response = {
            'error': {
                'message': self.message,
                'status_code': self.status_code
            }
        }
        return jsonify(response), self.status_code
    
    def return_success_response(self):
        """
        Helper function to generate JSON success response.

        Parameters:
            success_message (str): The success message to be included in the response.
            data (list, optional): Additional data to be included in the response (default is an empty list).

        Returns:
            tuple: A tuple containing the JSON success response and the HTTP status code 200.
        """
        response = {
            'success': {
                'message': self.message, 
                'status_code': self.status_code,
                'data': self.data,
            }
        }
        return jsonify(response), 200
