/**
 ******************************************************************************
 * Copyright 2024 jLab
 * @file     sdi12.h
 * @author   Stephen Taylor
 * @brief    This file contains all the driver functions for communication to a
 *           TEROS-12 sensor via SDI-12.
 *           https://www.sdi-12.org/
 *
 * @date     4/1/2024
 ******************************************************************************
 */

#ifndef LIB_SDI12_INCLUDE_SDI12_H_
#define LIB_SDI12_INCLUDE_SDI12_H_

#ifdef __cplusplus
extern "C" {
#endif

#include <stdio.h>
#include <stdlib.h>

#include "usart.h"
#include "gpio.h"
#include "lptim.h"
#include "user_config.h"
#include "tim.h"

/** Status codes for the Fram library*/
typedef enum {
  SDI12_OK = 0,
  SDI12_ERROR = -1,
  SDI12_TIMEOUT_ON_READ = -2,
  SDI12_PARSING_ERROR = -3,
} SDI12Status;


/* The returned values from a SDI12 get measurment command*/
typedef struct {
  char Address;
  uint16_t Time;
  uint8_t NumValues;
} SDI12_Measure_TypeDef;

/* The relevant data for a TEROS-12 sensor*/
typedef struct {
  int ec;
  float vwc_raw;
  float vwc_adj;
  float tmp;
  int addr;
} Teros12_Data;

/**
******************************************************************************
* @brief    Wake all sensors on the data line.
*
* @param    void
* @return   void
******************************************************************************
*/
void SDI12WakeSensors(void);

/**
******************************************************************************
* @brief    Send a command via SDI12
*
* @param    const char *, command
* @return   SDI12Status
******************************************************************************
*/
SDI12Status SDI12SendCommand(const char *command, uint8_t size);

/**
******************************************************************************
* @brief    Read data from a TEROS-12 sensor via SDI-12
*
* @param    char *, buffer
* @param    uint16_t, bufferSize
* @param    uint16_t, timeoutMillis
* @param    const char *, command
* @return   SDI12Status
******************************************************************************
*/
SDI12Status SDI12ReadData(char *buffer, uint16_t bufferSize, uint16_t timeoutMillis);

/**
******************************************************************************
* @brief    This is a function to read a measurment from a particular sensor.
*
* @param    char const addr, the device address
* @param    SDI12_Measure_TypeDef, a custom struct to store the measurment information returned from start measurment
* @param    char* the measurment data returned
* @param    uint16_t timeoutMillis time out in milliseconds
* @return   SDI12Status
******************************************************************************
*/
SDI12Status SDI12GetMeasurment(uint8_t addr, SDI12_Measure_TypeDef *measurment_info, char *measurment_data, uint16_t timeoutMillis);

#ifdef __cplusplus
}
#endif

#endif  // LIB_SDI12_INCLUDE_SDI12_H_
