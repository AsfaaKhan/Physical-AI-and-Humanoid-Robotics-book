---
sidebar_label: SDF and URDF Import
---

# SDF and URDF Import

Simulation Description Format (SDF) and Unified Robot Description Format (URDF) are the two primary formats for describing robots in simulation environments. Understanding how to work with both formats is crucial for effective robotics simulation.

## SDF vs URDF

While URDF is XML-based and primarily used in ROS, SDF is designed specifically for Gazebo simulation. SDF supports features that URDF doesn't, such as:

- Multi-body models in a single file
- Simulation-specific properties
- More complex joint types
- World composition

## Converting URDF to SDF

Most robots are described in URDF format, but Gazebo works with SDF. The conversion is typically handled automatically when launching Gazebo with ROS2, but understanding the process is important:

- Joint and link properties are preserved
- Visual and collision properties are maintained
- Inertial properties are transferred
- Gazebo-specific extensions can be added

## Import Best Practices

- Validate URDF files before import using check_urdf
- Use xacro preprocessing for complex URDFs
- Add Gazebo-specific plugins for sensors and actuators
- Include appropriate physical properties for realistic simulation
- Test import with simple visualizations before complex scenarios

## Troubleshooting Common Issues

- Joint limits not preserved: Add Gazebo-specific extensions
- Physics issues: Verify inertial properties
- Visual artifacts: Check mesh file paths and formats
- Performance problems: Simplify collision geometries where possible