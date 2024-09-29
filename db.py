from pymongo import MongoClient
from bson import ObjectId
import datetime
from datetime import datetime

# Initialize MongoDB client
dbconnection = MongoClient('mongodb://localhost:27017/')
db = dbconnection['enterprise']  # Replace with your database name
# Workshops Collection
workshop_id = ObjectId()
db.workshops.insert_one({
    "_id": workshop_id,
    "name": "Main Workshop",
    "staff": [
        { "name": "John Doe", "position": "Engineer" },
        { "name": "Jane Smith", "position": "Technician" }
    ],
    "sections": [
        {
            "name": "Assembly",
            "chief": "Alice Johnson"
        },
        {
            "name": "Testing",
            "chief": "Bob Brown"
        }
    ]
})

# Insert sample data into Products collection
product_a_id = ObjectId()
product_b_id = ObjectId()
db.products.insert_many([
    {
        "_id": product_a_id,
        "name": "Product A",
        "workshop_id": workshop_id,
        "date": datetime(2024, 1, 1),
        "test_date": datetime(2024, 1, 15)
    },
    {
        "_id": product_b_id,
        "name": "Product B",
        "workshop_id": workshop_id,
        "date": datetime(2024, 2, 1),
        "test_date": datetime(2024, 2, 15)
    }
])

# Insert sample data into Laboratories collection
db.laboratories.insert_one({
    "_id": ObjectId(),
    "name": "Lab A",
    "tests": [
        { "product_id": product_a_id },
        { "product_id": product_b_id }
    ]
})

# Insert sample data into Works collection
db.works.insert_one({
    "_id": ObjectId(),
    "product_id": product_a_id,
    "description": "Assembly process"
})

# Insert sample data into Equipment collection
db.equipment.insert_one({
    "_id": ObjectId(),
    "name": "Equipment A",
    "tests": [
        { "product_id": product_a_id }
    ]
})

# Insert sample data into Brigades collection
db.brigades.insert_one({
    "_id": ObjectId(),
    "workshop_id": workshop_id,
    "section_id": workshop_id,
    "members": [
        { "name": "Mike Green", "role": "Worker" },
        { "name": "Laura White", "role": "Helper" }
    ]
})

# Insert sample data into Masters collection
db.masters.insert_one({
    "_id": ObjectId(),
    "workshop_id": workshop_id,
    "name": "Frank Black"
})

# Insert sample data into Employees collection
db.employees.insert_one({
    "_id": ObjectId(),
    "tests": [
        { "product_id": product_a_id }
    ],
    "name": "Sara Blue"
})
