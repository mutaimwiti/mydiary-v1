from flask import make_response, jsonify
from app.models import ModelNotFoundException
from app.request import ValidationException
from utils import NOT_FOUND_MSG, SERVER_ERROR_MSG


class Handler:
    @staticmethod
    def response_message(code, message=''):
        return make_response(jsonify({'message': message}), code)

    @staticmethod
    def response_object(code, obj):
        return make_response(jsonify(obj), code)


class ExceptionHandler(Handler):
    @staticmethod
    def handle(exception):
        if type(exception) == ModelNotFoundException:
            return Handler.response_message(404, str(exception))
        if type(exception) == ValidationException:
            return Handler.response_object(422, exception.errors)


class HttpHandler(Handler):
    @staticmethod
    def handle(code):
        if code == 404:
            return Handler.response_message(404, NOT_FOUND_MSG)
        if code == 405:
            return Handler.response_message(404, NOT_FOUND_MSG)
        # 500 is the fallback
        return Handler.response_message(500, SERVER_ERROR_MSG)
