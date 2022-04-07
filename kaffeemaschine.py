import random
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.device import IoTHubDeviceClient

CONNECTION_STRING_HUB = "HostName=iot3bhwii22-sk.azure-devices.net;SharedAccessKeyName=service;SharedAccessKey=f4P4f4EbxJWVVuAl/dxDeFwV3Ok/jLlGS5g1TYBrPJ0="
CONNECTION_STRING_COFFEE_MACHINE = "HostName=iot3bhwii22-sk.azure-devices.net;DeviceId=coffee_machine;SharedAccessKey=EYgNsYVH8xf+doe+PjF06gRRD//bkJwtI6eKlytH1OI="
DEVICE_ID = "Client1WaitForMessage"



def cm_2_hub():
    coffee_data = {"type": "", "amount": ""}
    coffee_type_name = ["cappuccino", "verlaengerter", "schwarz", "großer brauner", "kleiner brauner"]
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING_COFFEE_MACHINE)
    client.connect()
    coffee_amount = str(random.randint(0, 28))
    coffe_type_number = random.randint(0, 4)
    coffee_data["type"] = str(coffee_type_name[coffe_type_number])
    coffee_data["amount"] = str(coffee_amount)
    print(coffee_data)
    #print(coffee_type_name[coffe_type_number])
    client.send_message(str(coffee_data["type"]) + "\n" + str(coffee_data["amount"]))
    client.disconnect()
    client.shutdown()

"""
def main():
    registry_manager = IoTHubRegistryManager(CONNECTION_STRING_HUB)
    print('Sending message')

    data = "test"

    registry_manager.send_c2d_message(DEVICE_ID, data)
"""
if __name__ == '__main__':
    #main()
    cm_2_hub()