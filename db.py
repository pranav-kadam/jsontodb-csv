import json
import sqlite3
import pandas as pd

json_file = 'example_2.json'

with open(json_file, 'r') as file:
    data = json.load(file)

def create_table_and_insert_data(data):
    connection = sqlite3.connect('quiz_data.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz_questions (
            category TEXT,
            question_id TEXT,
            question TEXT,
            options TEXT,
            answer TEXT
        )
    ''')

    for category, category_data in data['quiz'].items():
        for question_id, question_data in category_data.items():
            question = question_data['question']
            options = json.dumps(question_data['options'])
            answer = question_data['answer']
            cursor.execute('INSERT INTO quiz_questions (category, question_id, question, options, answer) VALUES (?, ?, ?, ?, ?)',
                           (category, question_id, question, options, answer))

    connection.commit()
    connection.close()

create_table_and_insert_data(data)

def retrieve_data():
    connection = sqlite3.connect('quiz_data.db')
    cursor = connection.cursor()

    cursor.execute('SELECT category, question_id, question, options, answer FROM quiz_questions')
    data = cursor.fetchall()

    connection.close()
    return data

retrieved_data = retrieve_data()

def export_to_csv(data, filename):
    df = pd.DataFrame(data, columns=['Category', 'Question ID', 'Question', 'Options', 'Answer'])
    df.to_csv(filename, index=False)

export_to_csv(retrieved_data, 'quiz_data.csv')
