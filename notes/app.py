from flask import Flask, request, jsonify, redirect, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask_cors import CORS
from flask_socketio import SocketIO
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(500))
    done = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {'id': self.id, 'title': self.title, 'content': self.content, 'done': self.done}

@app.route('/')
def index():
    return redirect('/page-notes')

@app.route('/page-notes')
def page_notes():
    notes = Note.query.all()
    return render_template('notes.html.j2', notes=notes)

@app.route('/front/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/api/notes', methods=['GET', 'POST'])
def notes():
    if request.method == 'POST':
        data = request.get_json()
        note = Note(title=data['title'], content=data['content'])
        db.session.add(note)
        db.session.commit()
        socketio.emit('note_updated')
        return jsonify(note.to_dict()), 201
    else:
        return jsonify([note.to_dict() for note in Note.query.all()])
    
@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    note = Note.query.get(note_id)
    if not note:
        return jsonify({'error': 'Note not found'}), 404
    db.session.delete(note)
    db.session.commit()
    socketio.emit('note_updated')
    return jsonify({'ok': True})

@app.route('/api/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    note = Note.query.get(note_id)
    if not note:
        return jsonify({'error': 'Note not found'}), 404
    data = request.get_json()
    note.done = data.get('done', note.done)
    db.session.commit()
    socketio.emit('note_updated')
    return jsonify(note.to_dict())

if __name__ == '__main__':
    if not os.path.exists('notes.db'):
        with app.app_context():
            db.create_all()
    print("✅ Serveur en ligne sur http://localhost:5002")
    socketio.run(app, host="0.0.0.0", port=5002, debug=True)
