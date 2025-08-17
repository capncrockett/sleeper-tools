import csv
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will allow the frontend to make requests to this server

def load_adp_data():
    """Loads ADP data from the CSV file."""
    data = []
    try:
        with open('eleveners_2025_mock_adp.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert numerical fields to appropriate types
                for key in ['average_pick', 'std_dev', 'earliest_pick', 'latest_pick']:
                    if row.get(key):
                        try:
                            row[key] = float(row[key])
                        except (ValueError, TypeError):
                            row[key] = 0.0
                for key in ['times_drafted']:
                    if row.get(key):
                        try:
                            row[key] = int(row[key])
                        except (ValueError, TypeError):
                            row[key] = 0
                data.append(row)
    except FileNotFoundError:
        print("ADP data file not found.")
        return []
    return data

@app.route('/api/adp', methods=['GET'])
def get_adp():
    """API endpoint to get the ADP data."""
    adp_data = load_adp_data()
    return jsonify(adp_data)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
