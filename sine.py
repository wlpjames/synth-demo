
import pyaudio
import numpy as np
from scipy import signal as sig
import pdb
import time
import cmath
import matplotlib.pyplot as plot
from timeit import default_timer as timer
from scipy.fftpack import rfft, irfft, fftfreq, fft

import cylowPass
import sineGen
import tape_delay
import env
#import pygame
#import funtools

"""
def main():
	bs = 44100
	master = masterOut()
	
	master.addChannel()
	master.channels[0].addWave(890, vol = .15, waveType = "sine")
	master.channels[0].addWave(440, vol = .6, waveType = "sine")
	master.channels[0].addWave(110, vol = 6, waveType = "sine")
	#self, freq, control, , controlObj, BufferSize, waveType = "sine", MinVal = 0 , MaxVal = 1
	master.channels[0].addWave(1760, vol = 0.1, waveType = "sine")
	master.channels[0].addWave(523.2)
	master.channels[0].addWave(261.6)
	master.channels[0].addWave(783.99, vol = .1, waveType = "sine")	
	master.channels[0].addWave(391.995, vol = .1, waveType = "sine")	
	master.channels[0].addWave(329.6276, vol = .3, waveType = "sine")
	#self, freq, control, , controlObj, BufferSize, waveType = "sine", MinVal = 0 , MaxVal = 1
	

	
	
	
	#av, al, dl, sv, sl, rl
	master.channels[0].FX.append(env.env(1, 0.01, 0.1, 0.6, 0.23, 0.05, 1.5, BS = bs, FPS = 44100))

	#Band_Len, Delay, Mix = 0.5, Fade = 2
	
	#master.channels[0].FX.append(echo(44100, 0.5, 7, BuffSize = bs, FPS = 44100))
	master.channels[0].FX.append(tape_delay.tape(15000, 0.2, Decay = 0.4, BuffSize = bs, FPS = 44100))
	master.channels[0].FX.append(tape_delay.tape(44100, 0.5, Decay = 0.3, BuffSize = bs, FPS = 44100))
	
	#master.channels[0].FX.append(smpl_flt(3, master.bufferSize, Reps = 1))
	
	master.channels[0].staticConts.append(LFO(0.8, master.channels[0].FX[3].updatebeta,
									  master.channels[0].FX[0],
									  bs, MaxVal = .2, MinVal = 0.15, waveType = "sine"))
	
	master.channels[0].staticConts.append(LFO(5, master.channels[0].inputs[1].updateFreq,
										  master.channels[0].inputs[0],
										  bs, MaxVal = 455, MinVal = 425, waveType = "sine"))
	
	master.channels[0].staticConts.append(LFO(.03, master.channels[0].staticConts[0].wave.updateFreq,
										  master.channels[0].staticConts[0].wave,
										  bs, MaxVal = 1, MinVal = .5, waveType = "sine"))
	
	
	
	
	master.channels[0].addWave(261.6)
	master.channels[0].addWave(391.995, vol = .6, waveType = "sine")	
	master.channels[0].addWave(329.6276, vol = .55, waveType = "sine")
	
	
	master.addChannel(vol = .6)


	master.channels[1].FX.append(env.env(1, 0.28, 0.1, 0.65, 0.2, 0.15, 0.9, BS = bs, FPS = 44100))
	master.channels[1].addWave(329.6276, vol = .2, waveType = "sine")
	#master.channels[1].inputs[0].setGlide(0.1)
	master.channels[1].addWave(220, vol = .5, waveType = "sine")
	master.channels[1].addWave(110, vol = 1, waveType = "sine")
	master.channels[1].addWave(55, vol = 1, waveType = "sine")

	#master.channels[1].inputs[1].setGlide(-0.1)

	master.channels[1].FX.append(tape_delay.tape(7, 0.5, Decay = 0.45, BuffSize = bs, FPS = 44100))
	master.channels[1].FX.append(tape_delay.tape(10000, 0.5, Decay = 0.4, BuffSize = bs, FPS = 44100))
	#a = master.sing_call()
	#master.playOutStream()
"""

class masterOut:
	def __init__(self, BS):

		self.channels = []
		self.channelsNum = 0
		self.masterVol = 0.1
		self.setVol = .0

		self.sampleRate = 44100
		self.bufferSize = BS
		self.stream = None
		self.p = None
		
	def getSlice(self, fc):

		data = combineInputs(self.channels, fc)
		return data

	def bootStream(self): # pyaidio
		#open pyaudio
		self.p = pyaudio.PyAudio()

		#prepare stream
		self.stream = self.p.open(format=pyaudio.paFloat32,
    	            channels=1,
        	        rate=self.sampleRate,
            	    output=True,
            	    stream_callback=callback_maker(self),
            	    frames_per_buffer=self.bufferSize
            	    )
		
		# start the stream (4)		
		#self.stream.start_stream()
		

		# wait for stream to finish (5)
		"""
		while self.stream.is_active():
			time.sleep(0.1)
		"""
		

	def closeStream(self):
		#shut everything down nicely
		
		self.stream.close()
		self.p.terminate()

	def play(self):
		self.setVol = self.masterVol

	def pause(self):
		self.setVol = 0
		#self.stream.stop_stream()

	def setVolume(self, val):
		#print(val -1 100)
		self.masterVol = val

		if self.setVol > 0:
			self.setVol = val




	def sing_call(self):
		a = callback_maker(self)
		a(0,self.bufferSize ,0,0,)


	def addChannel(self, vol = 1):
		self.channels += [channel(self.bufferSize, vol)]
		self.channelsNum += 1

	
