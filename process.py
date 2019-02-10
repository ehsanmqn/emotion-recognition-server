# Call syntax:
#   python3 OpenVokaWavMean-linux64.py path_to_sound_file.wav
#
# For the sound file hello.wav that comes with OpenVokaturi, the result should be:
#	Neutral: 0.760
#	Happy: 0.000
#	Sad: 0.238
#	Angry: 0.001
#	Fear: 0.000

import sys
import scipy.io.wavfile
import Vokaturi
import os
from flask import jsonify

# Load model 1
Vokaturi.load("./emotion-lib-linux64.so")

def voiceSelection(file_name):
	# Reading sound file
	# file_name = sys.argv[1]
	(sample_rate, samples) = scipy.io.wavfile.read(file_name)
	# print ("Sample rate: %.3f Hz" % sample_rate)

	# Allocating sample array
	buffer_length = len(samples)
	# print ("Samples: %d" % (buffer_length))
	# print ("Channels: %d" % (samples.ndim))
	c_buffer = Vokaturi.SampleArrayC(buffer_length)
	if samples.ndim == 1:  # mono
		c_buffer[:] = samples[:] / 32768.0
	else:  # stereo
		c_buffer[:] = 0.5*(samples[:,0]+0.0+samples[:,1]) / 32768.0

	# Creating data structure
	voice = Vokaturi.Voice (sample_rate, buffer_length)
	# Filling data structure with samples
	voice.fill(buffer_length, c_buffer)

	# print ("Extracting emotions...")
	return voice

def model1GetNeutral(voice_Selection):
	quality = Vokaturi.Quality()
	emotionProbabilities = Vokaturi.EmotionProbabilities()
	voiceSelection(voice_Selection).extract(quality, emotionProbabilities)

	if quality.valid:
		print ("Neutral: %.3f" % emotionProbabilities.neutrality)
	else:
		print ("Not enough sonorancy to determine emotions")
	return
def model1GetHappy(voice_Selection):
	quality = Vokaturi.Quality()
	emotionProbabilities = Vokaturi.EmotionProbabilities()
	voiceSelection(voice_Selection).extract(quality, emotionProbabilities)

	if quality.valid:
		print ("Happy: %.3f" % emotionProbabilities.happiness)
	else:
		print ("Not enough sonorancy to determine emotions")
	return
def model1GetSad(voice_Selection):
	quality = Vokaturi.Quality()
	emotionProbabilities = Vokaturi.EmotionProbabilities()
	voiceSelection(voice_Selection).extract(quality, emotionProbabilities)

	if quality.valid:
		print ("Sad: %.3f" % emotionProbabilities.sadness)
	else:
		print ("Not enough sonorancy to determine emotions")
	return
def model1GetAngry(voice_Selection):
	quality = Vokaturi.Quality()
	emotionProbabilities = Vokaturi.EmotionProbabilities()
	voiceSelection(voice_Selection).extract(quality, emotionProbabilities)

	if quality.valid:
		print ("Angry: %.3f" % emotionProbabilities.anger)
	else:
		print ("Not enough sonorancy to determine emotions")
	return

def model1GetFear(voice_Selection):
	quality = Vokaturi.Quality()
	emotionProbabilities = Vokaturi.EmotionProbabilities()
	voiceSelection(voice_Selection).extract(quality, emotionProbabilities)

	if quality.valid:
		print ("Fear: %.3f" % emotionProbabilities.fear)
	else:
		print ("Not enough sonorancy to determine emotions")
	return

def model1GetResult(voice_Selection):
	quality = Vokaturi.Quality()
	emotionProbabilities = Vokaturi.EmotionProbabilities()
	voiceSelection(voice_Selection).extract(quality, emotionProbabilities)

	if quality.valid:
		result_of ={
		"request":"ok",
		"Model": "1",
		"result":[ {
		"Neutral":"%.3f"%emotionProbabilities.neutrality,
		"Happy":"%3f"%emotionProbabilities.happiness,
		"Sad":" %.3f" % emotionProbabilities.sadness,
		"Angry":" %.3f" % emotionProbabilities.anger,
		"Fear":" %.3f" % emotionProbabilities.fear
		}]}
	else:
		result_of={"request":"null", "result":[]}
	return result_of

def model1GetResultForAVA(voice_Selection):
	quality = Vokaturi.Quality()
	emotionProbabilities = Vokaturi.EmotionProbabilities()
	voiceSelection(voice_Selection).extract(quality, emotionProbabilities)

	if quality.valid:
		result_of = "<saba><request>ok</request><model>1</model><result>"
		result_of += "<neutral>{neutral:3f}</neutral><happy>{happy:3f}</happy><sad>{sad:3f}</sad><angry>{angry:3f}</angry><fear>{fear:3f}</fear>".format(neutral=emotionProbabilities.neutrality,
			happy=emotionProbabilities.happiness, 
			sad=emotionProbabilities.sadness,
			angry=emotionProbabilities.anger,
			fear=emotionProbabilities.fear)
		result_of += "</result></saba>"
	else:
		result_of = result_of = "<saba><request>failed</request></saba>"
	return result_of