---
sidebar_label: ROS2 Topics
---

# ROS2 Topics

Topics in ROS2 provide a publish-subscribe communication mechanism that enables asynchronous message passing between nodes. This decoupled communication pattern is fundamental to ROS2's distributed architecture.

## Message Passing

Topics use a one-to-many communication pattern where publishers send messages to a topic and multiple subscribers can receive those messages. This pattern promotes loose coupling between nodes and enables flexible system architectures.

## Quality of Service (QoS)

ROS2 introduces QoS profiles that allow fine-tuning of communication behavior. Key QoS settings include:

- **Reliability**: Best effort vs. reliable delivery
- **Durability**: Volatile vs. transient local (replay last message to new subscribers)
- **History**: Keep all messages vs. keep last N messages
- **Deadline**: Maximum time between consecutive messages
- **Liveliness**: How to detect if a publisher is alive

## Creating Publishers and Subscribers

In Python, publishers are created using `node.create_publisher()` and subscribers using `node.create_subscription()`. Both require specifying the message type, topic name, and QoS profile.

## Common Patterns

Topics are commonly used for sensor data distribution, robot state publishing (tf, joint states), and command interfaces. Understanding QoS settings is crucial for reliable communication in real-time robotic systems.