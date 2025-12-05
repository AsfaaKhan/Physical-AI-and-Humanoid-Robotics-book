---
sidebar_label: ROS2 Services and Actions
---

# ROS2 Services and Actions

ROS2 provides two additional communication patterns beyond topics: services for request-response communication and actions for long-running tasks with feedback.

## Services

Services implement a synchronous request-response pattern where a client sends a request and waits for a response from a server. This pattern is ideal for operations that have a clear beginning and end, such as triggering a calibration procedure or requesting robot state.

### Service Implementation
- Clients use `node.create_client()` to call services
- Servers use `node.create_service()` to provide services
- Services use request/response message pairs defined in .srv files
- Services block the calling thread until the response is received

## Actions

Actions are designed for long-running operations that may take seconds, minutes, or longer. They provide feedback during execution and can be preempted if needed.

### Action Features
- **Goal**: Request sent to start an action
- **Feedback**: Continuous updates during execution
- **Result**: Final outcome when the action completes
- **Preemption**: Ability to cancel or replace running goals
- **Status**: Track the current state of the action

### Action Implementation
Actions use the actionlib framework with .action definition files. In Python, action clients use `action_msgs` and action servers implement the action interface with appropriate callbacks.

## When to Use Each

- **Topics**: For continuous data streams (sensors, state)
- **Services**: For discrete operations with quick responses
- **Actions**: For complex operations requiring feedback or cancellation