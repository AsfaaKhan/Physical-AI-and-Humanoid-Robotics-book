---
sidebar_label: ROS2 Control
---

# ROS2 Control

ROS2 Control is the standard framework for hardware interface and controller management in ROS2. For humanoid robots, it provides the essential infrastructure for real-time control of joints and actuators.

## Architecture

ROS2 Control follows a hardware interface and controller manager architecture:

- **Hardware Interface**: Abstracts communication with physical or simulated hardware
- **Controller Manager**: Manages lifecycle of controllers
- **Controllers**: Implement specific control algorithms (position, velocity, effort, etc.)
- **Resource Manager**: Tracks and allocates hardware resources

## Hardware Abstraction

The framework provides a unified interface for different types of hardware:
- Physical robots with real actuators
- Simulation environments (Gazebo, Webots, etc.)
- Hardware-in-the-loop systems

## Controller Types

Common controllers for humanoid robots include:
- **Joint Trajectory Controller**: Executes smooth trajectories for joint sets
- **Position/Velocity/Effort Controllers**: Direct control of individual joints
- **Forward Command Controllers**: Passes commands directly to hardware
- **IMU Sensor Controller**: Reads sensor data from hardware

## Real-time Considerations

ROS2 Control is designed for real-time performance, which is critical for humanoid balance and stability. Controllers run at high frequencies (typically 100Hz-1kHz) to ensure responsive control.

## Configuration

Controllers are configured using YAML files that specify:
- Controller type and parameters
- Joint names and mappings
- Hardware interfaces to use
- Real-time constraints and safety limits