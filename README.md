# IMGUR CLONE-ish

## 1. This is an IMGUR CLONE, an online server based image gallery.

Here you can upload photos using the upload at the top left of the page on the IP provided privately. You can also use one of the many API endpoints in order to use the functionalities in that are the following:

### I. delete_image  -->  /uploadfile/    [POST]
Is the API endpoint for the create_upload_file function, where the user can upload the file.
### II. delete_image  -->  /images/{image_id}    [DELETE]
Is the API endpoint for the delete_image function, where the user can delete an image given the image ID in the URL.
### III. update_image_title  -->  /images/{image_id}    [PATCH]
Is the API endpoint for the update_image_title function, where the user can update an Image's title given the image ID in the URL.
### IV. get_image  -->  /images/{image_id}    [GET]
Is the API endpoint for the get_image function, where the user can get an Image given the image ID in the URL.
### V. get_all_images  -->  /images/    [GET]
Is the API endpoint for the get_all_images function, where the user can get all of the Images list.
### VI. get_image_title_byimage_id  -->  /images/{image_id}/title    [GET]
Is the API endpoint for the get_image_title_byimage_id function, where the user can get an Image's title using the given image ID in the URL.
### VII. count_images  -->  /images_count/    [GET]
Is the API endpoint for the count_images function, where the user can get the number of all the Images in the database.
### VIII. get_highest_image_id  -->  /highest_image_id/    [GET]
Is the API endpoint for the get_highest_image_id function, where the user can get the ID number of the Image with the highest Image ID.