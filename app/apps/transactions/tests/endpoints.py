from app.settings import  BASE_URL
CREATE_TRANSACTION_URL = f"{BASE_URL}/transactions/"
LIST_TRANSACTION_URL = f"{BASE_URL}/transactions/"
RETRIEVE_TRANSACTION_URL = f"{BASE_URL}/transactions/{{transaction_id}}/"
UPDATE_TRANSACTION_URL = f"{BASE_URL}/transactions/{{transaction_id}}/"