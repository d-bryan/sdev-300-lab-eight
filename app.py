"""
File: app.py
Author: Dylan Bryan
Date: 11/22/20, 1:29 PM
Project: Lab-6
Purpose: Main application file which calls
the rest of the project
"""

from flask import Flask

app = Flask(__name__)

# import routes from routes
import routes

if __name__ == '__main__':
    app.run()
