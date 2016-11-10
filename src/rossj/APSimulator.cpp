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

APSimulator::APSimulator(unsigned model_number,
                         unsigned protocol_number)
    : mModelNumber(model_number),
      mProtocolNumber(protocol_number)
{
}

APSimulator::~APSimulator()
{
}
