/**
 * @brief Library used to interface with the Dirtviz API
 *
 * Assumes that WiFi interface is connected to the network.
 *
 * @author John Madden <jmadden173@pm.me>
 * @date 2023-11-29
 */

#ifndef LIB_DIRTVIZ_INCLUDE_DIRTVIZ_HPP_
#define LIB_DIRTVIZ_INCLUDE_DIRTVIZ_HPP_

#include <WiFi.h>
#include <WiFiClientSecure.h>

#include <cstdio>
#include <cstdlib>
#include <cstring>

/**
 * @brief HTTP interface for Dirtviz API
 */
class Dirtviz {
 private:
  /** URL of API */
  char *url = nullptr;

  /** Port of API*/
  uint16_t port;

  /** Buffer for the HTTP response */
  char *response = nullptr;

 public:
  /**
   * @brief Default constructor
   *
   * Allows for setting of URL on initialization.
   *
   * @param url API URL
   * @param port API port number
   */
  Dirtviz(const char *url, const uint16_t &port);

  /**
   * @brief Frees all memory
   */
  ~Dirtviz();

  /**
   * @brief Setter for @p url
   *
   * @param new_url New API URL
   */
  void SetUrl(const char *new_url);

  /**
   * @brief Getter for @p url
   *
   * @returns Pointer to @p url
   */
  const char *GetUrl(void) const;

  /**
   * @brief Setter for @p port
   *
   * @param new_port New port number
   */
  void SetPort(const uint16_t &new_port);

  /**
   * @brief Getter for @p port
   *
   * @returns value of @p url
   */
  uint16_t GetPort(void) const;

  /**
   * @brief Send serialized measurement to the API
   *
   * The entire response is stored in a dynamically allocated buffer. Use
   * Dirtviz::GetResponse to get the binary response data.
   *
   * @param meas Pointer to serialized measurement data
   * @param meas_len Number of bytes in @p meas
   *
   * @return HTTP response code, -1 indicates an error in parsing
   */
  int SendMeasurement(const uint8_t *meas, size_t meas_len);

  /**
   * @brief Get binary data from response
   *
   * A returned length of 0 indicates an error and the pointer @p data has not
   * been modified.
   *
   * @param data Pointer to response binary data
   *
   * @return Length of @p data
   */
  size_t GetResponse(const uint8_t *data) const;
};

#endif  // LIB_DIRTVIZ_INCLUDE_DIRTVIZ_HPP_
