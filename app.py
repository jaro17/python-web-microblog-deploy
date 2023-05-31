import os

from flask import Flask, render_template, request
import datetime
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)
    client = MongoClient(os.getenv('MONGODB_URI'))
    app.db = client.microblog
    entries = []

    @app.route('/', methods=['GET', 'POST'])
    def home():
        if request.method == 'POST':
            entry_content = request.form.get('content')
            formatted_date = datetime.datetime.today().strftime('%Y-%m-%d')
            app.db.entries.insert_one({'content': entry_content, 'date': formatted_date})

        entries_with_date = [
            (
                entry[0],
                entry[1],
                datetime.datetime.strptime(entry[1], '%Y-%m-%d').strftime('%b %d')
            )
            for entry in entries
        ]

        return render_template('home.html', entries=entries_with_date)

    return app



# mongodb+srv://Jaroslav17:Uxg56N3IXfKVuaJ0@rest.c7rz3.mongodb.net/