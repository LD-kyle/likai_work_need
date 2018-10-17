# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 10:24:18 2018

@author: Administrator
"""

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__=='__main__':
    app.run()