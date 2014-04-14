import device
import settings

device_data_generator=device.acc_data()
data=[]
peaks=0
prev_slope=0
peak,dip,peak_range=0,0,0
all_reps={"curls":0,"latRaise":0}
reps=0
dominant_axis=3


def get_slope(axis, samples=2):
    """returns the slope of the axis from the 
    second to last point to the current point"""
    global data
    rise=data[-1][axis] - data[-samples][axis] #acc value, for x, i=1;    y, i=2;    z, i=3
    run=data[-1][0] - data[-samples][0] #time change
    return rise/run


def detect_rep():
	global data, peaks, prev_slope, peak, dip, peak_range, all_reps, reps, dominant_axis,device_data_generator
	"""Use changes in slope to find peaks. 
	After a second peak is detected, trigger the rep_event function

	"""

	#ensure list 'data' never gets bigger than the max rep window
	if len(data)*settings.sampleRate>=settings.max_rep_window: 
		del data[0]
	# Fetch accelerometer data
	try:
		sample=device_data_generator.next()
	except:
		print "\nNo more data"
		quit()
	data.append(sample)
	# print data
    #data  looks like [(.2,,5,-1.1,.4),(.4,,5,-1.1,.4),...]
    # initialize the data for the first sample
	if len(data)==1:
	    peak,dip,peak_range=sample[dominant_axis],sample[dominant_axis],0

	else:
	    if sample[dominant_axis]>peak:  
	        peak=sample[dominant_axis]
	        peak_range=peak - dip
	    # dips
	    if sample[dominant_axis]<dip:  
	        dip=sample[dominant_axis]
	        peak_range=peak - dip

	if len(data)>3:
	    y_slope=get_slope(dominant_axis)
	    # print str(y_slope)
	    d_slope=prev_slope- y_slope
	    
	    ## This determines the sensitivity of the rep counter.
	    if  peak_range>.7:
	        if (prev_slope>0 and y_slope<0) or (prev_slope<0 and y_slope>0):
	            # print "peak with range: %f" % peak_range
	            peaks+=1
	            if peaks==2:
					exercise="curl"
					all_reps["curls"]+=1
					# print exercise + str(all_reps["curls"])
					del data[:-1]
					reps+=1
					# print reps
				
					# print "test"
					peaks=0
					peak, dip,range_z=sample[dominant_axis],sample[dominant_axis], 0
					# return all_reps
	    prev_slope=y_slope


def main():
	global reps
	r=reps
	while True:
		detect_rep()
		if reps !=r:
			print reps
			r=reps
		# 	with open('tmp.json',"w") as f:
		# 		f.write(reps)

if __name__ == '__main__':
	main()