#ifndef LIB_FRAM_SRC_MB85RC1MT_H_
#define LIB_FRAM_SRC_MB85RC1MT_H_

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>
#include <stdio.h>

#include "fram.h"

/**
 * @brief Writes bytes to an address
 *
 * @param addr Address of write
 * @param data An array of data bytes.
 * @param len The number of bytes to be written.
 * @return See FramStatus
 */
FramStatus Mb85rc1mtWrite(FramAddr addr, const uint8_t *data, size_t len);

/**
 * @brief This function reads a dynamic number of bytes to FRAM.
 *
 * @param addr Address of read
 * @param data Array to be read into
 * @param len Number of sequential bytes to read
 * @return See FramStatus
 */
FramStatus Mb85rc1mtRead(FramAddr addr, size_t len, uint8_t *data);

#ifdef __cplusplus
}
#endif

#endif  // LIB_FRAM_SRC_MB85RC1MT_H_