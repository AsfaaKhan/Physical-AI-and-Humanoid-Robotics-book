---
sidebar_label: URDF for Humanoids
---

# URDF for Humanoids

Unified Robot Description Format (URDF) is an XML format used in ROS to describe robot models. For humanoid robots, URDF becomes particularly important due to the complex kinematic structures involved.

## URDF Structure

A URDF file contains:
- **Links**: Rigid bodies with physical properties (mass, inertia, visual, collision)
- **Joints**: Connections between links with kinematic properties (type, limits, origin)
- **Materials**: Visual properties for rendering
- **Gazebo plugins**: Simulation-specific extensions

## Humanoid-Specific Considerations

Humanoid robots have unique requirements in their URDF descriptions:

- **Bipedal structure**: Two legs with appropriate degrees of freedom
- **Balance constraints**: Accurate center of mass and inertia properties
- **Anthropomorphic proportions**: Realistic limb lengths and joint configurations
- **Sensor placements**: IMU, force/torque sensors in feet, cameras in head

## Kinematic Chains

Humanoid robots typically have multiple kinematic chains:
- Left and right arms (for manipulation)
- Left and right legs (for locomotion)
- Spine and head (for orientation)

## Best Practices

- Use xacro for complex URDFs to avoid repetition
- Validate kinematic models before simulation
- Include accurate inertial properties for realistic simulation
- Use appropriate joint limits based on physical constraints
- Consider adding collision-free zones for safe operation