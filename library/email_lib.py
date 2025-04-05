import json
import requests

def send_email_notification(recipient_email, order_status, order_id):
    try:
        API_URL = "https://ay4wp7fc97.execute-api.us-west-1.amazonaws.com/prod/send_emails"
        API_KEY = "rKTmbOUNfR6Wkv5MM3ALV7cmYKpADL3J9zdlPwcS"

        payload = {
            "recipient_email": recipient_email,
            "order_status": order_status,
            "order_id": str(order_id)
        }

        headers = {
            "Content-Type": "application/json",
            "x-api-key": API_KEY
        }

        response = requests.post(API_URL, data=json.dumps(payload), headers=headers)

        if response.status_code == 200:
            return {"status": "success", "message": "Email sent successfully."}
        else:
            return {"status": "error", "message": f"Failed to send email. API Response: {response.text}"}

    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"Error sending email: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"An unexpected error occurred: {str(e)}"}
