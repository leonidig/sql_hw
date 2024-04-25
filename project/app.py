import requests
from flask import Flask, render_template, request

app = Flask(__name__)


#  НА ДАННИЙ МОММЕНТ ERROR HTML НЕ ПРАЦЮЄ !!!

KEY = "46033ace9a69fa3a645ed1d86d45ab9b"


error_codes = [502, 404, 403, 500, 401]


@app.route('/')
def home():
    return render_template('form.html')


@app.post('/weather')
def weather():
    city = request.form['city']
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={KEY}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        weather = data["main"]
        temperature = weather["temp"]
        feels_like = weather["feels_like"]
        description = data["weather"][0]["description"]
        return render_template('index.html', city=city, temperature=temperature, feels_like=feels_like, description=description)

    else: 
        if response.status_code in error_codes:
            def error_handling(error):
                return render_template('error.html', code=error.code)

            for error in error_codes:
                app.register_error_handler(error, error_handling)


if __name__ == '__main__':
    app.run(debug=True)


