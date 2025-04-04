from flask import Flask, render_template, redirect, url_for, request, flash, session
from config import DevelopmentConfig
from tasks import make_payment
from flask_login import LoginManager, current_user, login_required
from models import User

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Инициализация LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'


# Загрузка текущего пользователя
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Регистрация blueprint-а для аутентификации
from auth import auth as auth_blueprint

app.register_blueprint(auth_blueprint)


# Маршрут главной страницы
@app.route('/')
def index():
    return render_template('index.html')


# Маршрут для добавления товара в корзину
@app.route('/add_to_cart/<int:product_id>')
@login_required
def add_to_cart(product_id):
    if not session.get('cart'):
        session['cart'] = []

    session['cart'].append(product_id)
    flash(f'Товар {product_id} добавлен в корзину.')
    return redirect(url_for('index'))


# Маршрут для просмотра корзины
@app.route('/cart')
@login_required
def cart():
    return render_template('cart.html', cart=session.get('cart', []))


# Маршрут для оформления заказа
@app.route('/checkout', methods=['POST'])
@login_required
def checkout():
    if not session.get('cart'):
        flash('Корзина пуста.')
        return redirect(url_for('index'))

    # Асинхронная обработка платежа
    task = make_payment.delay(session['cart'])

    session.pop('cart', None)
    flash('Ваш заказ успешно оформлен!')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.secret_key = app.config['SECRET_KEY']
    app.run(debug=True, host='0.0.0.0', port=5000)
