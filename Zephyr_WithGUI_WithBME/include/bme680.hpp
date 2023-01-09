#ifndef BME680_HPP
#define BME680_HPP

#include <drivers/sensor.h>
//#include "log.hpp"
/*#include <logging/log.h>
LOG_MODULE_DECLARE(app);*/
#ifndef LOG_LEVEL
#define LOG_LEVEL CONFIG_LOG_DEFAULT_LEVEL
#endif

#define BME680_DEV_NAME DT_LABEL(DT_INST(0, bosch_bme680))

class BME680 {       
  public:             
    const struct device *dev;

    int false_value = 0;

    void init();

    double get_temperature();
    double get_humidity();
};

#endif