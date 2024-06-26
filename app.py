from flask import Flask, render_template, request, redirect, url_for
from ContentBasedRecommendation import generate_recommendations
from CollaborativeFilteringTechnique import recommend_courses
from courses import courses
from course_by_genre import course_by_genre
from hybrid import hybrid_recommendation
import pandas as pd

app = Flask(__name__)

users = {'admin': 'admin123'}

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/content-recommend',methods=['POST'])
def content_recommend():
    if request.method == 'POST':
        selected_courses = request.form.getlist('courses')
        recommendations = generate_recommendations(selected_courses,0.5,0)
        return render_template('recommendations.html', recommendations=recommendations)

@app.route('/submit-ratings', methods=['POST'])
def collaborative():
    if request.method == 'POST':
        user_ratings = {}
        for course, rating in request.form.items():
            if rating=='0':
                continue
            user_ratings[course] = float(rating)
        user_profile = pd.Series(user_ratings, name='target_user')
        recommendations = recommend_courses(user_profile, 0.7)
        
        second_pass_content = []
        for item, score in recommendations[:5]:
            second_pass_content.append(item)
        second_recommend = generate_recommendations(second_pass_content,0.7,1)
        net_recommendation = hybrid_recommendation(recommendations, second_recommend)
        return render_template('final_page.html', net_recommendation=net_recommendation)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username in users and users[username] == password:
        return redirect(url_for('dashboard', username=username))
    else:
        return render_template('login.html', message='Invalid username or password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return render_template('register.html', message='Username already exists')
        else:
            users[username] = password
            return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/dashboard/<username>')
def dashboard(username):
    return render_template('home.html', username=username, courses=courses, course_by_genre = course_by_genre)

if __name__ == '__main__':
    app.run(debug=True)