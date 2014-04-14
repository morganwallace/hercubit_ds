import device
from time import sleep
from peak_detect2 import peakdetect


def peak_found(maxtab,mintab):
	print maxtab
	print mintab
	pass

def test_live_peaks():
	'''run peak detection on device stream or archive data'''
	from device import sensor_stream
	gen=sensor_stream()
	data=[]
	t=[]
	x=[]
	y=[]
	z=[]
	lookahead=10
	first=True
	#iterate through the device stream (or archive data)
	while True:
		#get rid of the first value sent from the device, it's usually bogus
		if first==True: 
			gen.next()
			first=False
			
		sample=gen.next()
		print sample
		#go until the device data runs out
		if sample!=None:
			data.append(sample)
			for sample in data:
				#time - (considered the 'x' axis in peak detection function)
				t.append(sample['time'])

				x.append(sample['accel'][0])
				y.append(sample['accel'][1])
				z.append(sample['accel'][2])


				#for each axis x,y, and z, look for peaks
				peaks={}
				peaks['x']=peakdetect(x,t,lookahead=lookahead)
				peaks['y']=peakdetect(y,t,lookahead=lookahead)
				peaks['z']=peakdetect(z,t,lookahead=lookahead)

				# dom_axis=''
				# if dom_axis=='':
				#wait until min an max both have values for all three axes
				test=sum([1 for i in peaks.values() if i[0]!=[] and i[1]!=[]])
				for i in peaks:
					if peaks[i]!=([],[]): print i+": "+ str(peaks[i])
				print peaks
				#find longest range
				big_range=0
				if test==6: #completed peak
					print peaks
					for axis in peaks:
						r=abs(peaks[axis][0][1]-peaks[axis][1][1])
						if r > big_range: 
							big_range=r
							dom_axis=axis
				# else:

				#peaks found


				# for axis in peaks:
				# 	if peaks[axis]!=([], []):
				# 		print axis + str(peaks[axis])
						
						#psuedocode
						#wait until min an max both have values for all three axes
						#take the axis with the longest range to be the indicative one


			    # if peaks[0] != [] and peaks[1]!=[]: #Peaks found
			    #     print str(peaks)
			    #     peaks=[[],[]]
			    #     del data[:-1*lookahead/2]
			    #     break
	            
if __name__ == '__main__':
	test_live_peaks()