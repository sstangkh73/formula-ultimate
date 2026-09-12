# Control Hardware Realization V1

Thai companion: `CONTROL_HARDWARE_REALIZATION_V1.th.md`

Status: Implemented by Work 122 as bounded Level-0 reference evidence.

## Hardware, paths and finite opportunity

This contract pins exact Work 119 actuator and Work 120 supply evidence. One sampled scalar sensor-controller-actuator reference includes two sensors, a controller, harness, four connectors, six mounts and an actuator interface. Every sensor/hardware record is explicitly synthetic/estimated; no signal is represented as measured.

The signal graph requires sensor-to-controller and controller-to-actuator edges. Sample interval is `0.01 s`, duration `2 s`, registered latency two samples, deterministic noise amplitude `0.01`, actuator authority `200 N*m`, and charged supply `100000 J`. Actuator authority and supply cannot exceed upstream evidence.

Common and adapted modes each receive exactly four gain evaluations. Failed or poor evaluations remain charged. A parameter that does not enter sensing, control, actuation or plant equations must preserve the exact trace identity and cannot count as useful adaptation.

## Controls and limitations

Sensor dropout, disconnected signal, exhausted supply, actuator saturation, increased delay and noncausal mutation are mandatory controls. Faults and finite limits remain observable in histories and counters. Hardware mass and run energy are explicit outputs.

Plant, noise, delay and hardware specifications are synthetic. Ideal full-state observation, advanced electronics, measured noise/delay, multivariable stability, EMI/fault safety, safety-critical certification and physical validation remain unresolved.
