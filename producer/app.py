from flask import Flask, render_template, request
from azure.servicebus import ServiceBusClient, ServiceBusMessage

app = Flask(__name__, template_folder='templates')

CONNECTION_STR = "Endpoint=sb://test-ucu.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=lk+fUlxaTNXNmjGJ4aWQazOFCDT5yA78+6NErPz7ofI="
QUEUE_NAME = "message-queue"


@app.route("/", methods=['post', 'get'])
def hello():
    servicebus_client = ServiceBusClient.from_connection_string(
        conn_str=CONNECTION_STR, logging_enable=True)
    with servicebus_client:
        sender = servicebus_client.get_queue_sender(queue_name=QUEUE_NAME)
        with sender:
            if request.method == 'POST':
                message = request.form.get('message')
                sb_message = ServiceBusMessage(message)
                sender.send_messages(sb_message)
    return render_template("form.html")
