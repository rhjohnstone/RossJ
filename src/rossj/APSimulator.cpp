#include "APSimulator.hpp"

#include "RegularStimulus.hpp"
#include "SimpleStimulus.hpp"
#include "MultiStimulus.hpp"
#include "AbstractIvpOdeSolver.hpp"
#include <boost/shared_ptr.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/tokenizer.hpp>
#include "BoostFilesystem.hpp"
#include "RandomNumberGenerator.hpp"

#include "CheckpointArchiveTypes.hpp"
#include "ArchiveLocationInfo.hpp"

//#include "HodgkinHuxley1952CvodeDataClamp.hpp"
//#include "HodgkinHuxley1952Cvode.hpp"
#include "hodgkin_huxley_squid_axon_model_1952_modifiedCvode.hpp"

APSimulator::APSimulator()
{
}

APSimulator::~APSimulator()
{
}

void APSimulator::DefineStimulus(double stimulus_magnitude,
                                 double stimulus_duration,
                                 double stimulus_period,
                                 double stimulus_start_time)
{
    mpStimulus.reset(new RegularStimulus(stimulus_magnitude,stimulus_duration,stimulus_period,stimulus_start_time));
}

void APSimulator::DefineModel(unsigned model_number)
{
    boost::shared_ptr<AbstractIvpOdeSolver> p_solver;
    if (model_number == 1u)
    {
        mpModel.reset(new Cellhodgkin_huxley_squid_axon_model_1952_modifiedFromCellMLCvode(p_solver, mpStimulus));
        mParameterMetanames.push_back("membrane_fast_sodium_current_conductance"); // 120
        mParameterMetanames.push_back("membrane_potassium_current_conductance"); // 36
        mParameterMetanames.push_back("membrane_leakage_current_conductance"); // 0.3
    }
}

std::vector<std::string> APSimulator::GetParameterMetanames()
{
    return mParameterMetanames;
}
