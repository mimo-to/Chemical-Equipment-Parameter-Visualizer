API_DOCUMENTATION = """
POST /api/login/
    Request: {"username": str, "password": str}
    Response: {"token": str, "user_id": int, "username": str}

POST /api/upload/
    Headers: Authorization: Token <token>
    Request: FormData with 'file' (CSV)
    Response: EquipmentDatasetSerializer

GET /api/history/
    Headers: Authorization: Token <token>
    Response: List[EquipmentDatasetSerializer]

GET /api/dataset/<id>/
    Headers: Authorization: Token <token>
    Response: EquipmentDatasetSerializer

GET /api/dataset/<id>/visualization/
    Headers: Authorization: Token <token>
    Response: {type_distribution: {labels, data}, averages: {labels, data}}

GET /api/report/<id>/
    Headers: Authorization: Token <token>
    Response: PDF file (application/pdf)
"""
