#ifndef WAVE_H
#define WAVE_H

#include "regular_wave.h"
#include "constants.h"

struct Wave
{
  // Input variables
  // ---------------
  double significant_wave_height;   // Significant wave height in meter.
  double heading; // wave heading in radians
  long random_number_seed; 
  
  // Output variables
  // ----------------
  // Table of regular waves in the irregular sea.
  struct Regular_wave spectrum[COUNT_WAVE_SPECTRAL_DIRECTIONS]
                              [COUNT_WAVE_SPECTRAL_FREQUENCIES];
  double min_spectral_frequency;  // Lower limit (0.1%) of spectral energy 
                                  // threshold.
  double max_spectral_frequency;  // Upper limit (99.9%) of spectral energy 
                                  // threshold.
  double peak_spectral_frequency; // Spectral peak frequency in Hz.
  double min_spectral_wave_heading; // Minimum angle, in radians, in spectrum
                                    // for wave heading.
  double max_spectral_wave_heading; // Maximum angle, in radians, in spectrum 
                                    // for wave heading.
};

/**
 * Initialise the irregular wave.
 * @param wave is the pointer to the wave object to be initialised.
 * @param sig_wave_height is the significant wave height. Value should be 
 * non-zero positive.
 * @param wave_heading in radians
 * @param rand_seed is the seed for random number generator. 
 * @return 0 if no error encountered. 
 *         1 if wave is nullptr. 
 *         2 if sig_wave_height is 0 or negative value.
 */
int wave_init(struct Wave* wave, 
               double sig_wave_height, 
               double wave_heading, 
               long rand_seed);

/**
 * Get sea surface elevation at the given location for the given time. 
 * @param wave is the pointer to the irregular sea surface wave. Assumes wave to
 * be not a null pointer.
 * @param location at which the elevation is to be computed.
 * @param time for which the elevation is to be computed. Time is measured in 
 * seconds from start of simulation.
 * @return wave elevation in meter.
 */
double wave_get_elevation(struct Wave* wave, 
                          struct Dimensions* location, 
                          double time);

#endif // WAVE_H
