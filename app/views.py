from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer
from IPython.display import Audio
import vlc

from django.shortcuts import render
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL = "tts_models/en/ljspeech/tacotron2-DDC"

def index(request):
    if request.method == 'POST':
        action = request.POST['meaning']

        manager = ModelManager()
        model_path, config_path, model_item = manager.download_model(MODEL)
        synthesizer = Synthesizer(
            model_path, config_path)
        wavs = synthesizer.tts(action)
        obj = Audio(wavs, rate=synthesizer.output_sample_rate, autoplay=True)

        with open('media/file.wav', 'wb') as f:
            f.write(obj.data)
            context = {"file": True}
        path = ''.join(("file://", str(BASE_DIR), '/media', "/file.wav"))
        p = vlc.MediaPlayer(path)
        p.play()

        return render(request, 'app/index.html', context=context)
    else:
        context = {"file": ""}
        return render(request, 'app/index.html', context=context)