from django.shortcuts import render, redirect
from googletrans import LANGUAGES, Translator
import gtts
import os
import tempfile
import speech_recognition as sr
import playsound

def translate(request):
    if request.method == 'POST':
        # Handle the form submission
        source_language = request.POST.get('source_language')
        target_language = request.POST.get('target_language')

        # Create a temporary directory for audio files
        with tempfile.TemporaryDirectory() as temp_dir:
            audio_source = os.path.join(temp_dir, 'audio.wav')
            translated_audio = os.path.join(temp_dir, 'translated.mp3')

            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                print("Speak Now")
                recognizer.adjust_for_ambient_noise(source)
                voice = recognizer.listen(source)
                text = recognizer.recognize_google(voice, language=source_language)
                print("Recognized Text:", text)

            translator = Translator()
            translation = translator.translate(text, src=source_language, dest=target_language)
            translated_text = translation.text
            print("Translated Text:", translated_text)

            # Convert translated text to speech
            tts = gtts.gTTS(translated_text, lang=target_language)
            tts.save(translated_audio)

            # Play the translated audio
            playsound.playsound(translated_audio)

        # Pass the recognized and translated text to the template
        return render(request, "index.html", {'recognized_text': text, 'translated_text': translated_text})

    # If it's a GET request or there's no form submission, render the initial page
    language_choices = list(LANGUAGES.keys())
    return render(request, "index.html", {'languages': language_choices})
