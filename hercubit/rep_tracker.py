# Attribution: https://gist.github.com/schlady/1576079
import numpy as np
import settings
import time

def peakdetect(y_axis, x_axis = None, lookahead = 500, delta = 0):
    """
    Converted from/based on a MATLAB script at http://billauer.co.il/peakdet.html
    
    Algorithm for detecting local maximas and minmias in a signal.
    Discovers peaks by searching for values which are surrounded by lower
    or larger values for maximas and minimas respectively
    
    keyword arguments:
    y_axis -- A list containg the signal over which to find peaks
    x_axis -- A x-axis whose values correspond to the 'y_axis' list and is used
        in the return to specify the postion of the peaks. If omitted the index
        of the y_axis is used. (default: None)
    lookahead -- (optional) distance to look ahead from a peak candidate to
        determine if it is the actual peak (default: 500) 
        '(sample / period) / f' where '4 >= f >= 1.25' might be a good value
    delta -- (optional) this specifies a minimum difference between a peak and
        the following points, before a peak may be considered a peak. Useful
        to hinder the algorithm from picking up false peaks towards to end of
        the signal. To work well delta should be set to 'delta >= RMSnoise * 5'.
        (default: 0)
            Delta function causes a 20% decrease in speed, when omitted
            Correctly used it can double the speed of the algorithm
    
    return -- two lists [maxtab, mintab] containing the positive and negative
        peaks respectively. Each cell of the lists contains a tupple of:
        (position, peak_value) 
        to get the average peak value do 'np.mean(maxtab, 0)[1]' on the results
    """
    maxtab = []
    mintab = []
    dump = []   #Used to pop the first hit which always if false
       
    length = len(y_axis)
    if x_axis is None:
        x_axis = range(length)
    
    #perform some checks
    if length != len(x_axis):
        raise ValueError, "Input vectors y_axis and x_axis must have same length"
    if lookahead < 1:
        raise ValueError, "Lookahead must be above '1' in value"
    if not (np.isscalar(delta) and delta >= 0):
        raise ValueError, "delta must be a positive number"
    
    #needs to be a numpy array
    y_axis = np.asarray(y_axis)
    
    #maxima and minima candidates are temporarily stored in
    #mx and mn respectively
    mn, mx = np.Inf, -np.Inf
    
    #Only detect peak if there is 'lookahead' amount of points after it
    for index, (x, y) in enumerate(zip(x_axis[:-lookahead], y_axis[:-lookahead])):
        if y > mx:
            mx = y
            mxpos = x
        if y < mn:
            mn = y
            mnpos = x
        
        ####look for max####
        if y < mx-delta and mx != np.Inf:
            #Maxima peak candidate found
            #look ahead in signal to ensure that this is a peak and not jitter
            if y_axis[index:index+lookahead].max() < mx:
                maxtab.append((mxpos, mx))
                dump.append(True)
                #set algorithm to only find minima now
                mx = np.Inf
                mn = np.Inf
        ## Morgan's addition
        y    
            
        
        ####look for min####
        if y > mn+delta and mn != -np.Inf:
            #Minima peak candidate found 
            #look ahead in signal to ensure that this is a peak and not jitter
            if y_axis[index:index+lookahead].min() > mn:
                mintab.append((mnpos, mn))
                dump.append(False)
                #set algorithm to only find maxima now
                mn = -np.Inf
                mx = -np.Inf
    
    
    #Remove the false hit on the first value of the y_axis
    try:
        if dump[0]:
            maxtab.pop(0)
            #print "pop max"
        else:
            mintab.pop(0)
            #print "pop min"
        del dump
    except IndexError:
        #no peaks were found, should the function return empty lists?
        pass
    
    return maxtab, mintab


###
# Function by Morgan Wallace
#
# accepts streamed data from hercubit
# returns features of peaks
###
deltas={'acc':.15,'gyro':2500,'magnet':15}
last_peaks={}
t=[]
x=[]
y=[]
z=[]
rep_count=0
 # changes- get rid of first 8 lines- move them to main()
