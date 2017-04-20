#ifndef TESTARCHIVESTEADYSTATE_HPP_
#define TESTARCHIVESTEADYSTATE_HPP_

#include <cxxtest/TestSuite.h>
#include "APSimulator.hpp"
#include "FakePetscSetup.hpp"


class TestArchiveSteadyState : public CxxTest::TestSuite
{
public:
    void xTestRunToSteadyState() throw(Exception)
    {
#ifdef CHASTE_CVODE

        double stimulus_magnitude = -25.5, stimulus_duration = 2, stimulus_period = 1000, stimulus_start_time = 20;
        
        double solve_start = 0, solve_end = 400, solve_timestep = 0.1;
    
        unsigned model_number = 8u; // 8. Decker 2009 dog
    
        APSimulator simulator;
        
        simulator.DefineStimulus( stimulus_magnitude, stimulus_duration, stimulus_period, stimulus_start_time );
        simulator.DefineSolveTimes(solve_start, solve_end, solve_timestep);
        simulator.DefineModel(model_number);
        
        std::vector<std::string> parameter_metanames = simulator.GetParameterMetanames();
        for (unsigned i=0; i<parameter_metanames.size(); i++)
        {
            std::cout << parameter_metanames[i] << std::endl << std::flush;
        }
        
        bool result = simulator.RunToSteadyState();
        TS_ASSERT_EQUALS(result,true);

#else
        std::cout << "Cvode is not enabled.\n";
#endif
    }
    void xTestArchiveNonSSVariables() throw(Exception)
    {
#ifdef CHASTE_CVODE

        double stimulus_magnitude = -25.5, stimulus_duration = 2, stimulus_period = 1000, stimulus_start_time = 20;
        
        double solve_start = 0, solve_end = 400, solve_timestep = 0.1;
    
        unsigned model_number = 8u; // 8. Decker 2009 dog
    
        APSimulator simulator;
        
        simulator.DefineStimulus( stimulus_magnitude, stimulus_duration, stimulus_period, stimulus_start_time );
        simulator.DefineSolveTimes(solve_start, solve_end, solve_timestep);
        simulator.DefineModel(model_number);
        
        simulator.ArchiveStateVariables();

#else
        std::cout << "Cvode is not enabled.\n";
#endif
    }
    void xTestArchiveSSVariables() throw(Exception)
    {
#ifdef CHASTE_CVODE

        double stimulus_magnitude = -25.5, stimulus_duration = 2, stimulus_period = 1000, stimulus_start_time = 20;
        
        double solve_start = 0, solve_end = 400, solve_timestep = 0.1;
    
        unsigned model_number = 8u; // 8. Decker 2009 dog
    
        APSimulator simulator;
        
        simulator.DefineStimulus( stimulus_magnitude, stimulus_duration, stimulus_period, stimulus_start_time );
        simulator.DefineSolveTimes(solve_start, solve_end, solve_timestep);
        simulator.DefineModel(model_number);
        
        bool result = simulator.RunToSteadyState();
        TS_ASSERT_EQUALS(result,true);
        
        simulator.ArchiveStateVariables();

#else
        std::cout << "Cvode is not enabled.\n";
#endif
    }
    void TestLoadArchiveSSVariables() throw(Exception)
    {
#ifdef CHASTE_CVODE

        double stimulus_magnitude = -25.5, stimulus_duration = 2, stimulus_period = 1000, stimulus_start_time = 20;
        
        double solve_start = 0, solve_end = 400, solve_timestep = 0.1;
    
        unsigned model_number = 8u; // 8. Decker 2009 dog
    
        APSimulator simulator;
        
        simulator.DefineStimulus( stimulus_magnitude, stimulus_duration, stimulus_period, stimulus_start_time );
        simulator.DefineSolveTimes(solve_start, solve_end, solve_timestep);
        simulator.DefineModel(model_number);
        
        bool result = simulator.RunToSteadyState();
        TS_ASSERT_EQUALS(result,true);
        
        APSimulator simulator2;
        
        simulator2.DefineStimulus( stimulus_magnitude, stimulus_duration, stimulus_period, stimulus_start_time );
        simulator2.DefineSolveTimes(solve_start, solve_end, solve_timestep);
        simulator2.DefineModel(model_number);
        simulator2.LoadStateVariables();

#else
        std::cout << "Cvode is not enabled.\n";
#endif
    }
};

#endif /*TESTARCHIVESTEADYSTATE_HPP_*/
