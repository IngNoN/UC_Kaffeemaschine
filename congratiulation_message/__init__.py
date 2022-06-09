import logging
from azure.iot.hub import IoTHubRegistryManager
import azure.functions as func


DEVICE_ID = "coffee_machine"
CONNECTION_STRING = "HostName=iot3bhwii22-sk.azure-devices.net;SharedAccessKeyName=service;SharedAccessKey=f4P4f4EbxJWVVuAl/dxDeFwV3Ok/jLlGS5g1TYBrPJ0="

def main(msg: func.ServiceBusMessage):
    logging.info('Python ServiceBus queue trigger processed message: %s',
                 msg.get_body().decode('utf-8'))

    logging.info("test")
    registry_manager = IoTHubRegistryManager(CONNECTION_STRING)
    data = "Congratulation! You won a free coffee"

    props={}
    # optional: assign system properties
    props.update(messageId = "message_1")
    props.update(correlationId = "correlation_1")
    props.update(contentType = "application/json")

    # optional: assign application properties
    prop_text = "PropMsg_1"
    props.update(testProperty = prop_text)

    registry_manager.send_c2d_message(DEVICE_ID, data, properties=props)
