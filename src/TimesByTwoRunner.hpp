/*

Copyright (c) 2005-2015, University of Oxford.
All rights reserved.

University of Oxford means the Chancellor, Masters and Scholars of the
University of Oxford, having an administrative office at Wellington
Square, Oxford OX1 2JD, UK.

This file is part of Chaste.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
 * Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.
 * Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
 * Neither the name of the University of Oxford nor the names of its
   contributors may be used to endorse or promote products derived from this
   software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

*/

#ifndef TIMESBYTWORUNNER_HPP_
#define TIMESBYTWORUNNER_HPP_

#include "CommandLineArguments.hpp"
#include "Ross.hpp"

/**
 * A small class that is used by the McmcApp to do all of its work.
 * It is in a separate class here so it can be tested nicely.
 *
 * build the App with the call
 * scons -j3 cl=1 b=GccOpt exe=1 projects/RossJ/apps/src
 *
 * At present it just checks that we have called the program with the argument --theta-values
 * and then prints out the vector multiplied by two.
 *
 * We want to change it so that the constructor does an ODE solve.
 *
 */
class TimesByTwoRunner
{
private:

public:
    /**
     * Default constructor.
     *
     * Reads command line arguments
     */
    TimesByTwoRunner()
    {
        // Runs our 'reference/experimental' trace.

        std::string message = "Hello world";
        Ross ross(message);

        std::vector<double> theta;
        std::vector<double> doubled_theta;
        do
        {
            //wait for theta values from std::in
            //std::vector<double> theta;
            // std::cin >> theta;

            std::string input;
            std::getline(std::cin, input);
            if (input=="finish")
            {
                break;
            }
            //std::cerr << "input = " << input << std::endl << std::flush;
            std::istringstream is(input);
            theta = std::vector<double>(std::istream_iterator<double>(is), std::istream_iterator<double>());

            doubled_theta = ross.TimesByTwo(theta);

            for (unsigned i=0; i<doubled_theta.size()-1; i++)
            {
                std::cout << doubled_theta[i] << " ";
            }
            std::cout << doubled_theta.back() << std::endl << std::flush;            
            
        }
        while(true);

    }

};

#endif /*TIMESBYTWORUNNER_HPP_*/
