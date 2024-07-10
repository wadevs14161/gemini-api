import requests

def upload_audio(url):
    upload_url = url

    file_path = "tts.mp3"

    with open(file_path, 'rb') as f:
        files = {'file': (f.name, f, 'audio/mpeg')}  # Include content type
        headers = {'Content-Type': 'audio/mpeg'}  # Set content type header

        response = requests.put(url, files=files, headers=headers)

        if response.status_code == 200:
            print("MP3 uploaded successfully!")
            return response.url
        else:
            print(f"Error uploading MP3: {response.status_code}")
            print(response.text)
