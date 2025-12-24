```python
import time
import json
import argparse
import RPi.GPIO as GPIO
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder

# Sensor Configuration (FC-51)
SENSOR_PIN = 17  # Adjust GPIO pin according to your wiring
TOPIC = "campus/IoT"

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

def parse_arguments():
    parser = argparse.ArgumentParser(description="AWS IoT Core + Raspberry Pi FC-51")
    parser.add_argument('--endpoint', required=True, help="Your AWS IoT Endpoint")
    parser.add_argument('--cert', required=True, help="Path to device certificate")
    parser.add_argument('--key', required=True, help="Path to private key")
    parser.add_argument('--root-ca', required=True, help="Path to Root CA certificate")
    parser.add_argument('--client-id', default="raspi-sensor", help="MQTT Client ID")
    return parser.parse_args()

def init_mqtt_connection(args):
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=args.endpoint,
        cert_filepath=args.cert,
        pri_key_filepath=args.key,
        client_bootstrap=client_bootstrap,
        ca_filepath=args.root_ca,
        client_id=args.client_id,
        clean_session=False,
        keep_alive_secs=6
    )
    return mqtt_connection

def main():
    args = parse_arguments()
    
    print(f"Connecting to AWS IoT Core at {args.endpoint}...")
    mqtt_connection = init_mqtt_connection(args)
    connect_future = mqtt_connection.connect()
    connect_future.result()
    print("Connected successfully!")

    try:
        print("Waiting for motion detection (CTRL+C to exit)...")
        while True:
            # FC-51 usually sends 0 (LOW) when an object is detected
            if GPIO.input(SENSOR_PIN) == 0:
                print("[!] Object detected")
                
                message = {
                    "message": "Alert: Motion detected on Raspberry Pi",
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "sensor_id": "FC-51"
                }
                message_json = json.dumps(message)
                
                mqtt_connection.publish(
                    topic=TOPIC,
                    payload=message_json,
                    qos=mqtt.QoS.AT_LEAST_ONCE
                )
                print(f"Message published to '{TOPIC}': {message_json}")
                
                # Wait a few seconds to avoid spamming messages
                time.sleep(5) 
            
            time.sleep(0.1) # Short delay to reduce CPU usage

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        mqtt_connection.disconnect()
        GPIO.cleanup()

if __name__ == '__main__':
    main()
