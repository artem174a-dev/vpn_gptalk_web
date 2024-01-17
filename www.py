from datetime import timedelta, datetime

from flask import Flask, request, redirect, render_template, jsonify

from database import get_user_info, user_usage
import locale

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

app = Flask(__name__)


def bytes_to_gb(byte_value):
    gb_value = byte_value / (1024 ** 3)
    return round(gb_value, 2)


def days_until_next_update(registration_date):
    registration_date = datetime.strptime(registration_date, '%Y-%m-%d')
    next_tariff_update = registration_date + timedelta(days=30)
    day_of_month = next_tariff_update.day
    days_until_update = (next_tariff_update - datetime.now()).days
    month_name = next_tariff_update.strftime('%B')[:3].capitalize()
    return f'{day_of_month}, {month_name}.'


# URL index
@app.route('/')
def index():
    return render_template('index.html')


# URL monitor
@app.route('/monitor/<int:user_id>')
def monitor(user_id):
    data = get_user_info(user_id)
    usage = user_usage(user_id)
    print(usage)
    data_day = [float(bytes_to_gb(int(i['used_bytes']))) for i in usage]
    print(data_day)
    data_day = [0.03, 0.2, 1.2, 0.3, 2.2]
    return render_template(
        'monitor.html',
        user_id=user_id,
        remains=bytes_to_gb(int(data['used_bytes'])),
        update_date=days_until_next_update(str(data['key_reg_time'])[:10]),
        data_day_json=data_day
    )


# API #

# URL для оповещений
@app.route('/api/transaction_notification', methods=['GET'])
def transaction_notification():
    # Получение данных из запроса
    data = request.args
    print("Received transaction notification:", data)

    # Обработка оповещений здесь
    return "Notification received successfully"


# URL для успешной оплаты
@app.route('/pay_subscribtion', methods=['GET'])
def successful_payment():
    # Получение данных из запроса
    data = request.args
    print("Received successful payment notification:", data)

    # Обработка успешной оплаты здесь
    return "Payment successful. Thank you!"


# URL для возврата в случае неудачи
@app.route('/payment_failure', methods=['GET'])
def payment_failure():
    # Получение данных из запроса
    data = request.args
    print("Received payment failure notification:", data)

    # Обработка неудачной оплаты здесь
    return "Payment failed. Please try again."


# Путь к вашему приватному ключу
private_key_path = 'priv_key.pem'

# Путь к вашему сертификату
certificate_path = 'sert_key.pem'

# Загрузка SSL-сертификата и приватного ключа
context = (certificate_path, private_key_path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
