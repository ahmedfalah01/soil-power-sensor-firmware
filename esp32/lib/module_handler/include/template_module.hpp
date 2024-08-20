/**
 * @file template_module.hpp
 * @author John Madden (jmadden173@pm.me)
 * @brief 
 * @version 0.1
 * @date 2024-08-12
 * 
 * @copyright Copyright (c) 2024
 * 
 */

#ifndef ESP32_LIB_MODULE_HANDLER_INCLUDE_TEMPLATE_MODULE_H_
#define ESP32_LIB_MODULE_HANDLER_INCLUDE_TEMPLATE_MODULE_H_

#include <cstddef>

#include "soil_power_sensor.pb.h"

namespace ModuleHandler {
  class Module {
    public:

    /**
     * @brief Construct a new Module object
     * 
     */
    Module(void);

    /**
     * @brief Destroy the Module object
     * 
     */
    ~Module(void);

    /**
     * @brief Arduino I2C onRecieve
     * 
     * @param num_bytes Number of bytes received from controller
     */
    virtual void OnReceive(const Esp32Command& cmd);

    /**
     * @brief Arduino I2C onRequest
     * 
     * @param buffer Pointer to store requested data
     * 
     * @returns Number of bytes in buffer
     */
    virtual size_t OnRequest(uint8_t* buffer);
    
    /**
     * @brief Get the current state of the module
     * 
     * @return Integer of state enum
     */
    virtual int State(void);

    /**
     * @brief Resets the module to default state
     * 
     */
    virtual void Reset();

    protected:
  };
}

#endif // ESP32_LIB_MODULE_HANDLER_INCLUDE_TEMPLATE_MODULE_H_