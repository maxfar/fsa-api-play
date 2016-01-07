from __future__ import division
import json
import requests
from flask import Flask, render_template

FSA_API_HEADERS = {
    'x-api-version': '2',
    'accept': 'application/json',
    'content-type': 'application/json'}
FSA_API_ROOT = 'http://api.ratings.food.gov.uk/'
app = Flask(__name__)


@app.route('/authorities')
def index():
    authorities = get_authorities()

    return render_template('authorities.html', authorities=authorities)


def get_authorities():
    url = FSA_API_ROOT + 'Authorities/basic'
    result = requests.get(url, headers=FSA_API_HEADERS)

    authorities = json.loads(result.text)['authorities']
    if len(authorities) == 0:
        return None

    return authorities


@app.route('/authorities/<int:authority_id>')
def authority(authority_id):
    results = get_authority_results(authority_id)

    return render_template('ratings.html', results=results)


def get_authority_results(authority_id):
    ratings = get_ratings(authority_id)

    scores = {}
    for establishment in ratings:
        establishment_rating = establishment['RatingValue']
        if establishment_rating in scores:
            scores[establishment_rating] += 1
        else:
            scores[establishment_rating] = 1

    results = {}
    establishments = len(ratings)
    for score in scores:
        results[score] = rating_percentage(scores[score], establishments)

    return results


def rating_percentage(rating_count, total_establishments):
    return "{0:.0f}%".format(rating_count/total_establishments * 100)


def get_ratings(authority_id):
    url = FSA_API_ROOT + 'Establishments?localAuthorityId=' + str(authority_id)
    result = requests.get(url, headers=FSA_API_HEADERS)

    establishments = json.loads(result.text)['establishments']
    if len(establishments) == 0:
        return None

    return establishments


if __name__ == '__main__':
    app.debug = True
    app.run()
