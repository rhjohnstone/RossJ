/*

Copyright (c) 2005-2016, University of Oxford.
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

#ifndef TESTAPSIMULATOR_HPP_
#define TESTAPSIMULATOR_HPP_

#include <cxxtest/TestSuite.h>
/* Most Chaste code uses PETSc to solve linear algebra problems.  This involves starting PETSc at the beginning of a test-suite
 * and closing it at the end.  (If you never run code in parallel then it is safe to replace PetscSetupAndFinalize.hpp with FakePetscSetup.hpp)
 */
#include "PetscSetupAndFinalize.hpp"
#include "APSimulator.hpp"

/**
 * @file
 *
 * This is an example of a CxxTest test suite, used to test the source
 * code, and also used to run simulations (as it provides a handy
 * shortcut to compile and link against the correct libraries using scons).
 *
 * You can #include any of the files in the project 'src' folder.
 * For example here we #include "Hello.hpp"
 *
 * You can utilise any of the code in the main the Chaste trunk
 * in exactly the same way.
 * NOTE: you will have to alter the project SConscript file lines 41-44
 * to enable #including of code from the 'heart', 'cell_based' or 'crypt'
 * components of Chaste.
 */

class TestAPSimulator : public CxxTest::TestSuite
{
public:
    void TestAPSimulatorClass() throw(Exception)
    {
    
        double stimulus_magnitude = -25.5, stimulus_duration = 2, stimulus_period = 1000, stimulus_start_time = 20;
    
        unsigned model_number = 1u;
    
        APSimulator simulator;
        
        simulator.DefineProtocol( stimulus_magnitude, stimulus_duration, stimulus_period, stimulus_start_time );
        simulator.DefineModel(model_number);
        
        std::vector<std::string> parameter_metanames = simulator.GetParameterMetanames();
        for (unsigned i=0; i<parameter_metanames.size(); i++)
        {
            std::cout << parameter_metanames[i] << std::endl << std::flush;
        }

    }
    void xTestAPSolve() throw(Exception)
    {
        unsigned model_number = 1u;

        double stimulus_magnitude = -25.5, stimulus_duration = 2, stimulus_period = 1000, stimulus_start_time = 20;
    
        APSimulator simulator;
        
        simulator.DefineProtocol( stimulus_magnitude, stimulus_duration, stimulus_period, stimulus_start_time );
        simulator.DefineModel(model_number);

        
        std::vector<double> params;
        if (model_number==1u)
        {
            params.push_back(120);
            params.push_back(36);
            params.push_back(0.3);
        }
        
        
        
        
        std::vector<double> voltage_trace = simulator.SolveForVoltageTraceWithParams(params);
        std::cout << "voltage_trace.size() = " << voltage_trace.size() << std::endl << std::flush;
        for (unsigned i=0; i<voltage_trace.size()-1; i++)
        {
            std::cout << voltage_trace[i] << " ";
        }
        std::cout << voltage_trace.back() << std::endl << std::flush;
    }
};

#endif /*TESTAPSIMULATOR_HPP_*/
