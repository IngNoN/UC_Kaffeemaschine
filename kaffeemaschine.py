import random
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.device import IoTHubDeviceClient
import json
import time

CONNECTION_STRING_HUB = "HostName=iot3bhwii22-sk.azure-devices.net;SharedAccessKeyName=service;SharedAccessKey=f4P4f4EbxJWVVuAl/dxDeFwV3Ok/jLlGS5g1TYBrPJ0="
CONNECTION_STRING_COFFEE_MACHINE = "HostName=iot3bhwii22-sk.azure-devices.net;DeviceId=coffee_machine;SharedAccessKey=EYgNsYVH8xf+doe+PjF06gRRD//bkJwtI6eKlytH1OI="
DEVICE_ID = "Client1WaitForMessage"



def cm_2_hub():
    coffee_data = {"cm_id": "", "cmc": "", "type": "", "amount": ""}
    coffee_type_name = ["cappuccino", "verlaengerter", "schwarz", "großer brauner", "kleiner brauner"]
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING_COFFEE_MACHINE)
    client.connect()
    coffee_data["cm_id"] = "1"
    coffee_data["cmc"] = get_coffee_count()
    coffee_amount = str(random.randint(0, 28))
    coffe_type_number = random.randint(0, 4)
    coffee_data["type"] = str(coffee_type_name[coffe_type_number])
    coffee_data["amount"] = str(coffee_amount)
    print(coffee_data)
    coffee_data_json = json.dumps(coffee_data)
    #print(coffee_type_name[coffe_type_number])
    client.send_message(coffee_data_json)
    client.disconnect()
    client.shutdown()

    get_hub_answer()

"""
def main():
    registry_manager = IoTHubRegistryManager(CONNECTION_STRING_HUB)
    print('Sending message')

    data = "test"

    registry_manager.send_c2d_message(DEVICE_ID, data)
"""
"""
if __name__ == '__main__':
    main()
    """


def get_coffee_count():
    try:
        f = open("coffee_count.txt", "r")
    except:
        f = open("coffee_count.txt", "a")
        f = open("coffee_count.txt", "r")
    coffee_count = f.read()
    f = open("coffee_count.txt", "w")
    f.write(str(int(coffee_count) + 1))
    return coffee_count

RECEIVED_MESSAGES = 0

def message_handler(message):
    global RECEIVED_MESSAGES
    RECEIVED_MESSAGES += 1
    print("")
    print("Message received:")

    print(message)


def get_hub_answer():
    print ("Starting the Python IoT Hub C2D Messaging device sample...")

    # Instantiate the client
    client = IoTHubDeviceClient.create_from_connection_string("HostName=iot3bhwii22-sk.azure-devices.net;DeviceId=coffee_machine;SharedAccessKey=EYgNsYVH8xf+doe+PjF06gRRD//bkJwtI6eKlytH1OI=")

    print ("Waiting for C2D messages, press Ctrl-C to exit")
    try:
        # Attach the handler to the client
        client.on_message_received = message_handler
        while True:
            time.sleep(1000)
    except KeyboardInterrupt:
        print("IoT Hub C2D Messaging device sample stopped")
    finally:
        # Graceful exit
        print("Shutting down IoT Hub Client")
        client.shutdown()


if __name__ == "__main__":
    cm_2_hub()