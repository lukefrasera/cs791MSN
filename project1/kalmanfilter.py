#!/usr/bin/env python

import numpy
import pylab
from math import *

class Kalman:
  def __init__(self, A_, B_, H_, X_, P_, Q_, R_):
    self.A = A_
    self.B = B_
    self.H = H_
    self.Q = Q_
    self.R = R_
    self.state_estimate = X_
    self.prob_estimate = P_

  def Step(self, measurement):
    X_k = self.A * self.state_estimate
    P_k = self.A * self.prob_estimate * numpy.transpose(self.A) + self.Q
    kalman_gain = P_k * numpy.transpose(self.H) * numpy.linalg.inv(self.H * P_k * numpy.transpose(self.H) + self.R)

    self.state_estimate = X_k + kalman_gain * (measurement - self.H * X_k)
    self.prob_estimate = P_k - kalman_gain * self.H * P_k

  def GetCurrentState(self):
    return self.state_estimate

def main():
  # import data
  data = numpy.genfromtxt('data.txt', delimiter=',', usecols=(1,2,3,5,6,7), unpack=True)
  odom_x = 0
  odom_y = 1
  odom = 2
  imu = 3
  gps_x = 4
  gps_y = 5

  # Filter Data
  A = numpy.matrix('1 0 0 0 0;\
                    0 1 0 0 0;\
                    0 0 1 0 0;\
                    0 0 0 1 0;\
                    0 0 0 0 1')
  B = A
  H = A
  X = numpy.matrix('0;\
                    0;\
                    0;\
                    0;\
                    0')

  P = numpy.matrix('.01 0 0 0 0;\
                    0 .01 0 0 0;\
                    0 0 .01 0 0;\
                    0 0 0 .01 0;\
                    0 0 0 0 .01')

  Q = numpy.matrix('.00001 0 0 0 0;\
                    0 .00001 0 0 0;\
                    0 0 .0001 0 0;\
                    0 0 0 .0001 0;\
                    0 0 0 0 .0001')

  R = numpy.matrix('.01 0 0 0 0;\
                    0 .01 0 0 0;\
                    0 0 .01 0 0;\
                    0 0 0 .01 0;\
                    0 0 0 0 .01')

  kalman_filter = Kalman(A,B,H,X,P,Q,R)
  kx = []
  ky = []

  # Graph results
  for i in range(len(data[0])):
    omega = .44 * tan(data[odom][i])
    measure = numpy.matrix([[data[gps_x][i]], [data[gps_y][i]], [.44], [data[imu][i]], [omega]])
    kalman_filter.Step(measure)
    kx.append(kalman_filter.GetCurrentState()[0,0])
    ky.append(kalman_filter.GetCurrentState()[1,0])



  pylab.plot(data[gps_x], data[gps_y], '-', kx, ky, '-', data[odom_x], data[odom_y])
  pylab.xlabel('time')
  pylab.ylabel('Position')
  pylab.title('Kalman Filter Data')
  pylab.legend(('Measured', 'Kalman Filter','Odomentry'))
  pylab.show()


if __name__ == '__main__':
  main()