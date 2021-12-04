import subprocess
import uuid
import django
django.setup()
from .models import SubmissionCode


def create_code_file(code, language):
    # uuid4 will be unique always
    file_name = str(uuid.uuid4()) + "." + language.lower()

    with open("code/" + file_name, "w") as f:
        f.write(code)

    return file_name


def execute_file(filename, language, submission_id):
    submission = SubmissionCode.objects.get(pk=submission_id)
    if language == "py":
        result = subprocess.run(["python", "./code/" + filename], stdout=subprocess.PIPE)
        if result.returncode != 0:
            # runtime error
            submission.status = "E"
            submission.save()
            return
        submission.user_output = result.stdout.decode("utf-8").strip()
        submission.status = "S"
        submission.save()

