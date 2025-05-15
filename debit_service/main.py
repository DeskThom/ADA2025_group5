import functions_framework
from flask import Flask, request

@functions_framework.http
def debit_money(request):
    request_json = request.get_json(silent=True)
    
    if not request_json or 'iban' not in request_json or 'amount' not in request_json:
        return "Missing 'iban' or 'amount' in request body", 400

    iban = request_json['iban']
    amount = request_json['amount']
    
    print(f"Debiting {amount} from account {iban}")
    return {
        "message": f"Successfully debited {amount} from account {iban}",
        "status": "success"
    }, 200  # Simulate success

# gcloud functions deploy debit-money --entry-point debit_money --region us-central1 --allow-unauthenticated --runtime python313 --gen2 --trigger-http