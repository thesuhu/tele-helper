import requests


def verify_email(email, api_key):
    url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={api_key}"
    response = requests.get(url).json()
    # print(response)
    return response

# python -c "from scripts.email import verify_email; print(verify_email('thesuhu@protonmail', '<api key>'))"
