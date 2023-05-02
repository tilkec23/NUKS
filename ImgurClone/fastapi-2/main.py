# Import necessary modules
import datetime
import io
import os
from fastapi import FastAPI, File, HTTPException, Header, UploadFile
from pymongo import MongoClient
from bson.objectid import ObjectId
import uuid
from fastapi.responses import StreamingResponse, FileResponse
from pathlib import Path
from PIL import Image
from fastapi.middleware.cors import CORSMiddleware

# Create the FastAPI app instance
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to the MongoDB server
client = MongoClient("mongodb:27017")

# Select the database to use
db = client["myimagedatabase"]

# Select the collection to use
images = db["images"]
images.create_index([("image_id", 1)], unique=True)

# Create an endpoint to handle file uploads
@app.post("/uploadfile/")
async def create_upload_file(title: str, file: UploadFile = File(...)):
    # Extract the file extension from the filename
    extension = file.filename.split(".")[-1]

    # Generate a unique filename using UUID and the file extension
    filename = str(uuid.uuid4()) + "." + extension

    # Open a file in binary write mode and write the file contents to it
    with open(filename, "wb") as f:
        f.write(await file.read())


    # To get width and height
    with open(filename, "rb") as f:
        img_bytes = io.BytesIO(f.read())
    
    image = Image.open(img_bytes)
    width, height = image.size

    # Insert a new document into the MongoDB collection with the file metadata
    image_id = images.count_documents({}) + 1
    images.insert_one({
        "image_id": image_id,
        "title": title,
        "filename": filename,
        "size_MB": os.path.getsize(filename) / (1024 * 1024),
        "height": height,
        "width": width,
        "num_likes": 0,
        "num_dislikes": 0,
        "uploaded_time": datetime.datetime.now(),
        "title_modified": False
    })

    # Return the ID of the new document as a JSON response
    return {"image_id": image_id}

# Create an endpoint to handle image deletions
@app.delete("/images/{image_id}")
async def delete_image(image_id: str):
    # Find the document in the collection with the given ID
    image = images.find_one({"image_id": int(image_id)})

    if image is None:
        return {"message": "Image not found"}
    
    # Delete the image file from disk
    os.remove(image["filename"])

    # Delete the document from the collection
    images.delete_one({"image_id": int(image_id)})

    # Return a success message as a JSON response
    return {"message": "Image deleted"}

# Create an endpoint to handle image updates
@app.patch("/images/{image_id}")
async def update_image_title(image_id: str, new_title: str):
    # Update the document in the collection with the given ID
    images.update_one({"image_id": int(image_id)}, {"$set": {"title": new_title, "title_modified": True}})

    # Return a success message as a JSON response
    return {"message": "Image title updated"}

# Create an endpoint to get an image with a given ID
@app.get("/images/{image_id}")
async def get_image(image_id: str):
    file_extensions = (".png", ".jpg", ".jpeg", ".gif")
    
    image = images.find_one({"image_id": int(image_id)})
    if image:
        # Check if the image file exists
        print("Image yes")
        if Path(image["filename"]).is_file():
            # Check if the file extension is valid
            print("File yes")
            if image["filename"].endswith(file_extensions):
                # Return the image as a StreamingResponse
                return StreamingResponse(open(image["filename"], "rb"), media_type="image/*")
            else:
                raise HTTPException(status_code=415, detail="Unsupported media type")
        else:
            raise HTTPException(status_code=404, detail="Image file not found")
     
    
    
    else:
        raise HTTPException(status_code=404, detail="Image not found")
    
# Create an endpoint that tells how many images are in the database
@app.get("/images_count/")
async def count_images():
    count = images.count_documents({})
    return {"count": count}

# Create an endpoint to get the highest image_id
@app.get("/highest_image_id/")
async def get_highest_image_id():
    highest_id = images.count_documents({})
    return {"highest_id": highest_id}