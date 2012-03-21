import timeit

import scipy.fftpack
spfftn = scipy.fftpack.fftn
spifftn = scipy.fftpack.ifftn

import numpy as np
npfftn = np.fft.fftn
npifftn = np.fft.ifftn

import fftw3
def wfftn(array,nthreads=4):
    array = array.astype('complex')
    outarray = array.copy()
    fft_forward = fftw3.Plan(array,outarray, direction='forward', flags=['estimate'], nthreads=nthreads)
    fft_forward()
    return outarray
def wifftn(array,nthreads=4):
    array = array.astype('complex')
    outarray = array.copy()
    fft_backward = fftw3.Plan(array,outarray, direction='backward', flags=['estimate'], nthreads=nthreads)
    fft_backward()
    return outarray

if __name__ == "__main__":
    for ndims in [1,2,3]:
        print "\n%i-dimensional arrays" % ndims
        print " ".join(["%17s" % n for n in ("n","sp","np","fftw")])

        for ii in xrange(3,15-ndims*2):
            #array = np.random.random([2**ii]*ndims)
            setup="import test_ffts; import numpy as np; array = np.random.random([%i]*%i)" % (2**ii,ndims)

            #print array.mean(),array.std()
            #print [ffttype for ffttype in ('sp','np','w')]
            #print min(timeit.Timer(stmt="test_ffts.%sfft2(array)" % 'sp',setup=setup).repeat(3,100))

            print "%16i:" % (int(2**ii)) + \
                    "".join(
                        ["%17f" % (min(timeit.Timer(stmt="test_ffts.%sfftn(array)" % ffttype,setup=setup).repeat(3,10)))
                            for ffttype in ('sp','np','w')]
                    )
                    
"""
RESULTS: (on an 8x2.93 GHz machine)
1-dimensional arrays
                n                sp                np              fftw
               8:         0.000231         0.000118         0.000967
              16:         0.000232         0.000116         0.000939
              32:         0.000227         0.000123         0.000970
              64:         0.000247         0.000126         0.001020
             128:         0.000246         0.000138         0.001899
             256:         0.000269         0.000166         0.002012
             512:         0.000316         0.000238         0.001975
            1024:         0.000414         0.000379         0.002086
            2048:         0.000632         0.000654         0.005446
            4096:         0.001052         0.001342         0.002493

2-dimensional arrays
                n                sp                np              fftw
               8:         0.000324         0.000241         0.002173
              16:         0.000385         0.000278         0.002242
              32:         0.000650         0.000887         0.002319
              64:         0.001713         0.001565         0.002821
             128:         0.006986         0.005583         0.006226
             256:         0.043852         0.026981         0.013707
             512:         0.218871         0.153257         0.068380
            1024:         1.169302         0.750841         0.362940

3-dimensional arrays
                n                sp                np              fftw
               8:         0.000711         0.000499         0.003165
              16:         0.002498         0.001661         0.003488
              32:         0.022048         0.015378         0.006693
              64:         0.241185         0.144020         0.047905
             128:         4.972296         1.720321         1.252997
             256:        48.344317        21.581751        12.607542
    
"""
