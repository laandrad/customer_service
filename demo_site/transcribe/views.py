import os
import datetime
from django.shortcuts import render
from .src.audio_utils import Audio
from .src.transcriber import Transcriber
from .models import AudioFile


AUDIO_ROOT = './transcribe/src/data/'


def home(request):
    if 'action' in request.GET:
        if request.GET['action'] == 'record':
            print("I'm recording!")
        elif request.GET['action'] == 'play':
            print("I'm playing!")
        elif request.GET['action'] == 'transcribe':
            print("I'm transcribing!")
    return render(request, 'transcribe/home.html')


def record(request):
    date_time = datetime.datetime.now().strftime(format='%m_%d_%Y_%H:%M')
    filename = f'outfile_{date_time}.wav'
    if 'recording' in request.GET:
        if request.GET['recording'] == 'Start':
            duration = int(request.GET['duration'])
            audio = Audio()
            audio.record(
                filename=os.path.join(AUDIO_ROOT, filename),
                duration=duration,
            )
            audio_file = AudioFile(title=filename)
            audio_file.save()
    return render(request, 'transcribe/record.html')


def play(request):
    audio_files = AudioFile.objects.all()
    context = dict(
        files=audio_files,
    )
    if 'file' in request.GET:
        filename = os.path.join(AUDIO_ROOT, request.GET['file'])
        audio = Audio()
        audio.play(filename)
    return render(request, 'transcribe/play.html', context)


def transcribe(request):
    audio_files = AudioFile.objects.all()
    context = dict(
        files=audio_files,
    )
    if 'file' in request.GET:
        filename = os.path.join(AUDIO_ROOT, request.GET['file'])
        trancriber = Transcriber()
        transcription = trancriber.transcribe(filename)
        context['transcription'] = transcription
    return render(request, 'transcribe/transcribe.html', context)
