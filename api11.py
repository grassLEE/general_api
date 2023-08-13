from flask import Flask
from flask_restful import request, Api, Resource
import sqlite3
import os

class TotalPages(Resource):
    def get(self):
        conn = sqlite3.connect('dsworld.db')
        cursor = conn.cursor()

        cursor.execute("SELECT SUM(pages) FROM novels")
        total_pages = cursor.fetchone()[0]

        return {'total_pages': total_pages}