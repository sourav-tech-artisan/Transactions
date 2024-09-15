import uuid
INVALID_CREATION_DATA = [
    {
        "amount": "invalid_data",
        "transaction_type": "New test transaction",
    },
    {
        "amount": 200,
        "transaction_type": "New test transaction",
        "parent_transaction": "invalid_id"
    },
    {
        "amount": -100,
        "transaction_type": "New test transaction",
    },
    {
        "transaction_type": "New test transaction",
    },
    {
        "amount": 200,
    },
    {
        "amount": 200,
        "transaction_type": "New test transaction",
        "parent_transaction": str(uuid.uuid4())
    }
]