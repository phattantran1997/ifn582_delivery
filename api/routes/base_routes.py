from flask import Blueprint, jsonify, request
from utils.mysql_init import MySQLManager

class BaseRoute:
    def __init__(self, service_class):
        self.service_class = service_class
        self._service = None

    @property
    def service(self):
        if self._service is None:
            self._service = self.service_class()
        return self._service 