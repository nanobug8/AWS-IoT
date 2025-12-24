import json
import boto3
import os

# Initialize Pinpoint client
pinpoint = boto3.client('pinpoint')

def lambda_handler(event, context):
    # Your Pinpoint Project ID (set as an environment variable in Lambda)
    application_id = os.environ.get('APP_ID', 'YOUR_PROJECT_ID_HERE')
    
    # Message Type (TRANSACTIONAL or PROMOTIONAL)
    message_type = 'PROMOTIONAL'
    
    # Destination Number (must be verified if in sandbox mode)
    destination_number = '+1234567890' 
    
    # Message Content
    # We can parse the incoming IoT event if needed
    message_content = "IoT Alert: The Raspberry Pi sensor has been triggered."

    try:
        response = pinpoint.send_messages(
            ApplicationId=application_id,
            MessageRequest={
                'Addresses': {
                    destination_number: {
                        'ChannelType': 'SMS'
                    }
                },
                'MessageConfiguration': {
                    'SMSMessage': {
                        'Body': message_content,
                        'MessageType': message_type,
                    }
                }
            }
        )
        print("Message sent successfully: " + json.dumps(response))
        return {
            'statusCode': 200,
            'body': json.dumps('SMS sent successfully')
        }
        
    except Exception as e:
        print(f"Error sending SMS: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error sending SMS')
        }
