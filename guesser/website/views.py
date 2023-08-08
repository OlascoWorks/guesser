from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user
from .models import User
from . import db
import random

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@views.route('/home', methods=['GET', 'POST'])
def home():
    users = User.query.all()
    high_scores = []
    for user in users:
        high_scores.append(user.high_score)
    high_scores.sort()
    top_ten = []
    for high_score in high_scores[:10]:
        for user in users:
            if user.high_score == high_score:
                top_ten.append(user)
                break
    top_ten.reverse()

    return render_template('base.html', user=current_user, top_ten=top_ten, rank=1)

@views.route('/game', methods=['GET', 'POST'])
def game():
    return render_template('home.html', user=current_user)

@views.route('/get-num', methods=['POST'])
def get_num():
    wave = request.json['wave']
    range = wave*50
    num = random.randint(0, range)

    # Save current wave as high score
    if current_user.is_authenticated:
        user = User.query.filter_by(name=current_user.name).first()
        if user.high_score < wave:
            user.high_score = wave
            db.session.commit()

    return jsonify(num)