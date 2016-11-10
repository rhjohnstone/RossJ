#ifndef APSIMULATOR_HPP_
#define APSIMULATOR_HPP_

#include "AbstractCvodeCellWithDataClamp.hpp"
#include "OutputFileHandler.hpp"


class APSimulator
{
private:
    unsigned mModelNumber;
    unsigned mProtocolNumber;
public:
    APSimulator(unsigned model_number,
                unsigned protocol_number);
    ~APSimulator();
};










#endif /*APSIMULATOR_HPP_*/
