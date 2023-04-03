import dill
import pandas as pd
from flask import json
from flask import Flask, request
from flask import render_template


# Загружаем обученные модели
with open('models/xgb_predictor.dill', 'rb') as in_strm:
    model = dill.load(in_strm)


# Обработчики и запуск Flask
app = Flask(__name__)

@app.route("/", methods=["GET"])
def general():
    return render_template('drugs.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = {"success": False}

    # ensure an image was properly uploaded to our endpoint
    cat_columns = ['Age', 'Gender', 'Education', 'Country', 'Ethnicity']
    score_columns = ['Nscore', 'Escore', 'Oscore', 'AScore', 'Cscore', 'Impulsive', 'SS']
    legal_drugs_columns = ['Nicotine', 'Caff', 'Choc', 'Alcohol', 'Cannabis', 'Mushrooms']
    columns = cat_columns + score_columns + legal_drugs_columns

    request_data = request.form
    char_dict = {}
    for col in columns:
        char_dict[col] = [request_data.get(col, '')]

    drugs_df = pd.DataFrame.from_dict(char_dict)

    for col in cat_columns:
        drugs_df[col] = drugs_df[col].astype('category')
    for col in score_columns:
        drugs_df[col] = pd.to_numeric(drugs_df[col])
    for col in legal_drugs_columns:
        drugs_df[col] = pd.to_numeric(drugs_df[col])

    preds = model.predict(drugs_df)

    data["predictions"] = preds

    # indicate that the request was a success
    data["success"] = True
    print('OK')

    # return the data dictionary as a JSON response
    return json.jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0')