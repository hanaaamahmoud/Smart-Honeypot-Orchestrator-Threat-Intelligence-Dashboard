# Session Reconstruction

## 1. Overview
Session Reconstruction is the process of grouping individual network events into logical sessions. Instead of treating every log row as a separate event, related events are connected together to represent the complete activity of a user or attacker during a session.

## 2. Objective
The main goal was to:
* Group related network events into sessions.
* Preserve the original event information.
* Create a unique `reconstructed_session_id` for each reconstructed session.
* Keep the original `raw_session_id` for traceability.
* Prepare session-level data for the next stages of the project.

## 3. Process
The notebook performed the following steps:
1. Loaded the normalized network events.
2. Examined the existing session identifiers and event information.
3. Ordered events chronologically.
4. Analyzed event sequences to identify related activities.
5. Reconstructed logical sessions from the individual events.
6. Assigned a `reconstructed_session_id`.
7. Preserved the original `raw_session_id`.
8. Checked the resulting sessions for ambiguous cases.

## 4. Ambiguous Cases
Some sessions contained unusual patterns, such as:
* Multiple source IP addresses.
* Multiple destination IP addresses.

These cases were not automatically split or merged when the relationship between events was unclear. This helped avoid incorrect session reconstruction and preserved the integrity of the original data.

## 5. Output
The result of this stage was a session-level representation of the network events, where related events can be analyzed as a single session. 

This reconstructed session data was then used in the following stages:
`Validation` → `Feature Engineering` → `Machine Learning` → `Dashboard / Session Replay`

## 6. Key Result
Session Reconstruction transformed individual network events into structured sessions while maintaining traceability to the original data. This provided the foundation for analyzing attacker behavior and building session-level features in the next stages.
