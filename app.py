from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Inisialisasi Firebase
cred = credentials.Certificate("serviceAccount.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


@app.route('/api/users', methods=['GET'])
def get_all_data():
    data = []
    # Ambil semua data dari Firestore
    collection_ref = db.collection('users')
    docs = collection_ref.stream()
    for doc in docs:
        data.append(doc.to_dict())
    return jsonify(data)


@app.route('/api/users/<doc_id>', methods=['GET'])
def get_data_by_id(doc_id):
    # Ambil data dari Firestore berdasarkan ID
    doc_ref = db.collection('users').document(doc_id)
    doc = doc_ref.get()

    if doc.exists:
        return jsonify(doc.to_dict())
    else:
        return jsonify({"message": "Document not found"}), 404


@app.route('/api/users', methods=['POST'])
def add_data():
    new_data = request.json
    # Tambahkan data ke Firestore
    collection_ref = db.collection('users')
    collection_ref.add(new_data)
    return jsonify({"message": "Data added successfully"}), 201


@app.route('/api/users/<doc_id>', methods=['DELETE'])
def delete_data_by_id(doc_id):
    # Hapus data dari Firestore berdasarkan ID
    doc_ref = db.collection('users').document(doc_id)
    doc = doc_ref.get()

    if doc.exists:
        doc_ref.delete()
        return jsonify({"message": "Document deleted successfully"}), 200
    else:
        return jsonify({"message": "Document not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
