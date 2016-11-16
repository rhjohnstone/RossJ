#ifndef APSIMULATOR_HPP_
#define APSIMULATOR_HPP_

#include "AbstractCvodeCellWithDataClamp.hpp"
#include "OutputFileHandler.hpp"

class APSimulator
{
private:
    unsigned mModelNumber;
    //unsigned mProtocolNumber;
    boost::shared_ptr<AbstractCvodeCell> mpModel;
    boost::shared_ptr<AbstractStimulusFunction> mpStimulus;
    std::vector<std::string> mParameterMetanames;
    std::vector<double> mExptTimes;
    std::vector<double> mExptTrace;
    double mSamplingTimestep;
    unsigned mNumberOfFailedSolves;
    unsigned mHowManySolves;
public:
    APSimulator();
    ~APSimulator();
    void DefineStimulus(double stimulus_magnitude,
                        double stimulus_duration,
                        double stimulus_period,
                        double stimulus_start_time);
    void DefineModel(unsigned model_number);
    std::vector<std::string> GetParameterMetanames();
    std::vector<double> SolveForVoltageTraceWithParams(const std::vector<double>& rParams, double start_time, double end_time);
};



#endif /*APSIMULATOR_HPP_*/
