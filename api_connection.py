from flask import Flask, request, jsonify
from models import Singer, Queue

app = Flask(__name__)
karaoke_queue = Queue()

@app.route('/queue/add', methods=['POST'])
def add_singer():
    data = request.json
    name = data.get('name')
    song = data.get('song')
    
    if not name or not song:
        return jsonify({'error': 'Missing name or song'}), 400

    singer = Singer(name, song)
    karaoke_queue.add_singer(singer)
    return jsonify({'message': f"{name} added with song '{song}'"})

@app.route('/queue/next', methods=['GET'])
def next_singer():
    singer = karaoke_queue.next_singer()
    if singer:
        return jsonify({'next': str(singer)})
    return jsonify({'message': 'Queue is empty'})

@app.route('/queue', methods=['GET'])
def show_queue():
    return jsonify({'queue': karaoke_queue.show_queue()})

if __name__ == '__main__':
    app.run(debug=True)

