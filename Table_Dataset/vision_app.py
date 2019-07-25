from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateEntry
import glob, os

ENDPOINT = "https://southcentralus.api.cognitive.microsoft.com"

training_key = "fff242d0c6c64d49848d62e7bc7ee9f0"
prediction_key = "80baf3ea051a442ab0805892939a7591"
prediction_resource_id = "/subscriptions/a9668ed2-2114-4ab9-8600-c2ca85997b9a/resourceGroups/Growing_Forest/providers/Microsoft.CognitiveServices/accounts/Growing_Forest_prediction"
project_id = "98cfcb17-841d-4b72-a84b-84ec4151f5a2"

publish_iteration_name = "classifyModel"

trainer = CustomVisionTrainingClient(training_key, endpoint=ENDPOINT)

# Make two tags in the new project
notes_tag = trainer.create_tag(project_id, "Notes")
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
    base_image_url = "./" + tag.name + "/training/"

    for image_path in glob.glob(base_image_url + '*.jpg'):
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