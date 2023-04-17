from pymongo import MongoClient

def get_images_count():
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    # Access the database and collection
    db = client["myimagedatabase"]
    images = db["images"]
    # Get the count of images
    count = images.count_documents({})
    # Return the count as a dictionary
    return {"count": count}