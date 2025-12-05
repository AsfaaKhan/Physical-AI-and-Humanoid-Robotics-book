# Mermaid Diagram Examples

This file demonstrates how to include Mermaid diagrams in the book for illustrating architectural concepts.

## ROS2 Architecture Diagram

```mermaid
graph TD
    A[ROS2 Node] --> B[DDS Middleware]
    C[ROS2 Node] --> B
    B --> D[Topics]
    B --> E[Services]
    B --> F[Actions]
    D --> G[Publisher]
    D --> H[Subscriber]
```

## Humanoid Robot Control Architecture

```mermaid
graph LR
    A[High-level Planner] --> B[Task Planner]
    B --> C[Motion Planner]
    C --> D[Whole-Body Controller]
    D --> E[Joint Controllers]
    E --> F[Robot Hardware]
    F --> G[Sensors]
    G --> A
```

## VLA System Architecture

```mermaid
graph TB
    A[Visual Input] --> B[Vision Encoder]
    C[Language Input] --> D[Language Encoder]
    B --> E[Fusion Module]
    D --> E
    E --> F[Action Decoder]
    F --> G[Robot Actions]
```

These diagrams can be embedded directly in the documentation to illustrate complex concepts and system architectures.