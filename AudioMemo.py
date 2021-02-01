
import time as t
from datetime import datetime as dt

import speech_recognition as sr


def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio, language="it-IT")
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


if __name__ == "__main__":

   # create recognizer and mic instances
   recognizer = sr.Recognizer()
   microphone = sr.Microphone()
   t.sleep(3)
   fileName=input('Type the name of the memo: \n')
   fileName+='.txt'
   print('SPEAK TO RECORD YOUR MEMO: \n')
   guess = recognize_speech_from_mic(recognizer, microphone)
   if guess["transcription"]:
       print(guess["transcription"])
       memo = guess["transcription"]
       print('SAVING MEMO...\n')
       #fileName = 'Memo_'+dt.now().strftime("%d-%m-%Y_%H-%M-%S")+'.txt'
       with open(fileName, "w") as text_file:
          text_file.write(memo)
       print('SAVE COMPLETED: '+fileName)
   if not guess["success"]:
      print("I DID NOT UNDERSTAND WHAT YOU SAID :( \n")
