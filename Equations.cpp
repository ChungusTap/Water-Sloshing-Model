#include <cmath>

// Constants
const double PI = 3.141592653589793;
const double g = 9.81; 
const double length = 100.0; // Length of the pendulum (pixels)
const double dt = 0.005; // Time step (s)

// Function to update the pendulum's angle and angular velocity using a damped pendulum approach
extern "C" void updatePendulum(double &angle, double &angularVelocity, double pivotX, double pivotXPrev, double pivotXPrev2) {
    double pivotXAcc = ((pivotX - 2 * pivotXPrev + pivotXPrev2) / (dt * dt)) / 4;
    double damping = 0.5; // Damping factor
    double angularAcceleration = -(g / length) * sin(angle) - (pivotXAcc / length) * cos(angle) - damping * angularVelocity;
    angularVelocity += angularAcceleration * dt;
    angle += angularVelocity * dt;
}


// Recompile: g++ -shared -o libpendulum.so -fPIC Equations.cpp





