from pymongo import MongoClient
from bson import ObjectId

# Підключення до локальної MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['enterprise']

# Тестові дані для колекції "workshops"
workshops_data = [
    {
        "_id": ObjectId(),
        "name": "Workshop A",
        "sections": [
            {
                "_id": ObjectId(),
                "name": "Section 1",
                "chief": {
                    "name": "John Doe",
                    "position": "Section Chief",
                    "personnel": [
                        {
                            "name": "Jane Smith",
                            "position": "Master",
                            "brigades": [
                                {
                                    "brigadier": "Mark Johnson",
                                    "workers": [
                                        {"name": "Worker 1", "position": "Assembler"},
                                        {"name": "Worker 2", "position": "Turner"}
                                    ]
                                }
                            ]
                        }
                    ]
                }
            }
        ]
    }
]

# Тестові дані для колекції "products"
products_data = [
    {
        "_id": ObjectId(),
        "category": "Civil Aircraft",
        "type": "Passenger Plane",
        "attributes": {
            "engine_count": 2,
            "capacity": 150
        },
        "assembly": {
            "workshop_id": ObjectId(),  # Використовуй реальний _id майстерні
            "sections": [
                {
                    "section_id": ObjectId(),  # Використовуй реальний _id секції
                    "brigade_id": ObjectId(),  # Використовуй реальний _id бригади
                    "start_date": "2024-01-01",
                    "end_date": "2024-02-15"
                }
            ]
        },
        "tests": [
            {
                "lab_id": ObjectId(),  # Використовуй реальний _id лабораторії
                "equipment": ["Equipment A", "Equipment B"],
                "testers": [
                    {"name": "Tester 1"},
                    {"name": "Tester 2"}
                ],
                "date": "2024-03-01"
            }
        ]
    }
]

# Тестові дані для колекції "labs"
labs_data = [
    {
        "_id": ObjectId(),
        "name": "Test Lab 1",
        "workshops_serviced": [ObjectId(), ObjectId()],  # Використовуй реальні _id майстерень
        "equipment": [
            {
                "name": "Equipment A",
                "type": "Pressure Tester",
                "tests": [
                    {
                        "product_id": ObjectId(),  # Використовуй реальний _id продукту
                        "date": "2024-03-01",
                        "testers": [
                            {"name": "Tester 1"},
                            {"name": "Tester 2"}
                        ]
                    }
                ]
            }
        ]
    }
]

# Тестові дані для колекції "personnel"
personnel_data = [
    {
        "_id": ObjectId(),
        "name": "Jane Smith",
        "position": "Master",
        "workshop_id": ObjectId(),  # Використовуй реальний _id майстерні
        "section_id": ObjectId(),  # Використовуй реальний _id секції
        "brigade_id": ObjectId(),  # Використовуй реальний _id бригади
        "category": "Engineering Staff",
        "works_on": [
            {
                "product_id": ObjectId(),  # Використовуй реальний _id продукту
                "role": "Supervisor",
                "start_date": "2024-01-01",
                "end_date": "2024-02-15"
            }
        ]
    }
]

# Вставка даних у відповідні колекції
db.workshops.insert_many(workshops_data)
db.products.insert_many(products_data)
db.labs.insert_many(labs_data)
db.personnel.insert_many(personnel_data)

print("Дані успішно вставлені в базу даних.")