def callback_maker(master):
	
	def callback(in_data, frame_count, time_info, status):
		start = timer()
		data = master.getSlice(frame_count).astype(np.float32)
		end = timer()
		#print("per-buffer total speed =" + str(end - start))
		#plot.plot(np.arange(0, frame_count, 1), data)
		#plot.show()
		#print("between frames!")
		return (data*master.setVol, pyaudio.paContinue)

	return callback







class channel:

	def __init__(self, BS, vol = 1):

		self.inputs = []
		self.staticConts = []
		self.FX = []
		self.bufferSize = BS
		self.volume = vol

	def nextFrame(self):
		self.runStatics()
		
		signal = combineInputs(self.inputs, self.bufferSize)
		signal = self.runFX(signal)

		return self.volume * signal

	def addWave(self, frequency, waveType = "sine", vol = .75):
		#self.inputs += [waveGen(frequency, self.bufferSize, waveType, vol)]
		self.inputs += [sineGen.WaveGen(frequency, self.bufferSize, waveType, vol, 44100)]

	def addChannel(self):
		self.inputs += [channel(self.bufferSize, self.volume)]

	def runStatics(self):
		for i in range(len(self.staticConts)):
			self.staticConts[i].executePerBuffer()

	def runFX(self, signal):
		
		#plot.plot(np.arange(0, self.bufferSize, 1), signal)
		for i in range(len(self.FX)):
			signal = self.FX[i].execute(signal.astype(np.float32))
			#print("band len = ", len(self.band))
		#plot.plot(np.arange(0, self.bufferSize, 1), signal/2)
		#plot.show()
		return signal







class waveGen:
	
	def __init__(self, freq, BufferSize, waveType, vol):
		
		self.sampleRate = 44100
		self.bufferSize = BufferSize
		self.buffer = np.empty(BufferSize, dtype=np.complex)
		self.frequency = freq
		self.omega = 0
		self.updateOmega()
		self.last = complex(1,0)
		self.type = waveType
		self.volume = vol

		self.adjCount = 0
		self.adjLim = 1000
		
		#vals for glider
		self.isGliding = False
		self.glideVal = 0
		self.originalFreq = self.frequency

	def sineGen(self):

		#start = timer() #reduce function!!! functools
		for i in range(0, self.bufferSize):
			self.buffer[i] = self.last
			self.last=self.last*self.omega

			"""
			#adjust
			if self.adjCount > self.adjLim:
				print ("adjusting")
				a = np.real(self.last)
				b = np.imag(self.last)
				c = (3 - pow(a, 2) - pow(b, 2)) / 2
				self.last = self.last * complex(c, 0)
				self.adjCount = 0
		
			self.adjCount += 1

			"""
		#functools.reduce(lambda a,b : a+b,lis) #for a,b : b = a * self.omega
		#end = timer()
		#print("sineWave speed =" + str(end - start))
		self.glide()
		return self.volume * np.imag(self.buffer).astype(np.float32)

	def squareGen(self):
		#start = timer()
		for i in range(0, self.bufferSize):
			self.buffer[i] = np.sign(self.last)
			self.last=self.last*self.omega
			
		#end = timer()
		#print("squareWave speed =" + str(end - start))
		#plot.plot(np.arange(0, self.bufferSize, 1), self.buffer)
		self.glide()
		return np.real(self.volume * self.buffer).astype(np.float32)

	def triangleGen(self):
		#todo
		return self.buffer

	def glide(self): 
			
		if (self.isGliding == True 
				and self.frequency < self.originalFreq*2 
					and self.frequency > 0-(self.originalFreq/3)*2):
			
			self.frequency += self.glideVal
			self.updateOmega()

	def setGlide(self, val):
		self.isGliding = True
		self.glideVal = val

	def updateOmega(self):
		self.omega = cmath.exp(1j*(2*cmath.pi * self.frequency / self.sampleRate))

	def updateFreq(self, val):
		self.frequency = val
		self.updateOmega()

	def nextFrame(self):
		if self.type == "sine":
			return self.sineGen()
		elif self.type == "square":
			return self.squareGen()
		elif self.type == "triangle":
			return self.triangleGen()




def combineInputs(inputs, fc):
	
	#create silent array
	slices = np.zeros(fc, dtype=np.float32)
	#add the output from each channel to array
	for i in range(len(inputs)):
		slices = np.add(slices, inputs[i].nextFrame())

	#plot.plot(np.arange(0, fc, 1), slices)

	return slices




class LFO:
	#a class of object that directly controls a source, source can be any value

	def __init__(self, freq, control, controlObj, BufferSize, waveType = "sine", MinVal = 0 , MaxVal = 1):

		self.frequency = freq
		self.maxVal = MaxVal
		self.minVal = MinVal
		self.bufferSize = BufferSize

		#a slow wave to control input
		self.wave_Type = waveType
		self.wave = sineGen.WaveGen(self.frequency, self.bufferSize, self.wave_Type, 1, 44100)
		#self.wave = sineGen.WaveGen(freq, self.bufferSize, waveType, 1, 44100)

		#associated with another waveGen

		#pointer to the control function
		self.output = []
		self.output.append(control)

		self.controlObjs = []
		self.controlObjs.append(controlObj)

	def executePerBuffer(self):
		#sets the control to last point of self.wave
		nextFrame = self.wave.nextFrame()

		#between 0 and 1
		lastVal = (nextFrame[self.bufferSize-1] + 1) / 2



		#print("lfo Val = " + str(lastVal))

		val = (lastVal*(self.maxVal-self.minVal)) + self.minVal 
		#print("new freq Val = " + str(val))
		#the value of the thing pointed to here becomes set.
		self.output[0](val)


	#def executePerSample():
		#sets the frequency of the next sample in self.wave




