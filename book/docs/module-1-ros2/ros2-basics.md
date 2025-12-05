---
sidebar_label: ROS2 Basics
---

# ROS2 Basics

Robot Operating System 2 (ROS2) is a flexible framework for writing robot software. It is a collection of tools, libraries, and conventions that aim to simplify the task of creating complex and robust robot behavior across a wide variety of robotic platforms.

## Architecture

ROS2 uses a distributed architecture based on nodes that communicate through topics, services, and actions. Unlike ROS1, ROS2 is built on DDS (Data Distribution Service) for communication, providing better support for real-time systems and multi-robot applications.

## Key Concepts

- **Nodes**: Processes that perform computation
- **Topics**: Named buses over which nodes exchange messages
- **Services**: Synchronous request/response communication
- **Actions**: Asynchronous request/response with feedback and goal preemption
- **Parameters**: Configuration values that can be changed at runtime

## Installation

ROS2 is distributed in multiple distributions, with the latest being Rolling Ridley. For production systems, LTS (Long Term Support) distributions like Humble Hawksbill are recommended.

## Core Tools

ROS2 provides a rich set of command-line tools for debugging, monitoring, and controlling robotic systems. These include ros2 run, ros2 launch, ros2 topic, ros2 service, and many others.