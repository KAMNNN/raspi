- Go to the directory "pet"
- Run command "./setup.sh"
- Run command "python upload.py"

Watch the audio test stream get chunked and placed into the "raw" directory.
Meanwhile, the upload thread places files into the "processed" folder.

The process() function will be replaced with an API call to the web server.
