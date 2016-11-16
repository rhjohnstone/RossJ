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

#include "hodgkin_huxley_squid_axon_model_1952_modifiedCvode.hpp"

APSimulator::APSimulator()
    : mSamplingTimestep(0.25),
      mNumberOfFailedSolves(0),
      mHowManySolves(1)
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

std::vector<double> APSimulator::SolveForVoltageTraceWithParams(const std::vector<double>& rParams, double start_time, double end_time)
{
    std::vector<double> voltage_trace;

    mpModel->SetStateVariables(mpModel->GetInitialConditions());
    for (unsigned j=0; j<rParams.size(); j++)
    {
        mpModel->SetParameter(mParameterMetanames[j], rParams[j]);
    }
    try
    {
        if (mHowManySolves > 1)
        {
            for (unsigned i=0; i<mHowManySolves-1; i++)
            {
                mpModel->Compute(start_time, end_time, mSamplingTimestep);
            }
        }

        OdeSolution sol1 = mpModel->Compute(start_time, end_time, mSamplingTimestep); // Do I need a good way to kill everything if this fails to solve?
        voltage_trace = sol1.GetAnyVariable("membrane_voltage");
    }
    catch (Exception &e)
    {
        std::cerr << "WARNING: CVODE failed to solve with these parameters" << std::endl << std::flush;
        std::cerr << "error was " << e.GetShortMessage() << std::endl << std::flush;
        voltage_trace = std::vector<double>(mExptTimes.size(), 0.0);
        mNumberOfFailedSolves++;
    }
    return voltage_trace;
}
