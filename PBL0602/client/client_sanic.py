import json
from urllib.parse import quote
import requests
from sanic import Sanic
from sanic.response import redirect
from sanic_ext import render

app = Sanic("CarWebClient")
app.static('/static', './static')

appType = 'Sanic Web Service'
API_URL = "http://localhost:5012"

@app.route('/')
async def index(request):
    return redirect(app.url_for('readcar'))
 
@app.route('/readcar', methods=['GET', 'POST'])
async def readcar(request):
    keyword = ""
    if request.method == 'POST':
        keyword = request.form.get('keyword', '').strip()
        if keyword:
            datas = requests.get(f"{API_URL}/cars/search/{quote(keyword)}")
        else:
            datas = requests.get(f"{API_URL}/cars")
    else:
        datas = requests.get(f"{API_URL}/cars")

    rows = json.loads(datas.text)
    return await render('readcar.html', context={"rows": rows, "appType": appType, "keyword": keyword})

@app.route('/createcar')
async def createcar(request):
    return await render('createcar.html', context={"appType": appType})

@app.route('/createcarsave', methods=['POST'])
async def createcarsave(request):
    datacar = {
        "carname": request.form.get('carName'),
        "carbrand": request.form.get('carBrand'),
        "carmodel": request.form.get('carModel'),
        "carprice": request.form.get('carPrice')
    }
    headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
    requests.post(f"{API_URL}/cars", data=json.dumps(datacar), headers=headers)
    return redirect(app.url_for('readcar'))

@app.route('/updatecar')
async def updatecar(request):
    car_id = request.args.get('id')
    datas = requests.get(f"{API_URL}/cars/{car_id}")
    car_data = json.loads(datas.text)
    return await render('updatecar.html', context={"appType": appType, "car": car_data})

@app.route('/updatecarsave', methods=['POST'])
async def updatecarsave(request):
    datacar = {
        "id": request.form.get('id'),
        "carname": request.form.get('carName'),
        "carbrand": request.form.get('carBrand'),
        "carmodel": request.form.get('carModel'),
        "carprice": request.form.get('carPrice')
    }
    headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
    requests.put(f"{API_URL}/cars", data=json.dumps(datacar), headers=headers)
    return redirect(app.url_for('readcar'))

@app.route('/deletecar')
async def deletecar(request):
    car_id = request.args.get('id')
    datas = requests.get(f"{API_URL}/cars/{car_id}")
    car_data = json.loads(datas.text)
    return await render('deletecar.html', context={"appType": appType, "car": car_data})

@app.route('/deletecarsave', methods=['POST'])
async def deletecarsave(request):
    datacar = {
        "id": request.form.get('id')
    }
    headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
    requests.delete(f"{API_URL}/cars", data=json.dumps(datacar), headers=headers)
    return redirect(app.url_for('readcar'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5011, dev=True)