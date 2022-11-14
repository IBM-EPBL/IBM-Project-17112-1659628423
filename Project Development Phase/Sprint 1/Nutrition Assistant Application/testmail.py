from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def SendEmail(user_email, user_name):
    FROM_EMAIL =  "gokul.d.2019.cse@rajalakshmi.edu.in"
    TEMPLATE_ID = "d-b984dfc864df48d5884a4cf0cd7d5453"
    key = "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"

    message = Mail(from_email = FROM_EMAIL,
    to_emails= user_email)

    message.dynamic_template_data = {
        'verify_url': 'http://127.0.0.1:5000/',
        'name': user_name
    }
    
    message.template_id = TEMPLATE_ID

    try:
        sg = SendGridAPIClient(key)
        response = sg.send(message)
        code, body, headers = response.status_code, response.body, response.headers
        print(f"Response code: {code}")
        print(f"Response headers: {headers}")
        print(f"Response body: {body}")
        print("Dynamic Messages Sent!")
    except Exception as e:
        print(e)