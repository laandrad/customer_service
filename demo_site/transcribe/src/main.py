import argparse
from audio_utils import Audio
from transcriber import Transcriber

parser = argparse.ArgumentParser()
parser.add_argument('soundfile', type=str)
parser.add_argument('-r', '--record',
                    action='store',
                    required=False,
                    type=int)
parser.add_argument('-t', '--transcribe',
                    action='store_true',
                    required=False)

if __name__ == "__main__":
    args = parser.parse_args()
    filename = f'./data/{args.soundfile}'
    if args.record:
        print(f'record {args.soundfile} for {args.record} seconds')
        audio = Audio()
        audio.record(filename, args.record)
    elif args.transcribe:
        print(f'transcribing sound file: {args.soundfile}')
        transcriber = Transcriber()
        transcriber.transcribe(filename)
    else:
        print(f'this will play sound file: {args.soundfile}')
        audio = Audio()
        audio.play(filename)