def live_peaks(sample,debug=False,dataset='archive',lookahead=3,elim_first_value=True,get_features=False):
    global deltas, last_peaks,t,y,x,z,rep_count

    # #refresh
    # if len(t)>1:
    #     if t[-1]+(settings.sampleRate*2)<time.time():
    #         last_peaks={}
    #         t=[]
    #         x=[]
    #         y=[]
    #         z=[]

    if debug==True:
        # Graph peaks
        import matplotlib.pyplot as plt
        import pylab as pl

    #time - (although, it's considered the 'x' axis in the peak detection function
    t.append(sample['time'])
    
    #using just the accelerometer's x,y,z for peak detection
    x.append(sample['accel'][0])
    y.append(sample['accel'][1])
    z.append(sample['accel'][2])


    #Don't even look for peaks unless a min_rep_window worth of time has passed
    if len(t)<settings.min_rep_window/settings.sampleRate: return None
    
    x_peaks=peakdetect(x,t,lookahead=lookahead,delta=deltas['acc'])
    y_peaks=peakdetect(y,t,lookahead=lookahead,delta=deltas['acc'])
    z_peaks=peakdetect(z,t,lookahead=lookahead,delta=deltas['acc'])
    
    ###
    # Test for completion of repitition
    # ...Once all axes have min and max
    peaks_soFar= sum([1 for i in x_peaks+y_peaks+z_peaks if i!=[]])
    # print peaks_soFar
    sds={}
    sds['x']=np.std(x)
    sds['y']=np.std(y)
    sds['z']=np.std(z)
    avg={}
    avg['x']=sum(x)/len(x)
    avg['y']=sum(y)/len(y)
    avg['z']=sum(z)/len(z)
    peak_cutoff=3
    if peaks_soFar<peak_cutoff: return None #not enough peaks yet to be a repitition
    if peaks_soFar>=peak_cutoff and peaks_soFar<=5:
        

        if sds['y']>.42 and sds['x']>0.09 and sds['z']>0.13: # bicep curls
            if peaks_soFar<5: 
                if sum([1 for i in y_peaks if i!=[]])!=2:
                    return  None    
            
            print "Bicep Curl"
        if sds['x']>.3 and sds['y']<.29 and sds['z']<.17: #tricep curl
            if peaks_soFar<5:
                if sum([1 for i in x_peaks if i!=[]])!=2:
                    return None
            print "Tricep Curl"
        if sds['x']<0.19 and sds['z']<0.13:# Shoulder Press
            if sum([1 for i in y_peaks if i!=[]])!=2:
                return None
            else: print "Shoulder Press"
        # if y[-1]>y[1]:
        #     if y[-1]>y[1]+.2: return None
        # else:
        #     if y[-1]<y[1]-.2: return None
    # print "sd: "+str(sds)
    # print "avg: "+str(avg)



    # print sds
    rep_count+=1
    print 'reps: '+str(rep_count)
    if debug==True:
        # Graph peaks
        import matplotlib.pyplot as plt
        import pylab as pl
        fig, ax = plt.subplots()
        ax.plot(t, x,label='x')
        ax.plot(t, y,label='y')
        ax.plot(t, z,label='z')
        ax.plot([q[0] for q in x_peaks[0]+x_peaks[1]],[q[1] for q in x_peaks[0]+x_peaks[1]],'o')
        ax.plot([q[0] for q in y_peaks[0]+y_peaks[1]],[q[1] for q in y_peaks[0]+y_peaks[1]],'o')
        ax.plot([q[0] for q in z_peaks[0]+z_peaks[1]],[q[1] for q in z_peaks[0]+z_peaks[1]],'o')
        ax.legend()
    #find axis with 

    next_start_time= max([i[0][0] for i in x_peaks+y_peaks+z_peaks if i!=[]])
    # print l
    # print max(l)
    # #set place to start next peak detection at last min/max
    # for axis in (x_peaks,y_peaks,z_peaks):
    #     if axis[0]!=[] and axis[1]!=[]:    
    #         t_max= axis[0][-1][0] #time of x's max
    #         t_min= axis[1][-1][0] #time of x's min
    # next_start_time=max(t_max,t_min) #the later of the above 2
#                     print next_start_time
    for c in t:
#                         print c
        if round(c,2)==round(next_start_time,2):
            end=c
            i=t.index(c)
            break
    t=t[i:]
    x=x[i:]
    y=y[i:]
    z=z[i:]

    #extract features
    if get_features==False:
        return rep_count
    else:  
        ranges={}
#                     print x_peaks
        ranges['x']=x_peaks[0][0][1]-x_peaks[1][0][1]
        ranges['y']=y_peaks[0][0][1]-y_peaks[1][0][1]
        ranges['z']=z_peaks[0][0][1]-z_peaks[1][0][1]
        avg={}
        avg['x']=sum(x)/len(x)
        avg['y']=sum(y)/len(y)
        avg['z']=sum(z)/len(z)
        sds={}
        sds['x']=np.std(x)
        sds['y']=np.std(y)
        sds['z']=np.std(z)
        
        features={'peak start':t[0],'ranges':ranges,'means':avg,"standard deviations":sds,'peak end':end}
        
        return features


def main():
    import device
    ser,conn_type=device.connect(bluetooth_enabled=True)
    gen = device.sensor_stream(ser,conn_type)
    while True:
        sample=gen.next()
        # print sample
        count=live_peaks(sample,debug=True)
        # if count!=None:
        #     # print count

if __name__ == '__main__':
    main()
 