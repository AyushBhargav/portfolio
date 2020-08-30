import os, shutil, subprocess
from datetime import datetime


def executeAndAbortIfError(process, fail_msg):
    return_code = -1
    while True:
        output = process.stdout.readline()
        print(output.strip())
        # Do something else
        return_code = process.poll()
        if return_code is not None:
            print('RETURN CODE', return_code)
            # Process has finished, read rest of the output 
            for output in process.stdout.readlines():
                print(output.strip())
            break

    if return_code != 0:
        print("Git add failed. Aborting")
        exit(0)


executeAndAbortIfError(subprocess.Popen('ng build --prod',
                    shell=True,
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    universal_newlines=True), "'ng build' failed. Aborting")

# Clear the destination
dest_folder = '../ayushbhargav.github.io'
for filename in os.listdir(dest_folder):
    file_path = os.path.join(dest_folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            print("Deleting file:" + file_path)
            os.unlink(file_path)
        elif os.path.isdir(file_path) and (".git" not in file_path):
            print("Deleting folder:" + file_path)
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

# Copy bundled files to destination.
src_folder = 'dist/Portfolio'
for filename in os.listdir(src_folder):
    print("Copying files: " + filename)
    shutil.copy(os.path.join(src_folder, filename), dest_folder)


# Moving code to staging.
cmd = subprocess.run('git add .')
executeAndAbortIfError(subprocess.Popen('git add .', 
                    shell=True,
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                    cwd=dest_folder), "'git add' failed. Aborting")

# Committing code
today = datetime.now()
message = "Automated commit: " + today.strftime("%d/%m/%Y %H:%M:%S")
executeAndAbortIfError(subprocess.Popen('git commit -m "{message}"'.format(message=message), 
                    shell=True,
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                    cwd=dest_folder), "'git commit' failed. Aborting")

# Pushing to remote
executeAndAbortIfError(subprocess.Popen('git push origin master', 
                    shell=True,
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                    cwd=dest_folder), "'git push' failed. Aborting")

print("Process has now completed. Don't forget to give regards to monty python.")