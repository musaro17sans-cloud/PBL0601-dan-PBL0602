from urllib.parse import unquote
from sanic import Sanic
from sanic.response import json, text
from peewee import *

app = Sanic("CarWebServer")

db = SqliteDatabase('carsweb.db')

class BaseModel(Model):
    class Meta:
        database = db

class TBCarsWeb(BaseModel):
    carname = TextField()
    carbrand = TextField()
    carmodel = TextField()
    carprice = TextField()

def create_tables():
    with db:
        db.create_tables([TBCarsWeb])

def serialize_car(row):
    return {
        'id': row.id,
        'carname': row.carname,
        'carbrand': row.carbrand,
        'carmodel': row.carmodel,
        'carprice': row.carprice
    }

def get_all_cars():
    return [serialize_car(row) for row in TBCarsWeb.select()]

@app.route('/')
async def masukkeindeks(request):
    return text("Server Ready (Sanic Web Service - PBL0602)")

@app.route('/read', methods=['GET'])
async def readdata(request):
    return json(get_all_cars())

@app.route('/cars', methods=['GET'])
async def get_cars(request):
    return json(get_all_cars())

@app.route('/cars/<car_id:int>', methods=['GET'])
async def get_car_by_id(request, car_id):
    car = TBCarsWeb.get_or_none(TBCarsWeb.id == car_id)
    if not car:
        return json({'error': 'Data tidak ditemukan'}, status=404)
    return json(serialize_car(car))

@app.route('/cars', methods=['POST'])
async def create_car(request):
    data = request.json or {}
    TBCarsWeb.create(
        carname=data.get('carname'),
        carbrand=data.get('carbrand'),
        carmodel=data.get('carmodel'),
        carprice=data.get('carprice')
    )
    return json(get_all_cars())

@app.route('/cars', methods=['PUT'])
async def update_car(request):
    data = request.json or {}
    car_id = data.get('id')
    if car_id:
        query = TBCarsWeb.update(
            carname=data.get('carname'),
            carbrand=data.get('carbrand'),
            carmodel=data.get('carmodel'),
            carprice=data.get('carprice')
        ).where(TBCarsWeb.id == car_id)
    else:
        query = TBCarsWeb.update(
            carbrand=data.get('carbrand'),
            carmodel=data.get('carmodel'),
            carprice=data.get('carprice')
        ).where(TBCarsWeb.carname == data.get('carname'))
    query.execute()
    return json(get_all_cars())

@app.route('/cars', methods=['DELETE'])
async def delete_car(request):
    data = request.json or {}
    car_id = data.get('id')
    if car_id:
        car_delete = TBCarsWeb.delete().where(TBCarsWeb.id == car_id)
    else:
        car_delete = TBCarsWeb.delete().where(TBCarsWeb.carname == data.get('carname'))
    car_delete.execute()
    return json(get_all_cars())

@app.route('/cars/search', methods=['GET'], name="search_car_all")
@app.route('/cars/search/<keyword:str>', methods=['GET'], name="search_car")
async def search_car(request, keyword=""):
    clean_keyword = unquote(keyword)
    rows = TBCarsWeb.select().where(
        (TBCarsWeb.carname.contains(clean_keyword)) |
        (TBCarsWeb.carbrand.contains(clean_keyword)) |
        (TBCarsWeb.carmodel.contains(clean_keyword))
    )
    return json([serialize_car(row) for row in rows])

if __name__ == '__main__':
    create_tables()
    app.run(host='0.0.0.0', port=5012, dev=True)