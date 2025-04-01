import pathlib as pl

import numpy as np
import pandas as pd

from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

data = pl.Path(__file__).parent.absolute() / 'data'

# Charger les données CSV
associations_df = pd.read_csv(data / 'associations_etudiantes.csv')
evenements_df = pd.read_csv(data / 'evenements_associations.csv')

## Vous devez ajouter les routes ici : 
@app.route('/associations', methods=['GET'])
def get_associations():
    return jsonify(associations_df.to_dict(orient='records'))

@app.route('/evenements', methods=['GET'])
def get_evenements():
    return jsonify(evenements_df.to_dict(orient='records'))


if __name__ == '__main__':
    app.run(debug=True)
