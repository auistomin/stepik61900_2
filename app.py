from flask import Flask, render_template, abort
from numpy import random
import data

app = Flask(__name__)


@app.route('/')
def render_index():
    indexes = [int(i) for i in range(1, len(data.tours) + 1)]
    indexes = random.choice(indexes, 6, replace=False)
    tours = dict([(i, data.tours[i]) for i in indexes])
    return render_template('index.html', tours=tours, departures=data.departures)


@app.route('/departures/<departure>/')
def render_departures(departure):
    if departure in data.departures:
        tours = dict()
        for key, tour in data.tours.items():
            if tour["departure"] == departure:
                tours[key] = tour
        n_tours = len(tours)
        suffix = ('a' if 2 <= n_tours % 10 <= 4 and n_tours % 100 // 10 != 1 else ('' if n_tours % 10 == 1 and n_tours % 100 // 10 != 1 else 'ов'))
        info = dict()
        info['n_tours'] = str(n_tours) + ' тур' + suffix
        info['price_min'] = min(tours.items(), key=lambda item: item[1]['price'])[1]['price']
        info['price_max'] = max(tours.items(), key=lambda item: item[1]['price'])[1]['price']
        info['nights_min'] = min(tours.items(), key=lambda item: item[1]['nights'])[1]['nights']
        info['nights_max'] = max(tours.items(), key=lambda item: item[1]['nights'])[1]['nights']
        return render_template('departure.html', departures=data.departures, departure=departure, info=info, tours=tours)
    else:
        abort(404)


@app.route('/tours/<int:tour_id>/')
def render_tours(tour_id):
    tour = data.tours.get(tour_id)
    if not tour is None:
        stars = '★' * int(tour['stars'])
        return render_template('tour.html', departures=data.departures, tour_id=tour_id, tour=tour, stars=stars)
    else:
        abort(404)


@app.route('/purchase/<int:tour_id>/')
def render_purchase(tour_id):
    abort(404)


@app.errorhandler(404)
def render_404(error):
    return render_template('404.html', departures=data.departures)


if __name__ == '__main__':
    app.run()