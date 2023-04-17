from faas_count import get_images_count

def handle(req):
    response = get_images_count()
    return {
        "status": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": response
    }
