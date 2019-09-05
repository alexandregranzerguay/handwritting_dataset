from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateEntry
import glob, os

ENDPOINT = "https://southcentralus.api.cognitive.microsoft.com/"

training_key = "c53d96b6b2c14ae6b9b0f4a4bfabf386"
prediction_key = "c53d96b6b2c14ae6b9b0f4a4bfabf386"
prediction_resource_id = "/subscriptions/50b8feba-a0e3-44d5-ae45-52321efa4e26/resourceGroups/DA-rg-custom-vision-03/providers/Microsoft.CognitiveServices/accounts/da-custom-vision-03"
project_id = "4ba975a8-185b-4288-b3c6-d8ec34404da3"

publish_iteration_name = "da-custom-vision-test"

trainer = CustomVisionTrainingClient(training_key, endpoint=ENDPOINT)

# Make two tags in the new project
notes_tag = trainer.create_tag(project_id, "Note")
memo_tag = trainer.create_tag(project_id, "Memo")
news_tag = trainer.create_tag(project_id, "News")
resume_tag = trainer.create_tag(project_id, "Resume")
email_tag = trainer.create_tag(project_id, "Email")
report_tag = trainer.create_tag(project_id, "Report")


tags = [notes_tag, memo_tag, news_tag, report_tag, resume_tag, email_tag]

#Add Images

print("Adding images...")
for tag in tags:
    image_list = []
    print("tag name: ",tag.name)
    base_image_url = "./" + tag.name + "/training/"
    count = 0
    for image_path in glob.glob(base_image_url + '*.jpg'):
        if count == 63:
            break
        count += 1
        path, file_name = os.path.split(image_path)
        # path = path/to/file
        # filename = foobar.txt
        with open(image_path, "rb") as image_contents:
            image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), tag_ids=[tag.id]))
    print("Uploading new batch of images")
    upload_result = trainer.create_images_from_files(project_id, images=image_list)
    if not upload_result.is_batch_successful:
        print("Image batch upload failed.")
        for image in upload_result.images:
            print("Image status: ", image.status)
        exit(-1)
    print("Upload batch successful")


import time

print ("Training...")
iteration = trainer.train_project(project_id)
while (iteration.status != "Completed"):
    iteration = trainer.get_iteration(project_id, iteration.id)
    print ("Training status: " + iteration.status)
    time.sleep(1)

# The iteration is now trained. Publish it to the project endpoint
trainer.publish_iteration(project_id, iteration.id, publish_iteration_name, prediction_resource_id)
print ("Done!")