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
public:
    APSimulator();
    ~APSimulator();
    //void RedirectStdErr();
    void DefineProtocol(unsigned protocol_number);
    void DefineModel(unsigned model_number);
    std::vector<std::string> GetParameterMetanames();
    std::vector<double> SolveForVoltageTraceWithParams(const std::vector<double>& rParams);
    void SetTolerances(double rel_tol, double abs_tol);
    double ExampleLogLikelihoodFunction(const std::vector<double>& test_trace);
};



#endif /*APSIMULATOR_HPP_*/
