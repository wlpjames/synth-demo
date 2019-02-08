import sys
from PyQt4 import QtGui
from synthGui import Ui_MainWindow 

import sine
import cylowPass
import sineGen
import env
import tape_delay

class MyWindow(QtGui.QMainWindow):
	def __init__(self):
		super(MyWindow, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.master = None
		self.playing = False
		self.buildAudio()


		self.show()
	
	def buildAudio(self):
		bs = 63
		self.master = sine.masterOut(bs)

		#first channel
		self.master.addChannel()
		self.master.channels[0].FX.append(cylowPass.smpl_flt(1, bs, Reps = 1, Gain = .2, Res = 1.2))
		self.master.channels[0].FX.append(env.env(1, 0.01, 0.1, 0.6, 0.23, 0.05, 1.5, BS = bs, FPS = 44100))
		self.master.channels[0].FX.append(tape_delay.tape(20000, 0.5, Decay = .3, BuffSize = bs, FPS = 44100))
		

		#chan 1.1
		self.master.channels[0].addChannel()
		self.master.channels[0].inputs[0].FX.append(cylowPass.smpl_flt(1, bs, Reps = 1, Gain = .2, Res = 1.2))
		self.master.channels[0].inputs[0].addWave(440, vol = .5, waveType = "sine")
		self.master.channels[0].inputs[0].addWave(440, vol = .5, waveType = "sine")


		#chan 1.2
		self.master.channels[0].addChannel()

		self.master.channels[0].inputs[1].addWave(110, vol = .5, waveType = "triangle")
		self.master.channels[0].inputs[1].addWave(390, vol = .5, waveType = "saw")

		#this has to be in other thread!!!.
		#need boot stream function
		#start stream function
		#stop stream function

		#LFO attacted to master chan
		
		self.master.channels[0].staticConts.append(sine.LFO(2, self.master.channels[0].FX[0].updatebeta,
									  self.master.channels[0].FX[0],
									  bs, MaxVal = 1, MinVal = 0.15, waveType = "sine"))
		
		self.master.channels[0].staticConts.append(sine.LFO(7, self.master.channels[0].inputs[0].inputs[0].fineTune,
										  self.master.channels[0].inputs[0],
										  bs, MaxVal = 440, MinVal = 430, waveType = "sine"))
		

		self.master.bootStream()
		



	#master
	def play(self, val):

		if self.playing == False:
			self.playing = True
		else:
			self.playing = False
		if self.playing == True:
			
			#set evn to beggining

			self.master.play()
		else:
			self.master.pause()		
	
	#missing stop

	def masterVol(self, val):

		self.master.setVolume(float(val) / 1000)
		

	#echo
	def echoDecay(self, val):
		self.master.channels[0].FX[2].setDecay(float(val)/100)

	def echoDelay(self, val):
		#val twix 0 and 99
		#to be set betwixt 0 and 2 sec
		#divide by 50 for secs val
		#times by bs for samples

		#big issues here!!!
		#skipping for now
		self.master.channels[0].FX[2].setBand_len(((val+1) * 44100) // 50)
		

	def echoMix(self, val):
		self.master.channels[0].FX[2].setMix(float(val)/100)
		

	#osc1
	def osc1Fine(self, val):
		self.master.channels[0].inputs[0].inputs[0].fineTune(val)

	def osc1Type(self, val):
		self.master.channels[0].inputs[0].inputs[0].setType(val)
		
	def osc1Vol(self, val):
		self.master.channels[0].inputs[0].inputs[0].setVol(float(val)/100)
		
		
		

	#osc2
	def osc2Vol(self, val):
		self.master.channels[0].inputs[0].inputs[1].setVol(float(val)/100)

	def osc2Fine(self, val):
		self.master.channels[0].inputs[0].inputs[1].fineTune(val)

	def osc2Type(self, val):
		self.master.channels[0].inputs[0].inputs[1].setType(val)

	#missing type

	#osc3
	def osc3Fine(self, val):
		self.master.channels[0].inputs[1].inputs[0].fineTune(val)

	def osc3Vol(self, val):
		self.master.channels[0].inputs[1].inputs[0].setVol(float(val)/100)

	def osc3Type(self, val):
		self.master.channels[0].inputs[1].inputs[0].setType(val)

	#missing type

	#osc4
	def osc4Fine(self, val):
		self.master.channels[0].inputs[1].inputs[1].fineTune(val)

	def osc4Vol(self, val):
		self.master.channels[0].inputs[1].inputs[1].setVol(float(val)/100)

	def osc4Type(self, val):
		self.master.channels[0].inputs[1].inputs[1].setType(val)

	#missing type

	#env
	def A(self, val):
		self.master.channels[0].FX[1].setA(float(val)/300)

	def D(self, val):
		self.master.channels[0].FX[1].setD(float(val)/300)

	def V(self, val):
		self.master.channels[0].FX[1].setV(float(val)/300)

	def S(self, val):
		self.master.channels[0].FX[1].setS(float(val)/300)

	def R(self, val):
		self.master.channels[0].FX[1].setR(float(val)/300)

	def P(self, val):
		self.master.channels[0].FX[1].setP(float(val)/50)

	#filter1
	def filter1Cut(self, val):
		self.master.channels[0].inputs[0].FX[0].updatebeta(float(val)/100)
		

	def filter1Angle(self, val):
		self.master.channels[0].inputs[0].FX[0].updateReps((float(val)/10) + 1)

	#filter2
	def filter2Cut(self, val):
		self.master.channels[0].FX[0].updatebeta(float(val)/100)

	def filter2Angle(self, val):
		self.master.channels[0].FX[0].updateReps((float(val)/10) + 1)

	#lfo1

	#missing all

	#lfo2

	#missing all

	#crossfade1

	#crossfade2






def main():
	app = QtGui.QApplication(sys.argv)
	window = MyWindow()
	app.exec_()

if __name__ == "__main__":
	main()