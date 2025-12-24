# AWS IoT - Motion Detection System with Raspberry Pi

This project implements a complete serverless IoT solution using AWS and a Raspberry Pi. The system detects motion/proximity using an FC-51 infrared sensor and notifies the user via SMS using AWS Cloud services.

## 🏗 Architecture

1.  **Edge Device**: Raspberry Pi with an IR sensor (FC-51) running a Python script.
2.  **Communication**: Sends MQTT messages to **AWS IoT Core** when an object is detected.
3.  **Processing**: An AWS IoT Rule triggers an **AWS Lambda** function.
4.  **Notification**: The Lambda function uses **AWS Pinpoint** to send an SMS alert to the user.

## 📋 Prerequisites

### Hardware
* Raspberry Pi (3, 4, or Zero W)
* FC-51 Infrared Proximity Sensor
* Jumper wires

### Software & Cloud
* Active AWS Account.
* Python 3 installed on the Raspberry Pi.

## 🚀 Installation & Setup

### 1. AWS IoT Core Configuration
1.  Create a "Thing" in the AWS IoT Console.
2.  Generate and download the certificates (Device Certificate, Private Key, Root CA).
3.  Create an IoT Policy allowing `Connect`, `Publish`, and `Subscribe`, and attach it to the certificate.

### 2. Raspberry Pi Setup
1.  Clone this repository.
2.  Place the downloaded certificates in a folder (e.g., `certs/`).
3.  Install dependencies:
    ```bash
    pip3 install -r requirements.txt
    ```
4.  Connect the FC-51 Sensor:
    * **VCC** -> 5V (or 3.3V depending on the model)
    * **GND** -> GND
    * **OUT** -> GPIO 17 (Physical Pin 11)

### 3. Lambda & Pinpoint Configuration
1.  Create a project in **AWS Pinpoint** and enable the SMS channel.
2.  Create a **Lambda** function using the code provided in `lambda_function.py`.
3.  Add an Environment Variable `APP_ID` with your Pinpoint Project ID.
4.  Grant the Lambda execution role permission for `mobiletargeting:SendMessages`.
5.  Create a "Rule" in AWS IoT Core to trigger the Lambda when receiving messages on the topic `campus/IoT`.

## ▶️ Usage
On your Raspberry Pi, run the following command:

```bash
python3 device_script.py --endpoint YOUR_AWS_ENDPOINT.iot.us-east-1.amazonaws.com \
                         --cert certs/certificate.pem.crt \
                         --key certs/private.pem.key \
                         --root-ca certs/root-CA.pem
