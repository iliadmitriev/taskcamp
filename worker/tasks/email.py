from worker.app import app
from accounts.helpers import send_register_activation_email


@app.task
def send_activation_email(email, url_link):
    print(email, url_link)
    return send_register_activation_email(email, url_link)
