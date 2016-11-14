import unittest
import rossj
import time
import numpy as np
import subprocess

class TestCompareStdOut(unittest.TestCase):

    def test_rossj(self):
        message = 'hello world'
        ross = rossj.RossManual(message)
        how_many_repeats = 10000
        test_vector = np.arange(1000)
        
        start = time.time()
        for _ in xrange(how_many_repeats):
            doubled_vector_1 = ross.TimesByTwo(test_vector)
        time_taken = time.time()-start
        print "\nTime taken by rossj TimesByTwo: {} s\n".format(round(time_taken,2))
        
        
        #EXE_NAME = "./projects/RossJ/apps/TimesByTwoApp"
        EXE_NAME = "/home/rossj/chaste-build/projects/RossJ/apps/TimesByTwoApp" # this needs to be more general for chaste build path
        process = subprocess.Popen(EXE_NAME, False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        PROVENANCE_HEADER = "This version of Chaste was compiled on:"
	
        reading_values, looking_for_blank = False, False
        while (not reading_values):
            line = process.stdout.readline()
            if line.startswith(PROVENANCE_HEADER):
                looking_for_blank = True
            elif looking_for_blank and line.strip() == "":
                reading_values = True
                
        start = time.time()
        for _ in xrange(how_many_repeats):
            output_string_to_c = " ".join(map(str, test_vector)) + '\n'
            process.stdin.write(output_string_to_c)
            doubled_vector_2_str = process.stdout.readline()
            doubled_vector_2 = np.fromstring(doubled_vector_2_str, dtype=float, sep=' ')
        time_taken = time.time()-start
        print "\nTime taken by TimesByTwoApp: {} s\n".format(round(time_taken,2))
        
        if ( np.all(doubled_vector_1==doubled_vector_2) ):
            print "The two outputted vectors are the same, don't worry."


if __name__ == '__main__':
    unittest.main()
