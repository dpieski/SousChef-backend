from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from sqlalchemy import func, select
import os
import hashlib
import json
from recipeparsing import parse
from flask_heroku import Heroku

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

CORS(app)
#postgres://vhhabiabmrdtya:d2d626af16f4894a2a656de2ca8158f4414687b9b84ea08f801c2c07d774c6b8@ec2-54-243-241-62.compute-1.amazonaws.com:5432/d9d1mlh0cjs2lf

#app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://vhhabiabmrdtya:d2d626af16f4894a2a656de2ca8158f4414687b9b84ea08f801c2c07d774c6b8@ec2-54-243-241-62.compute-1.amazonaws.com:5432/d9d1mlh0cjs2lf"

#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://localhost/tigernest"
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:p@localhost:5432/souschef"

heroku = Heroku(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

#-----------------------------------------------------------------------------------------------------------------------------------------

class TrickyIngredient(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.Unicode, unique = False)

    def __init__(self, text): 
        self.text = text

class TrickyIngredientSchema(ma.Schema):
    class Meta:
        fields = ('id', 'text')

trickyingredient_schema = TrickyIngredientSchema()
trickyingredients_schema = TrickyIngredientSchema(many = True)

@app.route("/tricky", methods=["POST"])
def tricky_add():
    text = request.json['text']

    new_trickyingredient = TrickyIngredient(text)

    db.session.add(new_trickyingredient)
    db.session.commit()	
    
    #return jsonify({"original": new_trickyingredient.original, "rewritten": new_trickyingredient.rewritten})
    return trickyingredient_schema.jsonify(new_trickyingredient)

@app.route("/gettricky", methods=["GET"])
def tricky_get():
    ingredient = TrickyIngredient.query.order_by(func.random()).first()
    print(ingredient)
    return trickyingredient_schema.jsonify(ingredient)

#---------------------------------------------------------------------------------------------------------------------------------------------

class FixedIngredient(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    original = db.Column(db.Unicode, unique = False)
    rewritten = db.Column(db.Unicode, unique = False)

    def __init__(self, original, rewritten): 
        self.original = original
        self.rewritten = rewritten

class FixedIngredientSchema(ma.Schema):
    class Meta:
        fields = ('id', 'original', 'rewritten')

fixedingredient_schema = FixedIngredientSchema()
fixedingredients_schema = FixedIngredientSchema(many = True)
@app.route("/fixed", methods=["POST"])
def fixed_add():
    original = request.json['original']
    rewritten = request.json['rewritten']

    new_fixedingredient = FixedIngredient(original, rewritten)
    print(new_fixedingredient.original)
    print(new_fixedingredient.rewritten)

    db.session.add(new_fixedingredient)
    db.session.commit()	
    
    #return jsonify({"original": new_trickyingredient.original, "rewritten": new_trickyingredient.rewritten})
    return fixedingredient_schema.jsonify(new_fixedingredient)

db.create_all()
#---------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=os.environ.get("PORT", 5000))