from pydub import AudioSegment

sound = AudioSegment.from_file("space_laser.mp3",format="mp3")

sound.export("space_laser.wav", format="wav")