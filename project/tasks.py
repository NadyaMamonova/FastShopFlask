from celery import Celery
from config import DevelopmentConfig

# app = Celery('tasks', broker=DevelopmentConfig.CELERY_BROKER_URL, backend=DevelopmentConfig.CELERY_RESULT_BACKEND)

app = Celery('tasks')  # Только указание имени приложения
app.conf.broker_url = 'redis://localhost:6379/0'  # Настраиваем после
app.conf.result_backend = 'redis://localhost:6379/0'  # Настраиваем после


@app.task
def make_payment(cart):
    # Симуляция обработки платежа
    print(f'Обработка заказа: {cart}')
    return True