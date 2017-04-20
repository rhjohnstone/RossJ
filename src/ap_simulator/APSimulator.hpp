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
    unsigned mNumberOfFailedSolves;
    unsigned mHowManySolves;
    double mSolveStart;
    double mSolveEnd;
    double mSolveTimestep;
    unsigned mNumTimePts;
    bool mUseDataClamp;
    double mDataClampOn;
    double mDataClampOff;
    bool mHaveRunToSteadyState;
public:
    APSimulator();
    ~APSimulator();
    //void RedirectStdErr();
    void DefineStimulus(double stimulus_magnitude, double stimulus_duration, double stimulus_period, double stimulus_start_time);
    void DefineSolveTimes(double solve_start, double solve_end, double solve_timestep);
    void DefineModel(unsigned model_number);
    std::vector<std::string> GetParameterMetanames();
    std::vector<double> SolveForVoltageTraceWithParamsNoDataClamp(const std::vector<double>& rParams);
    std::vector<double> SolveForVoltageTraceWithParamsWithDataClamp(const std::vector<double>& rParams);
    std::vector<double> SolveForVoltageTraceWithParams(const std::vector<double>& rParams);
    void SetTolerances(double rel_tol, double abs_tol);
    double ExampleLogLikelihoodFunction(const std::vector<double>& test_trace);
    std::vector<double> GenerateSyntheticExptTrace(const std::vector<double>& rParams, double noise_sd, double c_seed);
    void UseDataClamp(double data_clamp_on, double data_clamp_off);
    void SetExperimentalTraceAndTimesForDataClamp(const std::vector<double>& expt_times, const std::vector<double>& expt_trace);
    void SetExtracellularPotassiumConc( double extra_K_conc );
    void SetNumberOfSolves( unsigned num_solves );
    boost::shared_ptr<AbstractCvodeCell> GetModel();
    bool RunToSteadyState();
    void ArchiveStateVariables();
};



#endif /*APSIMULATOR_HPP_*/
