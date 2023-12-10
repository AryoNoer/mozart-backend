from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Inisialisasi Firebase
cred = credentials.Certificate("serviceAccount.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# Route untuk mendapatkan semua data pengguna


@app.route('/api/users', methods=['GET'])
def get_data():
    data = []
    # Ambil data dari Firestore
    collection_ref = db.collection('user')
    docs = collection_ref.stream()
    for doc in docs:
        data.append(doc.to_dict())
    return jsonify(data)


# Route untuk menambahkan pengguna baru
@app.route('/api/users', methods=['POST'])
def add_data():
    new_data = request.json.get("data")

    if new_data is None:
        return jsonify({"message": "Invalid data format"}), 400

    # Tambahkan data ke Firestore
    collection_ref = db.collection('user')
    doc_ref, = collection_ref.add(new_data)

    # Dapatkan data pengguna langsung setelah menambahkannya
    user_data = doc_ref.get().to_dict()

    return jsonify({"message": "Data added successfully", "user": user_data}), 201


# Route untuk mendapatkan data pengguna berdasarkan ID


@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user_ref = db.collection('user').document(user_id)
    user_data = user_ref.get()
    if user_data.exists:
        return jsonify(user_data.to_dict())
    else:
        return jsonify({"message": "User not found"}), 404

# Route untuk mengupdate data pengguna berdasarkan ID


@app.route('/api/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user_ref = db.collection('user').document(user_id)
    user_data = user_ref.get()

    if user_data.exists:
        updated_data = request.json
        user_ref.update(updated_data)
        return jsonify({"message": "User updated successfully"}), 200
    else:
        return jsonify({"message": "User not found"}), 404

# Route untuk menghapus data pengguna berdasarkan ID


@app.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user_ref = db.collection('user').document(user_id)
    user_data = user_ref.get()

    if user_data.exists:
        user_ref.delete()
        return jsonify({"message": "User deleted successfully"}), 200
    else:
        return jsonify({"message": "User not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
