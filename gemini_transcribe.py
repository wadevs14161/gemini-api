import os, tempfile
from google.cloud import speech

def transcribe(audio):

    # audio is _io.BytesIO object    
    
    with tempfile.NamedTemporaryFile(suffix=".webm", delete=True) as tmp_file:
        # Save the audio file to the temporary file
        tmp_file.write(audio.read())

        tmp_file.flush()
        with open(tmp_file.name, "rb") as file_for_transcription:
            content = file_for_transcription.read()

            # Save the audio file to the local directory
            with open('static/audio/test.webm', 'wb+') as destination:
                destination.write(audio.read())
            

                #setting Google credential
                os.environ['GOOGLE_APPLICATION_CREDENTIALS']= 'google_secret_key.json'
                # create client instance 
                client = speech.SpeechClient()

                audio = speech.RecognitionAudio(content=content)

                config = speech.RecognitionConfig(
                    enable_automatic_punctuation=True,
                    # audio_channel_count=2,
                    language_code="en-US",
                    alternative_language_codes=["zh-TW", "es", "ja"],
                )

                # Sends the request to google to transcribe the audio
                response = client.recognize(request={"config": config, "audio": audio})
                
                # print(response)
                # print(response.results)

                transcript = ". ".join([result.alternatives[0].transcript for result in response.results])
                print(transcript)

                context = {
                    'transcript': transcript,
                }

                return context
