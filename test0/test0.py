#! /usr/bin/python3

import datetime
import getpass
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")
    return

if __name__ == "__main__":
    host = "aidbd7qwhz382.iot.us-west-2.amazonaws.com"
    userId = getpass.getuser()
    rootCAPath = "/home/{}/Certificates/root-CA.crt".format(userId)
    certificatePath = "/home/{}/Certificates/UCLARaspberryPiTesting.cert.pem".format(userId)
    privateKeyPath = "/home/{}/Certificates/UCLARaspberryPiTesting.private.key".format(userId)

    myAWSIoTMQTTClient = AWSIoTMQTTClient("test0")
    myAWSIoTMQTTClient.configureEndpoint(host, 8883)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath,
                                            certificatePath)
    
    # AWSIoTMQTTClient connection configuration
    myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
    myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)
    myAWSIoTMQTTClient.configureDrainingFrequency(2)
    myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
    
    # Connect and subscribe to AWS IoT
    myAWSIoTMQTTClient.connect()
    loopCount = 0
    command_str = ''
    topic = "RaspberryPi/test0"
    delay_s = 60
    sensor_sn = 'dev_r00000002'

    try:
        while True:
            timestamp = datetime.datetime.now()
            print(' Time: {} \n'.format(timestamp))
            msg = '"Device": "{:s}", "Loop": "{}"'.format(sensor_sn, loopCount)
            msg = '{'+msg+'}'
            myAWSIoTMQTTClient.publish(topic, msg, 1)
            print('Sleeping...')
            time.sleep(delay_s)
    except:
        print('Exiting the loop')
        myAWSIoTMQTTClient.disconnect()
        print('Disconnected from AWS')
