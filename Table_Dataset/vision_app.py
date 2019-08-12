from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateEntry
import glob, os

ENDPOINT = "https://southcentralus.api.cognitive.microsoft.com/"

training_key = "27891bb13a064eea9d748e02a3c26603"
prediction_key = "27891bb13a064eea9d748e02a3c26603"
prediction_resource_id = "/subscriptions/10f63f4d-59f8-4014-8bc1-3a84a37c2b20/resourceGroups/foggyforestrg/providers/Microsoft.CognitiveServices/accounts/foggyforestrg_prediction"
project_id = "d960a2df-49ea-48d6-a5c4-198438938c80"

publish_iteration_name = "classifyModel"

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

    for image_path in glob.glob(base_image_url + '*.jpg'):
        path, file_name = os.path.split(image_path)
        # path = path/to/file
        # filename = foobar.txt
        with open(image_path, "rb") as image_contents:
            image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), tag_ids=[tag.id]))
    print("Uploading new batch of images")
    print(image_list==[])
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