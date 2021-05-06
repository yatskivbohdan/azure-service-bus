from flask import Flask, render_template, request
from azure.servicebus import ServiceBusClient, ServiceBusMessage

app = Flask(__name__)

CONNECTION_STR = "Endpoint=sb://test-ucu.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=lk+fUlxaTNXNmjGJ4aWQazOFCDT5yA78+6NErPz7ofI="
QUEUE_NAME = "message-queue"
messages = []


@app.route("/", methods=['post', 'get'])
def hello():
    global messages
    servicebus_client = ServiceBusClient.from_connection_string(
        conn_str=CONNECTION_STR, logging_enable=True)
    with servicebus_client:
        receiver = servicebus_client.get_queue_receiver(
            queue_name=QUEUE_NAME, max_wait_time=5)
        with receiver:
            for msg in receiver:
                receiver.complete_message(msg)
                messages.append(str(msg))
    return render_template("result.html", value=str({"messages": messages}))
