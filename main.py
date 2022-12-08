from sqlalchemy import true
from edapp import app
from flask import Flask, render_template,flash

if __name__ == '__main__':
    app.run(debug=true)

