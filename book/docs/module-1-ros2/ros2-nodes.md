---
sidebar_label: ROS2 Nodes
---

# ROS2 Nodes

A ROS2 node is the fundamental building block of a ROS2 program. Nodes are processes that perform computation and communicate with other nodes through topics, services, actions, and parameters.

## Node Structure

Every ROS2 node consists of:

- A unique name within the ROS2 domain
- One or more publishers and/or subscribers
- One or more service clients and/or servers
- One or more action clients and/or servers
- A node lifecycle (construct, configure, activate, deactivate, cleanup, shutdown)

## Creating Nodes

Nodes are typically created by subclassing rclpy.Node or rclcpp::Node in Python and C++ respectively. The node constructor requires a name and can accept additional options like namespace and parameter overrides.

## Node Lifecycle

ROS2 introduces a more sophisticated lifecycle compared to ROS1. Nodes can be configured, activated, deactivated, and cleaned up in a controlled manner, which is essential for complex robotic systems requiring graceful startup and shutdown procedures.

## Best Practices

- Use meaningful node names that reflect their function
- Implement proper error handling and recovery
- Use parameters for configuration rather than hardcoding values
- Follow naming conventions for topics, services, and parameters
- Implement lifecycle management for production systems