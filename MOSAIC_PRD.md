MOSAIC — Product Requirements Document

Multi-Model Orchestration of Signals Across Integrated Channels

Project Type: Final-Year Major Project
Domain: Artificial Intelligence / Machine Learning / Multimodal Signal Analysis
Document Type: Product Requirements Document (PRD)
Version: 1.0
Status: Draft / Baseline
Primary Modalities: Physiological Signals, Audio, Computer Vision
Primary Objective: Experimental multimodal deception-analysis/classification system

Table of Contents

1. Document Control

1.1 Document Purpose
1.2 Document Status
1.3 Version History
1.4 Authors and Contributors
1.5 Intended Audience
1.6 Related Documents
1.7 Terminology and Conventions

2. Executive Summary

2.1 Product Overview
2.2 Problem Statement
2.3 Proposed Solution
2.4 Project Vision
2.5 Project Mission
2.6 Expected Outcome
2.7 Product Philosophy

3. Background and Context

3.1 Motivation
3.2 Academic Context
3.3 Problem Domain
3.4 Existing Approach
3.5 Limitations of Single-Modality Systems
3.6 Need for Multimodal Analysis
3.7 Research Opportunity

4. Product Vision

4.1 Vision Statement
4.2 Product Goals
4.3 Long-Term Vision
4.4 Product Principles
4.5 Success Definition

5. Problem Definition

5.1 Core Problem
5.2 User Problem
5.3 Technical Problem
5.4 Data Problem
5.5 Multimodal Synchronization Problem
5.6 Classification Problem
5.7 Reliability Problem
5.8 Ethical Problem

6. Objectives and Goals

6.1 Primary Objectives
6.2 Secondary Objectives
6.3 Academic Objectives
6.4 Technical Objectives
6.5 User Objectives
6.6 Measurable Goals
6.7 Non-Goals

7. Scope

7.1 In-Scope
7.2 Out-of-Scope
7.3 MVP Scope
7.4 Extended Scope
7.5 Future Scope
7.6 Scope Boundaries

8. Target Users and Stakeholders

8.1 Primary Users
8.2 Secondary Users
8.3 Project Team
8.4 Faculty / Evaluators
8.5 Dataset Contributors
8.6 Stakeholder Responsibilities
8.7 Stakeholder Expectations

9. User Personas

9.1 Research Student
9.2 Experiment Operator
9.3 Participant
9.4 Faculty Evaluator
9.5 ML/Data Analyst

10. User Stories

10.1 Participant Stories
10.2 Experiment Operator Stories
10.3 Researcher Stories
10.4 ML Engineer Stories
10.5 Faculty/Evaluator Stories

11. User Journey

11.1 Experiment Preparation
11.2 Participant Registration
11.3 Baseline Collection
11.4 Question/Trial Presentation
11.5 Signal Collection
11.6 Processing
11.7 Prediction
11.8 Result Review
11.9 Experiment Completion

12. Product Concept

12.1 Product Overview
12.2 System Components
12.3 Multimodal Pipeline
12.4 Signal Channels
12.5 Model Layer
12.6 Fusion Layer
12.7 Results Layer

13. Product Architecture — High Level

13.1 Architecture Overview
13.2 Data Acquisition Layer
13.3 Data Processing Layer
13.4 Feature Layer
13.5 Individual Model Layer
13.6 Fusion Layer
13.7 Evaluation Layer
13.8 Presentation Layer
13.9 External Interfaces

14. Physiological Signal Channel

14.1 Purpose
14.2 Signal Sources
14.3 MAX30102 Role
14.4 PPG Data
14.5 Heart Rate
14.6 SpO₂
14.7 Pulse Features
14.8 Signal Quality
14.9 Baseline Measurement
14.10 Physiological Feature Requirements
14.11 Physiological Limitations

15. Audio Channel

15.1 Purpose
15.2 Microphone Input
15.3 Speech Capture
15.4 Speech Segmentation
15.5 Response Latency
15.6 Pauses
15.7 Hesitation
15.8 Stuttering
15.9 Pitch
15.10 Voice Quality
15.11 MFCC and Spectral Features
15.12 Audio Quality Requirements

16. Computer Vision Channel

16.1 Purpose
16.2 Camera Input
16.3 Face Detection
16.4 Facial Landmarks
16.5 Eye Features
16.6 Blink Detection
16.7 Gaze Analysis
16.8 Head Pose
16.9 Facial Expressions
16.10 Mouth Movement
16.11 Facial Motion
16.12 Video Quality Requirements

17. Multimodal Synchronization

17.1 Need for Synchronization
17.2 Participant ID
17.3 Session ID
17.4 Trial ID
17.5 Question ID
17.6 Timestamp Requirements
17.7 Cross-Modality Alignment
17.8 Missing Modality Handling

18. Dataset Requirements

18.1 Dataset Philosophy
18.2 Dataset Structure
18.3 Participant Requirements
18.4 Trial Requirements
18.5 Ground Truth
18.6 Label Requirements
18.7 Feature Requirements
18.8 Raw Data Requirements
18.9 Derived Data Requirements
18.10 Metadata Requirements
18.11 Missing Data
18.12 Data Quality
18.13 Data Balance
18.14 Dataset Versioning

19. Dataset Schema

19.1 Participant Metadata
19.2 Experiment Metadata
19.3 Question Metadata
19.4 Physiological Columns
19.5 Audio Columns
19.6 Vision Columns
19.7 Temporal Columns
19.8 Quality Columns
19.9 Ground-Truth Columns
19.10 Model Output Columns

20. Data Pipeline Requirements

20.1 Data Ingestion
20.2 Validation
20.3 Cleaning
20.4 Normalization
20.5 Feature Extraction
20.6 Feature Validation
20.7 Dataset Assembly
20.8 Dataset Splitting
20.9 Leakage Prevention

21. Machine Learning Requirements

21.1 ML Objectives
21.2 Modality-Specific Models
21.3 Physiological Model
21.4 Audio Model
21.5 Vision Model
21.6 Fusion Model
21.7 Training Requirements
21.8 Validation Requirements
21.9 Testing Requirements
21.10 Reproducibility

22. Fusion Requirements

22.1 Purpose
22.2 Early Fusion
22.3 Late Fusion
22.4 Model-Level Fusion
22.5 Missing Modality Handling
22.6 Confidence Estimation
22.7 Fusion Output
22.8 Comparison Requirements

23. Prediction and Result Requirements

23.1 Prediction Output
23.2 Probability
23.3 Confidence
23.4 Modality Contributions
23.5 Result Categories
23.6 Uncertain Results
23.7 Explainability

24. User Interface Requirements

24.1 UI Goals
24.2 Dashboard
24.3 Participant Screen
24.4 Experiment Screen
24.5 Signal Monitoring
24.6 Processing Status
24.7 Results Screen
24.8 Dataset Screen
24.9 Model Evaluation Screen

25. Experiment Management

25.1 Experiment Creation
25.2 Participant Management
25.3 Session Management
25.4 Question Management
25.5 Trial Management
25.6 Recording Management
25.7 Experiment Completion

26. Hardware Requirements

26.1 ESP32-C3
26.2 MAX30102
26.3 Microphone
26.4 Camera
26.5 Power System
26.6 Communication
26.7 Hardware Reliability
26.8 Hardware Safety
26.9 Hardware Optionality

27. Software Requirements

27.1 Development Environment
27.2 Backend
27.3 Data Processing
27.4 ML Environment
27.5 Frontend
27.6 Storage
27.7 API Requirements
27.8 Logging

28. Functional Requirements

28.1 FR-001 Participant Registration
28.2 FR-002 Experiment Creation
28.3 FR-003 Trial Creation
28.4 FR-004 Signal Collection
28.5 FR-005 Audio Collection
28.6 FR-006 Video Collection
28.7 FR-007 Data Validation
28.8 FR-008 Feature Extraction
28.9 FR-009 Model Inference
28.10 FR-010 Fusion
28.11 FR-011 Result Generation
28.12 FR-012 Reporting

29. Non-Functional Requirements

29.1 Performance
29.2 Reliability
29.3 Availability
29.4 Scalability
29.5 Maintainability
29.6 Usability
29.7 Accessibility
29.8 Portability
29.9 Observability

30. Privacy and Security

30.1 Privacy Principles
30.2 Consent
30.3 Participant Identification
30.4 Audio Privacy
30.5 Video Privacy
30.6 Data Storage
30.7 Access Control
30.8 Data Retention
30.9 Data Deletion
30.10 Anonymization

31. Ethical Requirements

31.1 Experimental Nature
31.2 No Guaranteed Lie Detection
31.3 Avoiding Harmful Conclusions
31.4 Participant Consent
31.5 Bias
31.6 False Positives
31.7 False Negatives
31.8 Human Oversight
31.9 Appropriate Use

32. Bias and Fairness

32.1 Demographic Variation
32.2 Language Variation
32.3 Accent Variation
32.4 Lighting Variation
32.5 Physiological Variation
32.6 Model Bias
32.7 Fairness Evaluation

33. Performance Metrics

33.1 Accuracy
33.2 Precision
33.3 Recall
33.4 F1 Score
33.5 ROC-AUC
33.6 Confusion Matrix
33.7 Calibration
33.8 Per-Modality Performance
33.9 Fusion Performance
33.10 Error Analysis

34. Experiment and Evaluation Plan

34.1 Baseline Experiment
34.2 Physiological-Only Experiment
34.3 Audio-Only Experiment
34.4 Vision-Only Experiment
34.5 Multimodal Experiment
34.6 Ablation Study
34.7 Cross-Participant Evaluation
34.8 Generalization Testing

35. Error Handling

35.1 Missing Sensor
35.2 Poor PPG
35.3 Poor Audio
35.4 No Face Detected
35.5 Multiple Faces
35.6 Missing Data
35.7 Model Failure
35.8 Fusion Failure
35.9 System Failure

36. Logging and Monitoring

36.1 System Logs
36.2 Sensor Logs
36.3 Processing Logs
36.4 Model Logs
36.5 Error Logs
36.6 Audit Information

37. Reporting

37.1 Participant Report
37.2 Trial Report
37.3 Session Report
37.4 Model Report
37.5 Dataset Report
37.6 Research Report

38. Accessibility and Usability

38.1 Operator Usability
38.2 Participant Usability
38.3 Visual Design
38.4 Error Messaging
38.5 Minimal Cognitive Load

39. Security Threat Model

39.1 Threats
39.2 Attack Surface
39.3 Data Exposure
39.4 Unauthorized Access
39.5 Data Tampering
39.6 Model Manipulation

40. Risks and Mitigation

40.1 Hardware Risks
40.2 Dataset Risks
40.3 ML Risks
40.4 Integration Risks
40.5 Privacy Risks
40.6 Schedule Risks
40.7 Research Risks

41. Dependencies

41.1 Hardware Dependencies
41.2 Dataset Dependencies
41.3 Software Dependencies
41.4 Team Dependencies
41.5 External Dependencies

42. Constraints

42.1 Academic Timeline
42.2 Hardware Budget
42.3 Dataset Size
42.4 Computational Resources
42.5 Team Resources
42.6 Data Availability

43. Project Milestones

43.1 Phase 1 — Requirements
43.2 Phase 2 — Data Pipeline
43.3 Phase 3 — Hardware
43.4 Phase 4 — Audio
43.5 Phase 5 — Vision
43.6 Phase 6 — Models
43.7 Phase 7 — Fusion
43.8 Phase 8 — Evaluation
43.9 Phase 9 — Final Demonstration

44. Acceptance Criteria

44.1 Product-Level Acceptance
44.2 Hardware Acceptance
44.3 Dataset Acceptance
44.4 Model Acceptance
44.5 Fusion Acceptance
44.6 UI Acceptance
44.7 Documentation Acceptance

45. Quality Assurance

45.1 Data QA
45.2 Hardware QA
45.3 Software QA
45.4 ML QA
45.5 Integration QA
45.6 User Acceptance Testing

46. Research Questions

46.1 Primary Research Question
46.2 Secondary Questions
46.3 Hypotheses
46.4 Experimental Comparisons

47. Future Enhancements

47.1 Additional Physiological Sensors
47.2 Additional Audio Features
47.3 Advanced Vision
47.4 Additional Modalities
47.5 Real-Time Processing
47.6 Improved Fusion

48. Deliverables

48.1 Hardware Prototype
48.2 Dataset Pipeline
48.3 ML Models
48.4 Fusion System
48.5 Application
48.6 Reports
48.7 Demonstration

49. Glossary

49.1 AI
49.2 ML
49.3 PPG
49.4 SpO₂
49.5 HR
49.6 HRV
49.7 MFCC
49.8 CNN
49.9 LSTM
49.10 Fusion
49.11 Ground Truth
49.12 Trial
49.13 Modality

50. Appendices

A. Proposed Data Dictionary
B. Requirement ID Convention
C. Sample Trial Lifecycle
D. Sample Dataset Structure
E. Risk Matrix
F. Acceptance Checklist
G. Ethical Disclaimer
H. Project Assumptions

1. Document Control

1.1 Document Purpose

This Product Requirements Document defines the complete product requirements for MOSAIC — Multi-Model Orchestration of Signals Across Integrated Channels.

The purpose of this document is to establish a common understanding among all project stakeholders regarding:

what MOSAIC is;

why the system is being developed;

what problem it addresses;

who will use it;

what capabilities it must provide;

what data it requires;

what the major system components are;

what the expected outputs are;

how the product will be evaluated;

what limitations and ethical considerations apply;

what is included and excluded from the project scope.

This document serves as the baseline product specification for the entire project.

All future technical and implementation decisions should be evaluated against the requirements defined here.

The PRD intentionally focuses on product behavior and requirements rather than implementation details.

For example, this document specifies that MOSAIC must analyze physiological signals, but it does not mandate a particular machine-learning architecture. Similarly, it specifies that audio must be analyzed for speech-related characteristics, but it does not prescribe a particular programming library.

Those decisions will be documented separately in the Implementation and Technical Design Document.

1.2 Product Name

MOSAIC

Multi-Model Orchestration of Signals Across Integrated Channels

The name represents the central concept of the project:

Multi-Model — Multiple specialized AI/ML models operate on different signal modalities.

Orchestration — The outputs of individual models are coordinated and combined.

Signals — The system processes physiological, audio, and visual information.

Across — The system does not analyze modalities in isolation only; it establishes relationships between them.

Integrated — Different information channels are brought together within one system.

Channels — Each modality represents a separate signal/data channel.

1.3 Product Type

MOSAIC is an:

Experimental multimodal AI-based signal analysis and classification platform.

The system is intended primarily for:

academic research;

machine-learning experimentation;

multimodal signal analysis;

comparative model evaluation;

final-year project demonstration.

It is not intended to function as a legally or medically certified lie-detection system.

1.4 Document Status

Current Status: Product Requirements Baseline

The PRD may be updated during the project when:

project scope changes;

new requirements are approved;

hardware decisions change;

dataset characteristics become known;

research findings require modification;

technical constraints affect product requirements.

Changes should be recorded in the version history.

1.5 Version History

1.6 Intended Audience

This document is intended for:

Project Team

To understand the complete product requirements and ensure different modules are developed consistently.

Machine Learning Team

To understand:

required inputs;

expected outputs;

ground-truth requirements;

evaluation requirements;

multimodal fusion requirements.

Hardware Team

To understand:

physiological signal requirements;

expected sensor data;

acquisition requirements;

quality requirements.

Audio/CV Team

To understand the expected characteristics and outputs of the audio and vision channels.

UI/Frontend Team

To understand:

user workflows;

experiment management;

monitoring requirements;

result presentation requirements.

Faculty Guide

To review:

academic objectives;

research scope;

system requirements;

evaluation methodology;

ethical boundaries.

Project Evaluators

To understand the intended functionality and criteria against which the final project should be evaluated.

1.7 Document Boundaries

This document defines WHAT the product should do.

It does not define every detail of HOW the product will be implemented.

For example:

PRD

The system shall collect physiological signals associated with each experimental trial.

Implementation Document

Will later define:

Which ESP32 firmware, sensor library, sampling configuration, communication protocol, data format, and Python processing pipeline will be used.

This separation prevents implementation decisions from unnecessarily changing the product requirements.

2. Executive Summary

2.1 Product Overview

MOSAIC is a multimodal artificial-intelligence system designed to study whether combining different behavioral and physiological signals can improve the experimental classification of truthful and deceptive responses.

The system integrates three primary information channels:

1. Physiological Channel

This channel captures physiological signals associated with the participant's response.

The initial concept includes:

photoplethysmography (PPG);

heart rate;

SpO₂;

pulse-related features;

signal-quality information.

A potential hardware configuration includes a MAX30102 sensor connected to an ESP32-C3-based acquisition device.

2. Audio Channel

The audio channel analyzes characteristics of the participant's spoken response.

Potential characteristics include:

response latency;

speaking rate;

pauses;

hesitation;

filler words;

repetition;

stuttering-related characteristics;

pitch;

voice energy;

jitter;

shimmer;

spectral characteristics;

MFCC features.

3. Computer Vision Channel

The computer-vision channel analyzes observable facial and head-related behavior.

Potential characteristics include:

face detection;

eye movement;

blink behavior;

gaze;

head pose;

facial movement;

mouth movement;

expression-related features.

Each modality is processed independently before the information is combined through a multimodal fusion mechanism.

2.2 Core Product Concept

The central architecture is:

MOSAIC

│

┌───────────┼───────────┐

│ │ │

▼ ▼ ▼

Physiological Audio Vision

Channel Channel Channel

│ │ │

▼ ▼ ▼

Physio Model Audio Model Vision Model

│ │ │

└───────────┼───────────┘

▼

Fusion Engine

│

▼

Final Classification

│

▼

Evaluation

The primary research objective is not simply to create three independent models.

The important component is determining whether orchestrating information from multiple channels produces a meaningful improvement over individual modality models.

2.3 Problem Being Addressed

Human responses to questions can contain multiple observable characteristics.

For example, during an experimental response, a participant may exhibit:

changes in physiological measurements;

increased hesitation;

changes in speech rhythm;

changes in vocal characteristics;

altered gaze;

increased blinking;

facial movement;

changes in head movement.

However, none of these characteristics independently proves deception.

A change in heart rate could be caused by anxiety.

A pause could be caused by thinking.

A gaze shift could be normal behavior.

A voice change could be caused by fatigue.

Therefore, a system relying on one signal may produce unreliable classifications.

MOSAIC addresses this by treating the problem as a multimodal signal-analysis problem.

2.4 Proposed Solution

MOSAIC shall:

Collect or ingest multimodal data.

Associate data with participants and experimental trials.

Validate signal quality.

Preprocess the data.

Extract relevant features.

Analyze each modality independently.

Generate modality-specific predictions.

Combine modality information.

Produce a final experimental classification.

Evaluate the result against experimentally established ground truth.

2.5 Expected Outcome

The expected outcome is a working research prototype capable of demonstrating:

Whether multimodal signal integration provides measurable advantages over individual signal modalities for the experimental classification task.

The final project should therefore be capable of presenting comparative results such as:

The values will be determined using the final curated dataset and evaluation methodology.

2.6 Product Philosophy

MOSAIC shall follow five principles:

Multimodality

No single signal should be treated as sufficient evidence of deception.

Modularity

Each signal channel should be independently replaceable or improved.

Measurability

Claims about performance should be supported by quantitative evaluation.

Transparency

The system should distinguish ground truth, model prediction, probability, confidence, and uncertainty.

Responsible AI

The system should not present experimental predictions as absolute determinations of truth or deception.

3. Background and Context

3.1 Motivation

Communication is a complex process involving multiple observable signals.

When individuals respond to questions, information may be represented through:

spoken language;

voice characteristics;

facial behavior;

eye behavior;

physiological responses;

temporal response patterns.

Traditional machine-learning approaches often focus on one modality.

For example:

Audio-only

or:

Facial-only

or:

Physiological-only

Such systems may fail to capture information that exists in other channels.

MOSAIC is motivated by the hypothesis that combining complementary information sources may provide a more informative representation of an experimental response.

3.2 Academic Context

The project combines concepts from:

artificial intelligence;

machine learning;

signal processing;

digital signal analysis;

computer vision;

speech processing;

physiological signal processing;

multimodal learning;

data engineering;

human-computer interaction.

This makes MOSAIC a multidisciplinary project rather than a single-model machine-learning project.

3.3 Problem Domain

The project operates within the broader domain of behavioral and physiological signal analysis.

The system does not assume that behavioral signals have a one-to-one relationship with deception.

Instead, it investigates whether patterns in multiple signals can be associated with experimentally defined labels.

This distinction is essential.

The project therefore focuses on:

experimental classification based on multimodal observations

rather than:

absolute lie detection.

3.4 Existing Single-Modality Approaches

A single-modality system may use:

Physiological

Heart rate

SpO₂

PPG

HRV

Audio

Pitch

Pause

Speech rate

Stuttering

MFCC

Vision

Blink

Gaze

Facial movement

Head pose

These approaches provide useful information but can suffer from modality-specific limitations.

3.5 Limitations of Single-Modality Systems

Physiological limitations

Physiological changes can be influenced by:

stress;

anxiety;

physical activity;

environmental conditions;

individual baseline differences.

Audio limitations

Voice changes can result from:

nervousness;

language;

accent;

fatigue;

microphone quality;

background noise.

Vision limitations

Visual behavior can be influenced by:

lighting;

camera position;

facial characteristics;

normal conversational behavior;

fatigue;

camera quality.

Therefore, a single signal should not be treated as definitive.

3.6 Need for Multimodal Analysis

The motivation for multimodal analysis is that different channels can provide complementary information.

For example:

Physiological:

HR increased

Audio:

Response latency increased

Vision:

Gaze deviation increased

MOSAIC does not assume that these automatically mean deception.

Instead, the fusion model determines whether the combined pattern, based on the training data, is predictive of the experimental ground-truth label.

3.7 Research Opportunity

The primary research opportunity is to investigate whether:

Multimodal fusion produces better experimental classification performance than individual modality models.

This can be tested through controlled experiments comparing:

Physiology

Audio

Vision

Physiology + Audio

Physiology + Vision

Audio + Vision

All three

4. Product Vision

4.1 Vision Statement

MOSAIC aims to provide a modular, responsible, and experimentally measurable multimodal AI platform that orchestrates physiological, audio, and visual signals to study patterns associated with deceptive and truthful responses.

4.2 Product Vision Components

Unified

All modalities should operate as components of one platform.

Multimodal

The platform should support multiple signal channels.

Modular

Each modality should be independently developed and evaluated.

Intelligent

Machine-learning models should learn patterns from the curated dataset rather than relying solely on manually defined rules.

Research-oriented

The system should prioritize reproducible experiments and measurable results.

Responsible

The product should clearly communicate uncertainty and limitations.

4.3 Long-Term Vision

The architecture should allow additional modalities to be introduced later.

Potential future channels include:

ECG;

EEG;

additional physiological signals;

textual linguistic analysis;

thermal imaging;

additional speech representations.

The system should therefore not be architecturally dependent on exactly three modalities.

4.4 Product Principles

Principle 1 — No Single-Signal Determinism

No single signal should automatically determine the final classification.

Principle 2 — Evidence-Based Evaluation

Model performance must be evaluated using held-out data.

Principle 3 — Participant-Aware Evaluation

The evaluation strategy should prevent participant-specific information from creating misleading performance.

Principle 4 — Data Quality First

Poor-quality data should be identified before model inference.

Principle 5 — Ground Truth Independence

Ground truth must be established independently of the model prediction.

5. Problem Definition

5.1 Core Problem

The core problem addressed by MOSAIC is:

How can multiple heterogeneous physiological, audio, and visual signals be integrated into a unified machine-learning system for experimental classification of truthful and deceptive responses?

5.2 User Problem

Researchers and students working with multimodal datasets face several challenges:

heterogeneous data formats;

different sampling rates;

missing modalities;

inconsistent timestamps;

different feature scales;

signal noise;

participant variability;

limited datasets;

difficulty comparing models;

difficulty combining modality outputs.

MOSAIC aims to provide a unified framework for addressing these challenges.

5.3 Technical Problem

The technical problem consists of several interconnected challenges:

Data heterogeneity

Physiological signals are numerical time-series data.

Audio is waveform/time-frequency information.

Video is spatial-temporal information.

These representations are fundamentally different.

Temporal alignment

Signals must be associated with the same experimental trial.

Feature representation

Each modality requires appropriate feature extraction.

Model specialization

Different modalities may require different model architectures.

Fusion

Information from multiple models must be combined without allowing one modality to dominate unfairly.

Evaluation

The resulting system must be evaluated without data leakage.

5.4 Data Problem

The project depends heavily on the quality of the curated dataset.

Potential issues include:

missing values;

class imbalance;

poor-quality recordings;

inconsistent labels;

duplicate trials;

insufficient samples;

inconsistent feature definitions;

participant-specific bias.

The system therefore requires a formal dataset validation stage.

5.5 Multimodal Synchronization Problem

Each modality may have different temporal characteristics.

For example:

Physiological → continuous signal

Audio → response interval

Video → frame sequence

The system must determine which portions of each modality correspond to the same trial.

The common identifiers should therefore include:

participant_id

session_id

trial_id

question_id

5.6 Classification Problem

The system must learn a relationship between observed multimodal patterns and the experimental ground-truth labels.

The classification output should not be interpreted as absolute truth.

Instead:

Observed signals

↓

Learned patterns

↓

Probability

↓

Experimental classification

5.7 Reliability Problem

The system may encounter:

noisy signals;

missing sensors;

poor lighting;

audio interference;

face detection failure;

sensor disconnection.

The product must therefore distinguish between:

No evidence

and:

Evidence indicating a particular classification.

Missing data should not automatically be interpreted as a negative or positive signal.

5.8 Ethical Problem

Behavioral and physiological signals are influenced by many factors unrelated to deception.

Therefore, MOSAIC must not claim:

"This physiological response proves the participant lied."

Instead, the system should report:

"The model classified this trial as deceptive based on the learned multimodal patterns."

6. Objectives and Goals

6.1 Primary Objectives

Objective 1 — Develop a Multimodal Platform

Build a platform capable of handling physiological, audio, and visual information.

Objective 2 — Develop Independent Models

Create independent analytical pipelines for each modality.

Objective 3 — Develop Fusion

Combine modality information into a unified model.

Objective 4 — Compare Modalities

Measure the performance of each modality independently.

Objective 5 — Evaluate Multimodal Benefit

Determine whether fusion provides measurable improvement.

6.2 Secondary Objectives

The project should also:

establish a reusable data pipeline;

support dataset validation;

provide experiment-level traceability;

provide model evaluation;

support error analysis;

provide visual reporting;

document limitations.

6.3 Academic Objectives

MOSAIC should demonstrate knowledge of:

machine learning;

data preprocessing;

signal processing;

computer vision;

speech processing;

multimodal fusion;

model evaluation;

experimental design.

6.4 Technical Objectives

The technical system should be capable of:

accepting structured multimodal data;

processing heterogeneous inputs;

maintaining trial-level associations;

training independent models;

generating predictions;

combining predictions;

measuring performance.

6.5 User Objectives

The experiment operator should be able to:

Create an experiment.

Register a participant.

Start a session.

Conduct trials.

Collect/ingest multimodal data.

Validate data.

Process data.

Generate predictions.

Review results.

Generate evaluation reports.

6.6 Measurable Goals

The project should establish measurable targets for:

Dataset

number of participants;

number of trials;

class balance;

modality availability;

missing-data rate.

Model

accuracy;

precision;

recall;

F1;

ROC-AUC.

System

successful trial completion;

data integrity;

processing reliability;

reproducibility.

Exact target values should be finalized after the curated dataset is received.

6.7 Non-Goals

The project does not aim to:

replace professional investigators;

provide legal evidence;

provide medical conclusions;

identify criminal behavior;

determine personality;

perform continuous surveillance;

establish absolute truth.

7. Scope

7.1 In-Scope

Experiment Management

participant registration;

sessions;

questions;

trials.

Physiological

PPG;

heart rate;

SpO₂;

pulse-related features;

signal quality.

Audio

speech;

pauses;

hesitation;

stuttering;

pitch;

acoustic features.

Vision

face;

eyes;

gaze;

blink;

head pose;

facial movement.

Machine Learning

modality-specific models;

fusion model;

evaluation.

Data

ingestion;

validation;

preprocessing;

feature extraction;

synchronization;

versioning.

Reporting

dataset statistics;

model metrics;

comparison;

fusion results.

7.2 Out-of-Scope

The following are outside the initial product:

law-enforcement deployment;

clinical diagnosis;

automated interrogation;

identity recognition;

public surveillance;

autonomous decision-making about people;

employment screening;

financial eligibility decisions.

7.3 MVP Scope

The Minimum Viable Product should demonstrate:

Participant

↓

Experimental Trial

↓

3 Modalities

↓

Feature Processing

↓

3 Individual Models

↓

Fusion Model

↓

Experimental Classification

↓

Evaluation

The MVP does not require every possible feature.

It must instead demonstrate that the end-to-end multimodal concept works.

7.4 Extended Scope

After the MVP, the project may include:

additional features;

improved fusion;

real-time processing;

advanced visualization;

additional modalities;

stronger explainability.

7.5 Future Scope

Future versions may explore:

ECG;

EEG;

thermal imaging;

text analysis;

transformer-based models;

personalized baselines;

real-time multimodal inference.

8. Target Users and Stakeholders

8.1 Primary User — Experiment Operator

The experiment operator conducts the experiment.

Responsibilities include:

preparing the session;

registering participants;

ensuring signal quality;

initiating trials;

monitoring collection;

completing sessions.

The interface should minimize unnecessary complexity because the operator must focus on conducting the experiment rather than managing technical details.

8.2 Researcher

The researcher analyzes:

dataset quality;

feature distributions;

model performance;

fusion performance;

errors;

modality contributions.

The researcher requires access to detailed analytical information.

8.3 Participant

The participant interacts primarily with:

consent information;

questions;

response interface;

experiment instructions.

The participant should not be presented with technical ML information unnecessarily.

8.4 Faculty Guide

The faculty guide requires:

project objectives;

methodology;

progress;

evaluation;

limitations;

ethical considerations.

8.5 Project Evaluator

Evaluators should be able to understand:

the problem;

proposed solution;

architecture;

dataset;

models;

evaluation;

results;

limitations.

8.6 Stakeholder Expectations

All stakeholders should understand that MOSAIC is an academic experimental system.

The project should not be represented as a scientifically certified lie-detection device.

9. User Personas

9.1 Persona A — Research Student

Role: ML/AI project member

Goals

build models;

analyze datasets;

compare approaches;

improve performance;

generate research results.

Needs

clean datasets;

feature documentation;

reproducible experiments;

model metrics;

error analysis.

Pain Points

inconsistent data;

missing modalities;

unclear labels;

data leakage;

difficulty comparing experiments.

MOSAIC Solution

Provide a structured pipeline from:

Dataset

↓

Validation

↓

Processing

↓

Models

↓

Fusion

↓

Evaluation

9.2 Persona B — Experiment Operator

Goals

conduct experiments efficiently;

ensure data quality;

avoid technical errors.

Needs

simple interface;

clear instructions;

recording status;

sensor status;

trial status.

Pain Points

disconnected sensors;

unclear recording status;

failed trials.

MOSAIC Solution

Provide clear operational feedback.

9.3 Persona C — Participant

Goals

understand the experiment;

complete questions;

provide responses.

Needs

clear instructions;

understandable consent;

minimal technical interaction.

Pain Points

complicated interface;

unclear experiment status;

uncertainty about data collection.

MOSAIC Solution

Provide a simple participant workflow.

10. User Stories

User stories define what users should be able to accomplish.

10.1 Participant Stories

US-001 — Understand Experiment

As a participant, I want to understand what the experiment involves before participating so that I can provide informed consent.

Acceptance Criteria

experiment information is displayed;

data collection is explained;

participant can provide consent;

participant can decline participation.

US-002 — Answer Questions

As a participant, I want to receive experimental questions clearly so that I can respond naturally.

Acceptance Criteria

question is clearly displayed;

participant can provide a response;

response is associated with the correct trial.

US-003 — Complete a Trial

As a participant, I want to know when a trial starts and ends so that I understand the experiment flow.

10.2 Experiment Operator Stories

US-004 — Register Participant

As an experiment operator, I want to create a unique participant record so that all trials can be associated with the correct participant.

US-005 — Start Session

As an experiment operator, I want to start a session so that all trials performed during that session can be grouped together.

US-006 — Start Trial

As an experiment operator, I want to initiate a trial so that physiological, audio, and visual data are associated with the correct question.

US-007 — Monitor Data Quality

As an experiment operator, I want to see whether the required signal channels are available so that poor-quality trials can be identified.

10.3 Researcher Stories

US-008 — Validate Dataset

As a researcher, I want to validate a dataset before training so that invalid or incomplete data does not silently enter the model pipeline.

US-009 — Compare Models

As a researcher, I want to compare physiological, audio, vision, and fusion models so that I can determine whether multimodal integration improves performance.

US-010 — Analyze Errors

As a researcher, I want to inspect incorrect classifications so that I can understand the limitations of the system.

10.4 Faculty/Evaluator Stories

US-011 — Review Performance

As an evaluator, I want to see objective evaluation metrics so that I can assess the effectiveness of the proposed system.

US-012 — Review Multimodal Contribution

As an evaluator, I want to compare individual and multimodal performance so that I can determine whether the project's central multimodal concept provides measurable value.

These first 10 sections now give you the foundation of the full PRD. The next sections can continue with the same level of detail, particularly 11–20, where we'll define the complete user journey, product concept, high-level architecture, all three signal channels, synchronization, and the detailed dataset requirements.

Next 10

Absolutely. Continuing from Section 10, here are Sections 11–20 of the MOSAIC PRD. I’ll keep these strictly at PRD/product-requirement level—implementation details such as exact frameworks, model architectures, APIs, database schemas, and code structure can come later in the implementation document.

MOSAIC — Product Requirements Document

11. End-to-End Product Workflow

11.1 Overview

The complete MOSAIC workflow shall transform an experimental interaction into a structured multimodal prediction and evaluation result.

The high-level workflow is:

Experiment Setup

↓

Participant Registration

↓

Session Creation

↓

Baseline Collection

↓

Question/Trial Presentation

↓

Multimodal Data Collection

↓

Signal Quality Validation

↓

Data Synchronization

↓

Preprocessing

↓

Feature Extraction

↓

Modality-Specific Analysis

↓

Multimodal Fusion

↓

Final Experimental Classification

↓

Result Storage

↓

Evaluation & Reporting

11.2 Stage 1 — Experiment Setup

Before data collection begins, the operator shall configure the experiment.

The configuration may include:

experiment identifier;

experiment name;

experiment description;

number of participants;

question set;

trial configuration;

modality requirements;

recording duration;

baseline duration;

experimental conditions.

The system should ensure that the experiment configuration is complete before allowing data collection to begin.

11.3 Stage 2 — Participant Registration

Each participant shall receive a unique participant identifier.

The participant record should not rely solely on personally identifiable information.

The system should support pseudonymous identifiers such as:

P001

P002

P003

...

P300

The participant identifier shall remain consistent throughout the participant's experiment.

11.4 Stage 3 — Session Creation

A participant may have one or more sessions.

Each session should receive a unique session identifier.

Example:

Participant: P001

Session: S001

The session should contain:

session start time;

session end time;

participant identifier;

experiment identifier;

session status;

number of completed trials;

data-quality information.

11.5 Stage 4 — Baseline Collection

A baseline period should be collected before experimental questions whenever the experimental protocol supports it.

The purpose is to establish an approximate participant-specific reference.

Potential baseline measurements include:

heart rate;

SpO₂;

pulse characteristics;

voice characteristics;

facial/visual behavior.

The baseline should be associated with the participant and session.

11.6 Stage 5 — Trial Initialization

Each question-response interaction shall be treated as a separate trial.

Example:

Participant: P001

Session: S001

Trial: T001

Question: Q001

The trial should have clearly defined:

start;

question presentation;

response period;

end.

11.7 Stage 6 — Multimodal Collection

During a trial, the system shall collect the available modalities.

Conceptually:

Trial T001

│

┌────────────┼────────────┐

↓ ↓ ↓

Physiological Audio Vision

│ │ │

↓ ↓ ↓

Signals Speech Frames

Each modality must remain associated with the same trial identifier.

11.8 Stage 7 — Signal Quality Validation

Before model processing, the system should evaluate whether each modality contains usable information.

Examples:

Physiological

sensor connected;

sufficient signal quality;

no excessive missing data.

Audio

recording available;

sufficient speech;

acceptable noise level;

no excessive clipping.

Vision

face detected;

sufficient visibility;

acceptable image quality.

11.9 Stage 8 — Synchronization

The system shall associate corresponding portions of physiological, audio, and visual data with the same experimental trial.

The minimum conceptual relationship is:

participant_id

+

session_id

+

trial_id

This ensures that the signals being combined actually belong to the same experimental event.

11.10 Stage 9 — Preprocessing

Raw data shall undergo modality-specific preprocessing.

The product requirement is that preprocessing must:

reduce irrelevant noise;

identify invalid data;

standardize required representations;

preserve relevant signal characteristics;

document processing status.

Preprocessing must not modify the ground-truth label.

11.11 Stage 10 — Feature Extraction

The system shall transform raw signals into model-consumable representations.

For example:

PPG

↓

Heart-rate features

HRV features

Pulse features

Signal-quality features

Audio:

Speech

↓

Pause features

Pitch features

Speech-rate features

Acoustic features

Vision:

Video

↓

Blink features

Gaze features

Head-pose features

Facial movement features

11.12 Stage 11 — Individual Modality Models

Each modality should first be evaluated independently.

The system should produce:

Physiological prediction

Audio prediction

Vision prediction

This is necessary for comparison against the final fusion model.

11.13 Stage 12 — Multimodal Fusion

The individual modality information shall be combined into a multimodal representation or combined prediction.

Conceptually:

Physiological Model ──┐

│

Audio Model ──────────┼──► MOSAIC Fusion

│

Vision Model ─────────┘

↓

Final Prediction

The exact fusion technique is an implementation decision and shall be documented separately.

11.14 Stage 13 — Result Generation

The system shall generate an experimental result containing, where applicable:

modality predictions;

modality probabilities;

fusion prediction;

fusion probability;

confidence;

trial identifier;

ground-truth label;

prediction correctness.

11.15 Stage 14 — Evaluation

The system shall support aggregate evaluation across the test dataset.

Required evaluation should include:

confusion matrix;

accuracy;

precision;

recall;

F1-score;

ROC-AUC where applicable.

12. Product Architecture

12.1 Architecture Overview

MOSAIC shall follow a modular multimodal architecture.

MOSAIC PLATFORM

│

┌────────────────┼────────────────┐

│ │ │

▼ ▼ ▼

Physiological Audio Vision

Pipeline Pipeline Pipeline

│ │ │

▼ ▼ ▼

Feature Feature Feature

Extraction Extraction Extraction

│ │ │

▼ ▼ ▼

Physio Model Audio Model Vision Model

│ │ │

└────────────────┼────────────────┘

▼

Fusion Layer

│

▼

Final Classification

│

▼

Evaluation Layer

12.2 Architectural Requirements

The architecture shall be:

Modular

A modality should be replaceable without redesigning the entire product.

Extensible

Additional modalities should be possible in future versions.

Traceable

Every prediction should be traceable to:

participant;

session;

trial;

input modalities;

model version.

Fault tolerant

Failure of one optional modality should not necessarily terminate the entire experiment.

12.3 Modality Independence

Each modality shall have its own processing pipeline.

For example:

Physiology

Collection → Validation → Processing → Features → Model

Audio

Collection → Validation → Processing → Features → Model

Vision

Collection → Validation → Processing → Features → Model

This allows individual modality performance to be evaluated.

12.4 Fusion Layer

The fusion layer is the central component of MOSAIC.

It shall receive information from the available modality models and produce a unified result.

The fusion layer should account for:

modality availability;

model outputs;

probabilities/confidence;

missing modalities;

data quality.

12.5 Output Layer

The output layer shall provide:

Trial-level output

Trial ID

Physiological result

Audio result

Vision result

Fusion result

Confidence

Ground truth

Correct/incorrect

Experiment-level output

Total trials

Correct predictions

Incorrect predictions

Accuracy

Precision

Recall

F1

ROC-AUC

12.6 Architecture Extensibility

The architecture should allow future channels such as:

ECG

EEG

Text

Thermal

Additional physiological sensors

without requiring the existing three pipelines to be removed.

13. Physiological Signal Channel Requirements

13.1 Purpose

The physiological channel shall capture physiological measurements associated with participant responses during the experiment.

The initial project scope includes pulse-related measurements obtained through a pulse-oximeter/PPG sensing setup.

13.2 Primary Physiological Inputs

The system may capture:

PPG-related measurements;

heart rate;

SpO₂;

pulse amplitude;

perfusion index where available;

signal quality.

13.3 Hardware Acquisition Requirements

The hardware subsystem shall:

acquire physiological measurements;

associate measurements with a session/trial;

provide data-quality information where possible;

indicate sensor availability;

handle temporary sensor disconnection.

The exact hardware implementation shall be defined separately.

13.4 Baseline Requirements

Where the experimental protocol includes a baseline period, the system shall record baseline physiological measurements.

Baseline data may include:

baseline_heart_rate

baseline_spo2

baseline_perfusion_index

baseline_pulse_characteristics

The system should allow subsequent trial measurements to be compared against the baseline.

13.5 Heart Rate Requirements

The physiological processing layer should support:

average heart rate;

minimum heart rate;

maximum heart rate;

heart-rate variability;

change from baseline;

response-period heart rate.

13.6 SpO₂ Requirements

The system should record:

SpO₂ value;

mean SpO₂;

minimum SpO₂;

maximum SpO₂;

SpO₂ variation;

change from baseline;

signal-quality information.

SpO₂ should not be treated as an independent proof of deception.

13.7 Signal Quality

The system shall distinguish between:

Valid physiological signal

and:

Poor/invalid physiological signal

Potential quality conditions include:

sensor disconnected;

insufficient contact;

excessive noise;

missing measurements;

implausible measurements.

13.8 Physiological Feature Requirements

The feature layer should support categories such as:

Heart-rate features

mean;

minimum;

maximum;

variance;

standard deviation;

change from baseline.

HRV features

Where reliable beat-to-beat intervals are available:

RMSSD;

SDNN;

NN50;

pNN50.

Pulse features

amplitude;

interval;

pulse variability;

waveform quality.

13.9 Physiological Output

The physiological model should produce:

physiological_prediction

physiological_probability

physiological_confidence

physiological_quality

These outputs will later be passed to the fusion layer.

14. Audio Signal Channel Requirements

14.1 Purpose

The audio channel shall analyze speech and vocal characteristics associated with participant responses.

The purpose is not to determine that a particular speech characteristic inherently represents deception.

Instead, the model should learn patterns associated with the experimental labels in the dataset.

14.2 Audio Input

The system shall support recorded participant responses.

Required metadata should include:

participant;

session;

trial;

recording duration;

recording quality;

sampling information where available.

14.3 Speech Timing

The system should capture:

response latency;

speech duration;

silence duration;

pause count;

pause duration;

speech-to-silence ratio.

14.4 Speech Rate

Potential features include:

words per minute;

articulation rate;

syllable rate;

word count;

syllable count.

14.5 Hesitation

The system should support detection or measurement of:

hesitation events;

filler words;

repeated words;

incomplete words;

false starts;

self-corrections;

response delays.

14.6 Stuttering-Related Features

Because stuttering/hesitation is part of the project concept, the audio pipeline may include:

repetition count;

syllable repetition;

sound repetition;

prolongation;

blocks;

restarts;

false starts.

These features must be interpreted carefully because speech disfluency can be a normal individual characteristic and does not inherently indicate deception.

14.7 Acoustic Features

The audio pipeline should support:

Pitch

mean;

minimum;

maximum;

standard deviation;

pitch range.

Energy

RMS energy;

intensity;

energy variation.

Voice quality

Where reliable:

jitter;

shimmer;

harmonics-to-noise ratio.

Spectral

spectral centroid;

spectral bandwidth;

spectral rolloff;

zero-crossing rate.

14.8 MFCC Features

The system should support MFCC-based representations for audio modeling.

The exact number of coefficients is an implementation decision.

The dataset specification should clearly identify:

coefficient index;

aggregation method;

temporal window;

normalization method.

14.9 Audio Quality

The system shall record or derive:

signal-to-noise information;

clipping;

missing audio;

recording duration;

speech availability.

An audio model should not generate a strong prediction when the underlying recording is unusable.

14.10 Audio Model Output

The audio model should produce:

audio_prediction

audio_probability

audio_confidence

audio_quality

15. Computer Vision Channel Requirements

15.1 Purpose

The computer-vision channel shall analyze observable visual behavior during experimental responses.

The initial scope focuses on:

face;

eyes;

gaze;

blinking;

head movement;

facial movement.

15.2 Video Input

The system shall process video associated with a specific trial.

Video metadata should include:

trial identifier;

recording duration;

frame information;

video quality;

face detection status.

15.3 Face Detection

The system should determine:

whether a face is visible;

detection confidence;

face visibility;

approximate face position.

15.4 Eye and Blink Analysis

The system should support:

blink count;

blink rate;

blink duration;

eye openness;

eye-aspect measurements where applicable.

The system should preserve both:

Raw/derived measurement

and:

Quality/confidence

where appropriate.

15.5 Gaze Analysis

The system should support analysis of:

gaze direction;

gaze deviation;

gaze stability;

time looking toward camera;

time looking away.

Gaze behavior must not be interpreted independently as proof of deception.

15.6 Head Pose

The system should support:

yaw;

pitch;

roll;

head movement;

head movement frequency;

head orientation changes.

15.7 Facial Movement

The system should support measurements representing:

facial movement;

expression changes;

mouth movement;

facial landmark movement.

15.8 Facial Expression

Where supported by the selected model, the system may record expression-related probabilities.

Potential categories include:

neutral;

happy;

sad;

angry;

fear;

surprise;

disgust.

The system should retain probabilities rather than only the dominant expression wherever possible.

15.9 Vision Quality

The system should identify:

face not detected;

face partially occluded;

excessive motion blur;

insufficient lighting;

camera obstruction.

15.10 Vision Model Output

The vision model should produce:

vision_prediction

vision_probability

vision_confidence

vision_quality

16. Multimodal Data Synchronization Requirements

16.1 Purpose

Synchronization ensures that data from different modalities corresponds to the same experimental event.

Without synchronization, the fusion model could accidentally combine:

Physiology from Trial 12

+

Audio from Trial 13

+

Video from Trial 11

Such data would be invalid.

16.2 Required Identifiers

Every trial-level record should be associated with:

participant_id

session_id

trial_id

question_id

16.3 Temporal Association

Where timestamps are available, each modality should include appropriate temporal information.

Conceptually:

Trial Start

│

├── Physiological recording

│

├── Audio recording

│

└── Video recording

│

Trial End

16.4 Event Markers

The system should support important trial events such as:

baseline_start

baseline_end

question_start

question_end

answer_start

answer_end

trial_end

These events enable temporal feature extraction.

16.5 Missing Modality

A participant may have:

Physiology = available

Audio = available

Vision = unavailable

The system should record this explicitly.

It should not silently replace missing data with an arbitrary value.

16.6 Synchronization Validation

Before fusion, the system should verify:

matching participant;

matching session;

matching trial;

valid timestamps where available;

modality availability;

acceptable recording duration.

17. Dataset Requirements

17.1 Dataset Objective

The dataset is the foundation of MOSAIC.

The final curated dataset provided for the project shall contain sufficient information to support:

modality-specific analysis;

multimodal fusion;

training;

validation;

testing;

statistical analysis;

error analysis.

17.2 Participant-Level Structure

The dataset should support approximately:

300 participants

if that remains the agreed experimental target.

The final participant count may change depending on actual data collection.

17.3 Trial-Level Structure

A participant should ideally contribute multiple trials.

Conceptually:

300 participants

×

multiple questions/trials

↓

large number of experimental observations

This is preferable to having only one row per participant.

17.4 Ground Truth

Each trial should have a ground-truth label established independently of the model.

Example:

truthful

deceptive

or:

0

1

The dataset should clearly document the label encoding.

17.5 Required Dataset Metadata

The dataset should contain or be accompanied by:

data dictionary;

feature definitions;

label definitions;

participant identifiers;

trial identifiers;

modality descriptions;

missing-value policy;

preprocessing description;

collection protocol.

17.6 Core Dataset Relationship

The recommended logical relationship is:

Participant

│

└── Session

│

└── Trial

│

┌───────┼────────┐

↓ ↓ ↓

Physio Audio Vision

This relationship should be maintained regardless of whether the final data is stored in one CSV or multiple files.

17.7 Feature Categories

The curated dataset should support feature categories including:

Participant

participant ID;

demographic metadata where appropriate.

Experiment

session;

trial;

question;

condition.

Physiological

heart rate;

SpO₂;

PPG-derived features;

baseline comparisons.

Audio

timing;

speech rate;

hesitation;

stuttering-related features;

pitch;

acoustic features.

Vision

blink;

gaze;

head pose;

facial movement.

Quality

modality availability;

signal quality;

missing data.

Ground Truth

experimental label.

17.8 Dataset Quality Requirements

The dataset should be checked for:

duplicate trials;

missing participant IDs;

missing trial IDs;

inconsistent labels;

impossible values;

excessive missing values;

class imbalance;

modality mismatch.

18. Data Dictionary Requirements

18.1 Purpose

Because MOSAIC uses a large number of features, a formal data dictionary is required.

The data dictionary should define every dataset column.

18.2 Required Data Dictionary Fields

Each feature should have:

18.3 Example

18.4 Naming Convention

Column names should:

use a consistent naming style;

avoid spaces;

avoid ambiguous abbreviations;

specify units where useful;

distinguish baseline from trial measurements.

Recommended:

heart_rate_bpm

baseline_heart_rate_bpm

mean_pitch_hz

mean_pause_duration_ms

Avoid:

HR

HR2

pitch1

value

signal

19. Data Quality and Validation Requirements

19.1 Purpose

MOSAIC shall not assume that all collected data is usable.

Data validation is required before training or evaluation.

19.2 Validation Categories

Structural validation

Check:

required columns;

valid IDs;

valid data types.

Range validation

Check whether measurements fall within plausible ranges.

Temporal validation

Check:

timestamps;

durations;

ordering.

Modality validation

Check whether required modality data exists.

19.3 Missing Data

Missing data should be explicitly represented.

Possible states include:

available

missing

invalid

not_recorded

not_applicable

The system should not confuse these states.

19.4 Outlier Detection

The data-processing pipeline should identify potential outliers.

An outlier should not automatically be deleted.

It should first be investigated to determine whether it represents:

a genuine observation;

sensor error;

recording error;

preprocessing error.

19.5 Quality Score

Each modality should have a quality indicator where feasible.

For example:

physiological_quality

audio_quality

vision_quality

A trial-level overall quality indicator may also be maintained.

19.6 Quality-Control Status

Each trial may have a status such as:

valid

review_required

invalid

excluded

The reason for exclusion should be documented.

20. Experimental Design Requirements

20.1 Purpose

The experimental design defines how data is collected and how model performance is evaluated.

The design must prevent the model from obtaining misleading advantages through data leakage or uncontrolled differences between classes.

20.2 Truthful and Deceptive Conditions

Where the experimental protocol allows, participants should contribute both truthful and deceptive trials.

For example:

Participant P001

Trial 1 → Truthful

Trial 2 → Truthful

Trial 3 → Deceptive

Trial 4 → Truthful

Trial 5 → Deceptive

This is preferable to:

Participants 1–150 → Truthful

Participants 151–300 → Deceptive

because the second design can cause the model to learn participant-specific or demographic differences rather than response-related patterns.

20.3 Participant-Level Data Splitting

The train/validation/test split should be designed to prevent the same participant from appearing across training and test sets when evaluating generalization to unseen participants.

Conceptually:

Participants

│

├── Training participants

├── Validation participants

└── Test participants

rather than randomly splitting individual rows from the same participants across all three datasets.

20.4 Baseline vs Response

Where possible, each trial should contain a baseline period and response period.

Conceptually:

Baseline

↓

Question

↓

Response

↓

Recovery

This enables the system to evaluate changes relative to the participant's own baseline.

20.5 Experimental Comparisons

The evaluation should compare:

Experiment A

Physiological only.

Experiment B

Audio only.

Experiment C

Vision only.

Experiment D

Physiological + Audio.

Experiment E

Physiological + Vision.

Experiment F

Audio + Vision.

Experiment G

All three modalities.

This comparison directly tests the central MOSAIC hypothesis.

20.6 Success Criterion

The project should not define success solely as:

"MOSAIC achieved X% accuracy."

Instead, success should include demonstrating:

reliable multimodal data integration;

valid experimental methodology;

meaningful modality-level models;

measurable fusion performance;

comparison against individual modalities;

transparent limitations;

reproducible evaluation.

The final performance values should be reported honestly from the curated dataset rather than predetermined.

21. Functional Requirements

21.1 Overview

MOSAIC shall provide a complete workflow for conducting, recording, analyzing, and evaluating multimodal experimental sessions.

The functional requirements are divided into:

Experiment Management

Participant Management

Session Management

Trial Management

Data Acquisition

Data Validation

Analysis

Fusion

Results

Reporting

21.2 Experiment Management

The system shall allow an authorized operator to create an experiment.

An experiment should contain:

experiment ID;

experiment name;

description;

experiment version;

question set;

target modalities;

experiment status;

creation date;

modification date.

Possible experiment states:

Draft

Ready

Running

Completed

Archived

21.3 Experiment Configuration

The operator shall be able to configure:

number of questions;

question categories;

trial duration;

baseline duration;

recovery period;

enabled modalities;

recording requirements;

experimental conditions.

The system shall validate the configuration before the experiment begins.

21.4 Participant Management

The system shall allow the operator to:

create a participant record;

assign a unique participant ID;

associate the participant with an experiment;

create sessions;

view previous sessions;

review participant-level results.

The system should minimize unnecessary personally identifiable information.

21.5 Participant Status

The participant may have a session status such as:

Registered

Ready

In Session

Paused

Completed

Cancelled

21.6 Session Management

The system shall create a session for every experiment participation event.

Each session should contain:

session_id

participant_id

experiment_id

start_time

end_time

status

trial_count

quality_status

21.7 Session Resume

Where technically and experimentally appropriate, the system may allow a paused session to resume.

The system shall preserve:

completed trials;

collected data;

session metadata;

trial states.

21.8 Trial Management

Each question-response interaction shall be represented as a trial.

A trial should have:

trial_id

question_id

participant_id

session_id

start_time

end_time

ground_truth

status

21.9 Trial States

A trial may transition through:

Not Started

↓

Preparing

↓

Baseline

↓

Question Presented

↓

Response Recording

↓

Processing

↓

Completed

A trial may also enter:

Failed

Cancelled

Requires Review

22. User Interface Requirements

22.1 UI Objective

The MOSAIC interface shall allow an operator to conduct an experiment without needing to understand the internal machine-learning pipeline.

The interface should prioritize:

simplicity;

visibility;

clear status;

data quality;

experimental safety;

traceability.

22.2 Main Dashboard

The dashboard should provide an overview of:

active experiment;

participant;

current session;

current trial;

modality status;

recording status;

data quality;

system status.

Example conceptual layout:

┌─────────────────────────────────────────────┐

│ MOSAIC │

├─────────────────────────────────────────────┤

│ Experiment: EXP-001 │

│ Participant: P023 │

│ Session: S023-01 │

│ │

│ Physiological ● Connected │

│ Audio ● Recording │

│ Vision ● Face Detected │

│ │

│ Current Trial: 05 │

│ Status: Recording Response │

└─────────────────────────────────────────────┘

22.3 Participant Screen

The participant screen should show only information necessary for completing the experiment.

It may display:

question;

instructions;

countdown;

recording status;

trial progress.

The participant should not necessarily see model predictions during the experiment.

22.4 Operator Screen

The operator should be able to see:

participant ID;

current question;

sensor status;

audio status;

camera status;

trial status;

quality indicators.

22.5 Recording Status

Each modality shall have an easily understandable state.

Example:

Physiology ● Ready

Audio ● Ready

Vision ● Ready

During recording:

Physiology ● Recording

Audio ● Recording

Vision ● Recording

22.6 Quality Indicators

The UI should communicate quality without overwhelming the operator.

For example:

Physiology Good

Audio Good

Vision Attention

If a modality becomes unusable, the operator should receive a clear explanation.

Example:

Face not detected. Please ensure the participant is visible to the camera.

22.7 Trial Progress

The interface should display progress such as:

Question 5 of 10

or:

Trial 5 / 10

22.8 Error Messages

Errors should be understandable to non-technical users.

Avoid:

ERR_PPGR_1042

Prefer:

Physiological sensor signal is unavailable. Check sensor contact and try again.

23. Real-Time Monitoring Requirements

23.1 Purpose

During data collection, MOSAIC should provide real-time visibility into whether the required signals are being captured successfully.

23.2 Physiological Monitoring

Where hardware supports real-time values, the interface may display:

current heart rate;

SpO₂;

signal quality;

sensor connection.

The display should primarily be used for monitoring signal acquisition rather than presenting an immediate deception judgment.

23.3 Audio Monitoring

The system should indicate:

microphone connected;

recording active;

speech detected;

excessive noise;

clipping;

recording quality.

23.4 Vision Monitoring

The system should indicate:

camera connected;

face detected;

face visibility;

lighting quality;

excessive movement;

camera obstruction.

23.5 Unified System Status

The system should provide an overall readiness state.

Example:

SYSTEM READY

✓ Physiological

✓ Audio

✓ Vision

or:

SYSTEM NOT READY

✓ Physiological

⚠ Audio — microphone unavailable

✓ Vision

23.6 Recording Indicator

The system should clearly indicate when recording is active.

This is particularly important for transparency and participant awareness.

24. Experiment Execution Requirements

24.1 Pre-Session Checklist

Before starting a session, the system should verify:

participant registered;

experiment selected;

required sensors available;

camera available;

microphone available;

sufficient storage;

required configuration loaded.

24.2 Session Start

When the operator starts the session, MOSAIC shall:

create the session;

initialize enabled modalities;

validate readiness;

begin the configured workflow.

24.3 Baseline Stage

If baseline collection is configured, the system shall:

notify the participant;

start baseline collection;

maintain the configured baseline duration;

validate signal quality;

store baseline measurements.

24.4 Question Presentation

The system shall present the configured question.

The question should have:

question ID;

text;

category;

expected response format where applicable.

24.5 Response Recording

When the participant responds, MOSAIC shall associate:

audio;

video;

physiological measurements;

with the current trial.

24.6 Trial Completion

After the response period ends, the system shall:

stop trial recording;

finalize trial metadata;

validate collected data;

mark trial status;

begin processing where applicable.

24.7 Recovery Period

Where included in the protocol, the system should provide a recovery period between trials.

This can help distinguish:

Previous trial response

from:

Next trial baseline

25. Model Management Requirements

25.1 Purpose

MOSAIC shall treat models as versioned components rather than permanent black boxes.

Every prediction should be associated with a model version.

25.2 Modality Models

The platform shall support independent models for:

physiological signals;

audio;

computer vision.

25.3 Model Metadata

Each registered model should have:

model ID;

model version;

modality;

training dataset version;

training date;

evaluation metrics;

model status.

25.4 Model Lifecycle

A model may have states:

Development

Validation

Approved

Active

Deprecated

Archived

25.5 Model Selection

The system shall know which model version is active for a given experiment.

For example:

Physiology → Model v1.2

Audio → Model v2.0

Vision → Model v1.4

Fusion → Model v1.1

25.6 Model Reproducibility

The system should preserve enough metadata to reproduce an experiment's prediction results.

This includes:

model versions;

dataset version;

feature version;

experiment version.

26. Modality-Level Prediction Requirements

26.1 Purpose

Before combining modalities, each modality shall be capable of producing an independent result.

This enables proper comparison.

26.2 Physiological Prediction

The physiological model should generate:

prediction

probability

confidence

quality

26.3 Audio Prediction

The audio model should generate:

prediction

probability

confidence

quality

26.4 Vision Prediction

The vision model should generate:

prediction

probability

confidence

quality

26.5 Prediction Availability

If a modality fails, the system should identify the modality as unavailable rather than silently generating a prediction from invalid data.

Example:

Physiology → Available

Audio → Available

Vision → Unavailable

26.6 Independent Evaluation

The system shall support evaluation of each modality independently.

This allows the project to answer:

How much does each modality contribute?

rather than only:

How accurate is the final system?

27. Multimodal Fusion Requirements

27.1 Purpose

Fusion is the core MOSAIC capability.

The fusion component shall combine information from multiple modalities to produce a unified experimental prediction.

27.2 Fusion Inputs

The fusion layer may receive:

Physiological features

Audio features

Vision features

or outputs from modality-specific models, depending on the selected architecture.

The precise architecture belongs in the implementation document.

27.3 Modality Availability

Fusion shall account for unavailable modalities.

Example:

Physiology ✓

Audio ✓

Vision ✗

The system should not treat missing vision as equivalent to a meaningful numerical measurement.

27.4 Fusion Output

The fusion layer shall produce:

fusion_prediction

fusion_probability

fusion_confidence

27.5 Fusion Traceability

A final result should identify which modalities contributed to it.

Example:

Trial T001

Physiology: Available

Audio: Available

Vision: Available

Fusion: Generated

27.6 Modality Contribution

Where supported, the product should provide an interpretable representation of modality contribution.

For example:

Physiology contribution: 0.31

Audio contribution: 0.42

Vision contribution: 0.27

These values must only be displayed if they genuinely represent the selected model's contribution methodology.

28. Confidence and Uncertainty Requirements

28.1 Purpose

MOSAIC shall distinguish between a prediction and certainty about that prediction.

A model should not present every output as equally reliable.

28.2 Confidence

Each prediction should have a confidence representation where supported.

Example:

Prediction: Class A

Confidence: 0.82

28.3 Low Confidence

The system should identify low-confidence predictions.

Example:

Prediction confidence: Low

The exact threshold should be configurable or documented by the model evaluation process.

28.4 Insufficient Data

The system should be able to return:

Insufficient Data

when the available signals do not meet minimum quality requirements.

This is preferable to forcing a prediction from poor-quality data.

28.5 Confidence Interpretation

The UI and reports should make clear that:

Model confidence is not equivalent to certainty that a participant is truthful or deceptive.

29. Explainability Requirements

29.1 Purpose

Because MOSAIC deals with a sensitive classification task, the system should provide information explaining what types of signals influenced a result.

29.2 Modality-Level Explanation

The result should identify available modalities.

Example:

Physiological: High contribution

Audio: Moderate contribution

Vision: Low contribution

Only if supported by a valid explanation method.

29.3 Feature-Level Explanation

Where technically appropriate, the system may display influential feature categories such as:

Speech hesitation

Heart-rate variation

Gaze behavior

The system must avoid presenting these as deterministic indicators of deception.

29.4 Explanation Language

The UI should use experimental language.

Prefer:

The model identified patterns in the recorded signals that were associated with the experimental class.

Avoid:

The participant lied because their heart rate increased.

29.5 Explanation Limitations

The system should communicate that:

physiological changes have multiple causes;

speech hesitation is not unique to deception;

gaze behavior is not definitive;

facial expressions are not definitive;

model predictions depend on training data.

30. Results, Evaluation and Reporting Requirements

30.1 Trial-Level Results

For every completed trial, the system should be capable of storing:

participant_id

session_id

trial_id

physiological_prediction

physiological_probability

audio_prediction

audio_probability

vision_prediction

vision_probability

fusion_prediction

fusion_probability

ground_truth

prediction_correct

30.2 Participant-Level Results

The system should aggregate results for a participant.

Potential metrics include:

number of trials;

correct predictions;

incorrect predictions;

modality-level performance;

fusion performance.

The system should avoid reducing a participant to a simplistic permanent "liar" or "truthful" identity.

30.3 Experiment-Level Metrics

The reporting system shall support:

Accuracy

Correct predictions / Total predictions

Precision

Measurement of the proportion of predicted positive cases that were actually positive.

Recall

Measurement of the proportion of actual positive cases correctly detected.

F1-score

Harmonic mean of precision and recall.

Confusion Matrix

The system should show:

Actual

Class 0 Class 1

Predicted 0 TN FN

Predicted 1 FP TP

30.4 Modality Comparison

The report should compare:

The values shall be generated from actual evaluation results.

30.5 Fusion Improvement

The project should specifically evaluate whether multimodal fusion improves performance over individual modalities.

Example:

Physiology → 72%

Audio → 76%

Vision → 69%

MOSAIC Fusion → 81%

These numbers are illustrative only, not project targets.

30.6 Error Analysis

The reporting layer should support analysis of incorrect predictions.

Potential categories:

poor physiological signal;

noisy audio;

missing speech;

face not detected;

lighting issue;

participant variability;

ambiguous question;

incorrect ground-truth annotation;

model error.

30.7 Report Contents

A complete experiment report should include:

Experiment information

Dataset information

Participant count

Trial count

Modality availability

Data-quality summary

Individual model performance

Fusion performance

Confusion matrices

Performance metrics

Error analysis

Limitations

Model/version information

Dataset version

Experiment configuration

30.8 Export Requirements

The system should support exporting results for academic analysis.

Potential formats:

CSV;

JSON;

PDF report.

The exported report should preserve experiment identifiers and model versions so that results remain traceable.

Sections completed so far

01 — Product Overview

02 — Problem Statement

03 — Product Vision

04 — Objectives

05 — Scope

06 — Users & Stakeholders

07 — Use Cases

08 — Assumptions

09 — Constraints

10 — End-to-End Product Workflow

11 — End-to-End Product Workflow

12 — Product Architecture

13 — Physiological Channel

14 — Audio Channel

15 — Computer Vision Channel

16 — Data Synchronization

17 — Dataset Requirements

18 — Data Dictionary

19 — Data Quality

20 — Experimental Design

21 — Functional Requirements

22 — User Interface

23 — Real-Time Monitoring

24 — Experiment Execution

25 — Model Management

26 — Modality Predictions

27 — Multimodal Fusion

28 — Confidence & Uncertainty

29 — Explainability

30 — Results & Reporting

31. Data Storage and Data Lifecycle Requirements

31.1 Purpose

MOSAIC will generate multiple types of data during an experiment:

participant metadata;

experiment metadata;

session metadata;

trial metadata;

physiological measurements;

audio recordings/features;

video recordings/features;

model outputs;

quality metrics;

ground-truth annotations;

evaluation results.

The product must maintain a clear relationship between all of these data types.

31.2 Data Hierarchy

The logical data hierarchy shall be:

Experiment

│

├── Participants

│ │

│ └── Sessions

│ │

│ └── Trials

│ │

│ ┌──────────┼──────────┐

│ ↓ ↓ ↓

│ Physiology Audio Vision

│ │ │ │

│ └──────────┼──────────┘

│ ↓

│ Features

│ ↓

│ Models

│ ↓

│ Results

Every child record must remain traceable to its parent.

31.3 Raw Data

Where permitted by the experiment and storage constraints, MOSAIC should preserve raw recordings.

Examples include:

raw physiological measurements;

raw audio;

raw video;

timestamps;

sensor metadata.

Raw data should be considered the source data from which derived features are generated.

31.4 Processed Data

Processed data may include:

cleaned signals;

normalized signals;

extracted speech segments;

detected facial landmarks;

derived physiological measurements;

extracted audio features;

extracted vision features.

Processed data must retain a relationship with its source data.

31.5 Feature Data

The feature layer shall contain the measurements provided to the models.

Examples:

heart_rate_bpm

rmssd_ms

spo2_percent

mean_pitch_hz

pause_count

jitter_percent

blink_rate

gaze_deviation

head_yaw_degrees

Each feature should have a documented definition.

31.6 Prediction Data

Prediction records shall contain:

model identifier;

model version;

prediction;

probability/confidence where applicable;

timestamp;

trial identifier.

31.7 Ground-Truth Data

Ground-truth information shall be stored separately from model predictions conceptually, even if represented in the same final dataset.

This prevents accidental replacement of experimental labels with model outputs.

31.8 Data Lifecycle

MOSAIC should support the following lifecycle:

Collected

↓

Validated

↓

Processed

↓

Feature Extracted

↓

Analyzed

↓

Evaluated

↓

Archived

Invalid or incomplete records should be clearly marked rather than silently deleted.

31.9 Dataset Versioning

Every curated dataset should have a version.

Example:

MOSAIC-DATA-v1.0

MOSAIC-DATA-v1.1

MOSAIC-DATA-v2.0

Changes to:

participant records;

labels;

feature definitions;

preprocessing;

exclusions;

should result in an updated dataset version where appropriate.

32. User Roles and Access Control

32.1 Purpose

MOSAIC should distinguish between people who operate experiments, analyze results, and administer the platform.

32.2 Primary Roles

The initial system may support:

Administrator

Responsible for:

system configuration;

user management;

model management;

experiment management;

access control.

Researcher / Project Lead

Responsible for:

creating experiments;

configuring questions;

reviewing data;

analyzing results;

generating reports.

Operator

Responsible for:

registering participants;

conducting sessions;

monitoring sensors;

completing trials.

Viewer

Responsible for:

viewing approved results;

viewing reports.

32.3 Permission Principle

Users should only have access to functionality necessary for their role.

For example:

Operator

✓ Run experiment

✓ Monitor session

✓ View session status

✗ Change active ML model

✗ Delete dataset

32.4 Administrator Permissions

Administrators may manage:

users;

roles;

experiments;

datasets;

models;

system configuration.

Sensitive operations should require appropriate authorization.

32.5 Researcher Permissions

Researchers should be able to:

create experiments;

review datasets;

review model performance;

compare modalities;

generate reports.

32.6 Viewer Permissions

Viewers should have read-only access to permitted results.

They should not be able to:

modify experimental data;

alter labels;

change models;

delete sessions.

33. Participant Consent and Privacy Requirements

33.1 Purpose

MOSAIC collects potentially sensitive experimental information, including physiological, audio, and visual data.

The system must therefore support an explicit consent process appropriate to the research setting.

33.2 Consent Requirement

Before collecting participant data, the system should verify that the required consent process has been completed according to the project's approved protocol.

33.3 Consent Record

The system should be capable of recording:

consent_status

consent_timestamp

consent_version

experiment_id

participant_id

The exact legal wording should come from the project's institution/ethics process rather than being invented by the software.

33.4 Participant Information

Participants should be informed, as appropriate, about:

what information is being collected;

why it is being collected;

how it will be used;

how long it may be retained;

who may access it;

whether recordings are retained;

their ability to withdraw where applicable.

33.5 Pseudonymous Identification

The system should use a participant ID rather than exposing participant names throughout the ML pipeline.

Example:

P001

P002

P003

The analytical dataset should avoid unnecessary personally identifying information.

33.6 Audio and Video Privacy

Audio and video recordings should be treated as sensitive research data.

Access should be restricted according to project requirements.

33.7 Data Deletion / Withdrawal

Where the approved research protocol permits participant withdrawal, MOSAIC should support identification of the participant's associated records so that the appropriate data-management process can be followed.

33.8 Privacy in Reports

Reports should avoid unnecessary personally identifying information.

For example:

Participant: P017

is preferable to displaying a participant's full name unless there is a legitimate reason to do so.

34. Security Requirements

34.1 Purpose

MOSAIC must protect:

participant data;

experimental recordings;

datasets;

model files;

prediction results;

user accounts.

34.2 Authentication

Users with access to protected functionality shall authenticate before accessing the system.

34.3 Authorization

Authentication alone shall not grant unrestricted access.

The system shall enforce role-based permissions.

34.4 Data Protection

Sensitive data should be protected during:

storage;

transfer;

export;

backup.

The implementation document will define the specific security mechanisms.

34.5 Session Security

User sessions should:

expire according to configured security requirements;

prevent unauthorized reuse;

support secure logout.

34.6 File Access

Raw audio/video recordings should not be publicly accessible by default.

Access should be controlled through authorized application workflows.

34.7 Model Security

Model files should be protected from unauthorized modification.

A changed model can produce different experimental results, so model integrity is important.

34.8 Dataset Integrity

The system should detect or document changes to curated datasets.

A dataset used for published evaluation should remain reproducible.

34.9 Secure Export

Exports should be generated only by authorized users.

The system should identify:

who generated the export;

when it was generated;

which experiment/dataset version it represents.

35. Hardware and Device Management Requirements

35.1 Purpose

MOSAIC depends on multiple acquisition devices.

The initial experimental setup may include:

Pulse-Oximeter / PPG

+

Microphone

+

Camera

+

Processing Device

35.2 Device Registration

The system should maintain information about connected devices where feasible.

Example:

Device ID

Device Type

Device Status

Device Version

Connection Status

35.3 Device Status

Devices should expose a logical status such as:

Disconnected

Connected

Initializing

Ready

Recording

Error

35.4 Physiological Sensor

The system shall determine whether the physiological sensor is available before beginning a trial when it is configured as mandatory.

35.5 Microphone

The system shall verify:

microphone availability;

recording access;

usable audio signal.

35.6 Camera

The system shall verify:

camera availability;

camera access;

usable video;

face visibility where required.

35.7 Device Failure

If a device becomes unavailable during a trial, the system should:

detect the failure;

record the failure;

notify the operator;

preserve data collected before failure;

mark the affected modality appropriately.

35.8 Device Compatibility

The product should define a supported-device list for the project.

The PRD should not lock the project to a single hardware model unless the hardware has already been finalized.

This is especially important because the team's final hardware decision is still pending.

36. Sensor Calibration and Readiness Requirements

36.1 Purpose

Reliable measurements require the acquisition system to be in an appropriate state before recording begins.

36.2 Pre-Session Readiness

Before starting data collection, the system should verify:

sensor connected;

sensor producing data;

camera available;

microphone available;

required permissions available.

36.3 Physiological Sensor Readiness

The system should check whether the sensor appears to be receiving a stable signal.

The operator should receive an understandable status.

Example:

Physiological Sensor

Status: Waiting for stable signal

36.4 Camera Readiness

The system should check:

camera availability;

participant visibility;

acceptable framing;

sufficient lighting where possible.

36.5 Microphone Readiness

The system should verify:

microphone availability;

recording capability;

signal presence;

excessive noise where detectable.

36.6 Calibration State

If a device requires calibration according to its specification, MOSAIC should provide an appropriate calibration/readiness workflow.

The exact calibration procedure belongs to the selected hardware and therefore will be defined in the implementation/hardware document.

36.7 Readiness Gate

The system should prevent an experiment from starting when a mandatory modality has failed its readiness check.

Optional modalities may be handled according to the experiment configuration.

37. Offline and Connectivity Requirements

37.1 Purpose

A research experiment should not lose an entire session simply because network connectivity is temporarily unavailable.

37.2 Local Acquisition

Where the architecture permits, acquisition should be capable of continuing temporarily during network interruptions.

37.3 Offline State

The UI should clearly communicate:

Online

or:

Offline — Data stored locally

37.4 Data Synchronization

When connectivity returns, pending data should be synchronized according to the system's data-management policy.

37.5 Duplicate Prevention

Synchronization must avoid creating duplicate:

sessions;

trials;

recordings;

predictions.

Unique identifiers should be used to distinguish records.

37.6 Interrupted Upload

If a recording or dataset upload is interrupted, the system should indicate its status.

Example:

Upload:

75% complete

or:

Upload interrupted — retry required

37.7 Offline Experiment Integrity

The system should preserve the relationship between:

Participant

→ Session

→ Trial

→ Modalities

even when synchronization occurs later.

38. Notifications and Alerts

38.1 Purpose

Notifications should help operators respond to problems during experiments.

38.2 Alert Categories

Alerts may include:

Device alert

Microphone disconnected.

Signal alert

Physiological signal quality is low.

Vision alert

Face is not detected.

Storage alert

Available storage is low.

Session alert

Trial recording has stopped unexpectedly.

38.3 Severity Levels

Alerts should have severity levels such as:

Information

Warning

Critical

38.4 Warning

Warnings indicate something that may affect data quality.

Example:

Camera framing is changing.

The experiment may continue depending on the protocol.

38.5 Critical Alert

A critical alert indicates that continuing may produce invalid experimental data.

Example:

Required physiological sensor unavailable.

The system should recommend an appropriate action.

38.6 Alert History

Important alerts should be associated with the relevant:

session;

trial;

device;

timestamp.

This supports later error analysis.

39. Audit Logging and Traceability

39.1 Purpose

MOSAIC should maintain an audit trail of important system actions.

This is particularly important for an academic/research project where results need to be reproducible.

39.2 Events to Log

The system should record important events such as:

experiment created;

experiment modified;

participant registered;

session started;

session ended;

trial started;

trial completed;

recording started;

recording stopped;

sensor disconnected;

dataset imported;

dataset version changed;

model activated;

report generated.

39.3 Audit Record

An audit record should conceptually contain:

event_id

event_type

timestamp

user_id

experiment_id

session_id

trial_id

description

Not every field will apply to every event.

39.4 Model Auditability

Every prediction should be traceable to the model version used.

Example:

Trial T034

↓

Physiology Model v1.2

Audio Model v1.4

Vision Model v1.1

Fusion Model v1.0

39.5 Dataset Auditability

The system should identify which dataset version was used to train/evaluate a model.

Example:

Model: Fusion-v1.0

Dataset: MOSAIC-DATA-v1.2

39.6 Result Reproducibility

A completed experiment report should preserve sufficient metadata to determine:

which data was used;

which model was used;

which experiment configuration was used;

which feature version was used.

40. Accessibility, Usability and Human-Factor Requirements

40.1 Purpose

MOSAIC will be operated during live experiments, so the interface must be understandable and usable under time pressure.

40.2 Simplicity

The primary workflow should avoid unnecessary complexity.

An operator should be able to understand:

What experiment am I running?

Who is participating?

Which trial am I on?

Are the sensors working?

Is the recording valid?

What should I do next?

40.3 Visual Clarity

Important statuses should be visually distinguishable.

Examples:

✓ Ready

⚠ Attention

✕ Error

● Recording

The final UI should not rely exclusively on color to communicate state.

40.4 Readability

Text should be:

sufficiently large;

clearly structured;

easy to scan;

consistent throughout the application.

40.5 Error Recovery

Whenever possible, errors should provide an action.

Instead of:

Recording failed.

Prefer:

Audio recording failed. Check microphone access and retry the trial.

40.6 Confirmation for Destructive Actions

Actions such as:

deleting data;

deleting a session;

removing a dataset;

changing experimental labels;

should require confirmation and appropriate authorization.

40.7 Operator Workflow Efficiency

The operator should not need to repeatedly navigate through unrelated screens between trials.

The desired workflow should be approximately:

Start Session

↓

Baseline

↓

Question

↓

Record

↓

Validate

↓

Next Question

40.8 Participant Experience

The participant-facing interface should minimize distractions.

It should clearly communicate:

when to prepare;

when to answer;

when recording is happening;

when the trial is complete.

40.9 No Misleading Feedback

During an active experiment, the participant should not be shown potentially biasing predictions such as:

"You are probably lying."

The system should separate experimental measurement from participant feedback.

40.10 Accessibility Considerations

Where applicable, the interface should consider:

keyboard navigation;

readable typography;

sufficient contrast;

clear error messages;

non-color status indicators;

understandable language.

40.11 Usability Testing

Before final deployment, the team should conduct usability testing covering at least:

experiment setup;

participant registration;

sensor setup;

session start;

trial execution;

error recovery;

result review.

40.12 Usability Success Criteria

An operator should be able to complete a standard experiment without requiring technical knowledge of:

machine learning;

signal processing;

computer vision;

feature extraction;

multimodal fusion.

The complexity should remain behind the product interface.

41. Performance Requirements

41.1 Purpose

MOSAIC must provide sufficiently responsive behavior during live experimental sessions without interrupting data collection.

Performance requirements apply to:

user interface;

sensor acquisition;

audio recording;

video recording;

synchronization;

feature extraction;

model inference;

result generation.

41.2 Application Responsiveness

Normal user interactions should respond without noticeable delay.

Examples include:

opening a participant;

starting a session;

moving to the next question;

viewing sensor status;

navigating between results.

41.3 Recording Performance

During active recording, the system should maintain continuous acquisition for all enabled modalities.

The system should minimize:

dropped samples;

dropped video frames;

audio gaps;

timestamp inconsistencies;

unexpected recording termination.

41.4 Synchronization Performance

Measurements from different modalities must remain temporally associated with the correct trial.

The system should preserve timestamps sufficiently accurately for the selected experimental protocol.

41.5 Inference Performance

Model inference should be sufficiently fast for the intended workflow.

The system should distinguish between:

Real-time inference

and:

Post-session analysis

The final implementation may support one or both.

41.6 Large Dataset Processing

The system should be capable of processing the curated dataset supplied for the project without requiring manual processing of every row.

41.7 Performance Monitoring

The system should be able to identify processing bottlenecks such as:

excessive inference time;

slow feature extraction;

insufficient memory;

storage limitations;

device communication delays.

42. Reliability and Availability Requirements

42.1 Purpose

A failed sensor or software component should not unnecessarily invalidate an entire experimental session.

42.2 Session Reliability

Once a session begins, MOSAIC should preserve collected data even if a later component fails.

For example:

Trial 1 → Complete

Trial 2 → Complete

Trial 3 → Audio failure

Trial 4 → Complete

Trial 3 should not cause the previously completed trials to disappear.

42.3 Fault Isolation

A failure in one modality should be isolated where possible.

Example:

Physiology → Working

Audio → Failed

Vision → Working

The system should not automatically treat all three modalities as failed.

42.4 Recovery

The system should provide recovery mechanisms for:

sensor disconnection;

camera failure;

microphone failure;

temporary connectivity loss;

application interruption;

incomplete uploads.

42.5 Crash Recovery

If the application unexpectedly closes during an experiment, the system should preserve recoverable session information where technically possible.

42.6 Data Integrity

The system must avoid silently corrupting collected data.

Incomplete records should be explicitly marked.

42.7 Availability

For the academic prototype, the system should prioritize reliable operation during scheduled experimental sessions rather than requiring continuous 24/7 production availability.

43. Testing and Quality Assurance Requirements

43.1 Purpose

MOSAIC must be tested at multiple levels before being used to collect final experimental data.

43.2 Functional Testing

Testing should verify:

participant registration;

experiment creation;

question management;

session creation;

trial execution;

recording;

data storage;

result generation;

report generation.

43.3 Hardware Testing

Each acquisition component should be tested independently.

Physiological channel

Verify:

connection;

signal acquisition;

sensor stability;

expected measurement range;

disconnection handling.

Audio channel

Verify:

microphone connection;

recording;

speech detection;

noise handling;

recording failure.

Vision channel

Verify:

camera access;

face detection;

lighting conditions;

face movement;

camera disconnection.

43.4 Integration Testing

The complete acquisition workflow should be tested:

Question

↓

Physiology

+

Audio

+

Vision

↓

Timestamp Association

↓

Feature Extraction

↓

Model Processing

↓

Fusion

↓

Result

43.5 Data Validation Testing

The system should verify that:

required columns exist;

values have valid types;

timestamps are valid;

participant IDs are consistent;

trial IDs are unique;

labels are valid;

missing values are appropriately handled.

43.6 Model Testing

Models should be evaluated independently before being integrated into the fusion pipeline.

43.7 UI Testing

The application should be tested for:

navigation;

responsive layout;

error states;

loading states;

empty states;

device states;

result visualization.

43.8 Regression Testing

Changes to one modality should not unintentionally break another modality.

For example:

Updating audio processing should not cause physiological data synchronization to fail.

44. Model Evaluation Requirements

44.1 Purpose

The project must evaluate whether MOSAIC actually provides meaningful experimental performance.

Accuracy alone shall not be considered sufficient.

44.2 Required Metrics

Where applicable, evaluation should include:

accuracy;

precision;

recall;

F1-score;

specificity;

sensitivity;

confusion matrix.

44.3 Class Balance

The evaluation must consider class imbalance.

For example, if the dataset contains significantly more truthful than deceptive trials, accuracy alone may provide a misleading impression.

44.4 Train/Test Separation

The evaluation process must prevent test data from influencing model training.

44.5 Participant-Level Separation

Because multiple trials may belong to the same participant, the project should avoid situations where recordings from the same participant appear in both training and test sets in a way that causes data leakage.

The exact split strategy will be defined in the implementation/research methodology document.

44.6 Baseline Comparison

MOSAIC should compare:

Physiological-only

Audio-only

Vision-only

Multimodal Fusion

This will demonstrate whether combining modalities provides measurable improvement.

44.7 Statistical Reporting

Where appropriate, the project should report:

sample size;

number of trials;

number of participants;

class distribution;

confidence intervals or other uncertainty measures.

44.8 No Artificial Performance

The project must not artificially generate or manipulate test results to improve reported performance.

Synthetic data may be used for software testing, but final model evaluation should clearly distinguish synthetic data from experimentally collected data.

45. Data Leakage and Experimental Validity Requirements

45.1 Purpose

A major risk in multimodal ML systems is obtaining artificially high performance because information from the test set, participant, or future time period leaks into training.

MOSAIC shall explicitly address this.

45.2 Feature Leakage

Features that directly or indirectly reveal the ground-truth label must not be used unless intentionally part of the experimental design.

45.3 Participant Leakage

The same participant should not unintentionally appear in both training and testing in a manner that allows the model to memorize participant-specific patterns.

45.4 Temporal Leakage

Future information must not be used to generate features that would supposedly be available at prediction time.

45.5 Label Integrity

Ground-truth labels must originate from the defined experimental protocol.

They must not be generated from:

model prediction

model confidence

heart rate threshold

audio threshold

facial behavior threshold

unless the research design explicitly defines such a rule.

45.6 Data Pipeline Reproducibility

The same dataset and processing configuration should produce consistent results under the same conditions.

46. Ethical and Safety Requirements

46.1 Purpose

MOSAIC is an experimental multimodal classification system.

It must not be represented as a scientifically infallible device capable of determining whether a person is lying.

46.2 Experimental Classification

The system's labels should be described as experimental classifications based on the project's defined dataset and protocol.

46.3 No Deterministic Claims

The interface and reports should avoid statements such as:

"The participant is definitely lying."

Instead:

"The model classified this trial as deceptive with a confidence of X under the experimental protocol."

46.4 Physiological Limitations

Changes in physiological measurements may result from:

anxiety;

stress;

exercise;

fatigue;

environmental conditions;

sensor movement;

individual differences.

Therefore, physiological changes must not automatically be interpreted as deception.

46.5 Audio Limitations

Speech behavior can be influenced by:

nervousness;

language proficiency;

accent;

speech disorders;

fatigue;

microphone quality;

environmental noise.

The system should therefore avoid interpreting a stutter or hesitation as definitive evidence of deception.

46.6 Computer Vision Limitations

Facial behavior can vary because of:

lighting;

camera angle;

facial characteristics;

cultural differences;

individual expression patterns;

fatigue;

emotional state.

46.7 Bias Evaluation

The project should evaluate whether model performance changes significantly across relevant participant groups where sufficient data exists.

46.8 Human Oversight

MOSAIC should be positioned as a research/decision-support system rather than an autonomous authority.

Human researchers should remain responsible for interpreting experimental results.

47. Risk Management Requirements

47.1 Purpose

The project shall identify risks before final deployment.

47.2 Hardware Risks

Potential risks:

sensor failure;

loose sensor connection;

battery failure;

camera failure;

microphone failure;

damaged cables;

insufficient power.

Mitigation:

readiness checks;

device status monitoring;

spare components where feasible;

recording validation.

47.3 Data Risks

Potential risks:

missing data;

corrupted recordings;

duplicate records;

incorrect labels;

synchronization errors.

Mitigation:

validation;

unique identifiers;

quality checks;

audit logs;

dataset versioning.

47.4 ML Risks

Potential risks:

overfitting;

data leakage;

class imbalance;

poor generalization;

biased predictions;

synthetic-data dependence.

Mitigation:

participant-level evaluation;

proper dataset separation;

cross-validation where appropriate;

modality comparison;

transparent reporting.

47.5 Operational Risks

Potential risks:

operator error;

incorrect participant setup;

incorrect question selection;

accidental session termination.

Mitigation:

guided workflow;

pre-session checklist;

confirmation dialogs;

clear status indicators.

47.6 Project Risks

Potential project risks include:

hardware architecture not finalized;

insufficient participant data;

unreliable sensors;

limited computational resources;

incomplete datasets;

integration complexity.

The product design should therefore remain modular enough to accommodate hardware or model changes.

48. Assumptions and Dependencies

48.1 Assumptions

The PRD assumes:

A curated dataset will be supplied for model development/testing.

The dataset will contain multimodal information or sufficient features for the selected modalities.

Ground-truth labels will be defined through an experimental protocol.

Hardware requirements may change before implementation.

The project will initially operate as an academic/research prototype.

The three primary modalities are:

physiological;

audio;

computer vision.

Multimodal fusion will be evaluated against individual modalities.

48.2 Hardware Dependency

The final hardware design is not considered completely frozen at the PRD stage.

The current proposed architecture may include:

LiPo Battery

↓

Charging / Power Management

↓

Microcontroller

↓

Physiological Sensor

along with:

Microphone

Camera

The exact power architecture, sensor selection, voltage requirements, and wiring shall be finalized separately.

This is important because the current hardware discussion around the TP4056, LiPo, ESP32-C3 and boost converter should not unnecessarily constrain the software PRD before the teammates finalize the hardware.

48.3 Dataset Dependency

The final feature schema must be aligned with the curated dataset.

The large CSV structure previously discussed should therefore be treated as the target data model, not as permission to invent measurements that the actual hardware/dataset cannot produce.

48.4 Model Dependency

The final fusion architecture depends on:

available data;

sample size;

modality quality;

feature availability;

evaluation results.

The PRD therefore does not mandate a particular neural-network architecture.

48.5 Team Dependency

Successful implementation requires coordination between:

hardware team;

data/ML team;

backend team;

frontend team;

testing/documentation team.

49. Future Scope

49.1 Additional Physiological Signals

Future versions could potentially support additional physiological channels where ethically and technically appropriate.

Examples:

ECG;

EDA/GSR;

respiration;

temperature.

These should not be assumed to be part of the first version.

49.2 Advanced Audio Analysis

Future versions could investigate:

richer speech embeddings;

speaker-independent representations;

advanced prosody analysis;

multilingual speech analysis.

49.3 Advanced Computer Vision

Future versions could investigate:

temporal facial models;

advanced action-unit analysis;

posture analysis;

multimodal body-language analysis.

49.4 Improved Multimodal Fusion

Future versions may explore:

Feature-level fusion

Decision-level fusion

Attention-based fusion

Temporal fusion

Adaptive modality weighting

The implementation decision should be based on experimental evaluation rather than assuming one architecture is inherently superior.

49.5 Missing-Modality Intelligence

Future versions could make the fusion model more robust when one modality becomes unavailable.

For example:

Physiology ✓

Audio ✓

Vision ✗

The system could still produce a result if the selected model supports missing-modality operation.

49.6 Mobile/Edge Deployment

A future version could move more processing onto an edge device or mobile application.

Potential benefits:

lower latency;

reduced network dependence;

improved privacy;

portable experimentation.

49.7 Larger Dataset

The system could eventually support:

larger participant populations;

multiple languages;

different environments;

different question categories;

cross-device validation.

49.8 Longitudinal Research

Future studies could examine how an individual's signal patterns change across repeated sessions.

50. Definition of Done and Final Acceptance Criteria

50.1 Purpose

MOSAIC shall be considered complete only when the agreed product requirements have been satisfied and the complete experimental workflow has been validated.

50.2 Core Product Acceptance

The system must allow an authorized operator to:

Create Experiment

↓

Register Participant

↓

Create Session

↓

Check Devices

↓

Collect Baseline

↓

Present Question

↓

Collect Multimodal Data

↓

Complete Trial

↓

Process Data

↓

Generate Modality Predictions

↓

Perform Fusion

↓

Store Results

↓

Generate Report

50.3 Data Acceptance

The system must preserve the relationship:

Participant

↓

Session

↓

Trial

↓

Question

↓

Physiology + Audio + Vision

↓

Features

↓

Predictions

↓

Ground Truth

↓

Evaluation

50.4 Hardware Acceptance

Before final experimentation:

required hardware must be identified;

sensors must be tested;

power requirements must be validated;

device communication must be validated;

sensor failure must be handled;

collected signals must be checked for quality.

The exact hardware BOM and wiring are not acceptance criteria of this software PRD and should be maintained in the separate hardware/implementation document.

50.5 Dataset Acceptance

The final dataset must:

contain unique participant IDs;

contain unique trial/session identifiers;

contain valid ground-truth labels;

distinguish missing values from valid measurements;

document modality availability;

contain appropriate metadata;

have a defined version;

have documented feature definitions.

50.6 ML Acceptance

The ML pipeline must:

train using the approved training data;

evaluate on appropriately separated data;

avoid participant leakage;

report multiple evaluation metrics;

evaluate individual modalities;

evaluate multimodal fusion;

record model versions.

50.7 Fusion Acceptance

The fusion system must demonstrate that:

individual modality predictions can be generated;

available modality information can be combined;

unavailable modalities are handled appropriately;

the final prediction is traceable to the models used;

fusion performance can be compared against individual modalities.

50.8 Quality Acceptance

The system must identify poor-quality recordings rather than blindly treating them as valid.

At minimum, the project should be capable of identifying:

Missing signal

Poor physiological quality

No/poor speech

Poor audio

No face

Poor video

Synchronization problem

50.9 Reporting Acceptance

The final system should generate an experiment-level report containing:

dataset information;

participant/trial counts;

modality availability;

data-quality information;

model versions;

individual model metrics;

fusion metrics;

confusion matrices;

error analysis;

limitations.

50.10 Ethical Acceptance

The final product must not claim that it can determine deception with certainty.

The documentation and UI must clearly communicate that the output is an experimental machine-learning classification, influenced by the quality and limitations of the collected data.

50.11 Documentation Acceptance

Before project completion, the team should have separate documentation for:

Product Requirements Document

Defines:

What MOSAIC should do and why.

Implementation Document

Defines:

How MOSAIC will be built.

Hardware Document

Defines:

Which components are used and how they are connected.

ML/Research Methodology

Defines:

How the models are trained, evaluated and validated.

Dataset Documentation

Defines:

What every dataset column means and how it was collected/generated.

PRD COMPLETE — 50 SECTIONS

The complete structure is now:

PHASE 1 — PRODUCT FOUNDATION

01 Product Overview

02 Problem Statement

03 Product Vision

04 Product Objectives

05 Scope

06 Users & Stakeholders

07 Use Cases

08 Assumptions

09 Constraints

10 End-to-End Workflow

PHASE 2 — SYSTEM & DATA

11 Product Workflow

12 Product Architecture

13 Physiological Channel

14 Audio Channel

15 Computer Vision Channel

16 Data Synchronization

17 Dataset Requirements

18 Data Dictionary

19 Data Quality

20 Experimental Design

PHASE 3 — FUNCTIONAL PRODUCT

21 Functional Requirements

22 UI Requirements

23 Real-Time Monitoring

24 Experiment Execution

25 Model Management

26 Modality Predictions

27 Multimodal Fusion

28 Confidence & Uncertainty

29 Explainability

30 Results & Reporting

PHASE 4 — PLATFORM & OPERATIONS

31 Data Storage & Lifecycle

32 User Roles & Access Control

33 Consent & Privacy

34 Security

35 Hardware & Device Management

36 Calibration & Readiness

37 Offline & Connectivity

38 Notifications & Alerts

39 Audit Logging

40 Accessibility & Usability

PHASE 5 — QUALITY, RESEARCH & COMPLETION

41 Performance

42 Reliability

43 Testing & QA

44 Model Evaluation

45 Data Leakage & Experimental Validity

46 Ethics & Safety

47 Risk Management

48 Assumptions & Dependencies

49 Future Scope

50 Definition of Done & Acceptance Criteria

One important distinction for the next document

Since you're planning to build MOSAIC and your friend will provide the fully curated dataset, don't start implementation by blindly creating all the 300+ CSV columns we discussed earlier.

MOSAIC — Dataset Schema & Data Dictionary

Document Type: Data Specification
Project: MOSAIC — Multimodal Orchestration of Signals Across Integrated Channels
Purpose: Define exactly how experimental data must be represented before ML implementation begins.

1. Purpose of This Document

This document defines the structure, naming conventions, relationships, data types, validation rules, and meaning of the data that MOSAIC will consume.

It is not the ML implementation document.

It answers:

“What data does MOSAIC expect, what does every field mean, and how are the modalities connected?”

The schema must support the three primary channels:

MOSAIC

│

┌───────────┼───────────┐

↓ ↓ ↓

Physiological Audio Vision

│ │ │

└───────────┼───────────┘

↓

Feature Layer

↓

Fusion Layer

↓

Result

2. Fundamental Data Principle

The most important design decision is:

One row should represent one experimental trial/response, not one participant.

For example:

Participant P001

│

├── Trial 001

├── Trial 002

├── Trial 003

├── Trial 004

└── Trial 005

Therefore, if you eventually have:

300 participants × 10 trials

you would have approximately:

3,000 trial records.

This is much more useful than having only 300 rows.

3. Entity Hierarchy

The dataset should follow this relationship:

Experiment

│

├── Participant

│ │

│ └── Session

│ │

│ └── Trial

│ │

│ ┌───────────┼───────────┐

│ ↓ ↓ ↓

│ Physiology Audio Vision

│ │ │ │

│ └───────────┼───────────┘

│ ↓

│ Features

│ ↓

│ ML Models

│ ↓

│ Prediction

│ ↓

│ Ground Truth

This relationship is essential for your project.

4. Primary Identifiers

Every trial must be uniquely identifiable.

Required columns

experiment_id

participant_id

session_id

trial_id

question_id

Example

experiment_id = EXP001

participant_id = P023

session_id = S02301

trial_id = T023005

question_id = Q005

These IDs allow you to connect the three modalities.

5. Experiment Metadata

6. Participant Metadata

Avoid unnecessary personally identifiable information.

Participant names should not be required by the ML dataset.

7. Session Metadata

8. Trial Metadata

This is the core table.

9. Ground Truth

This needs special attention.

The dataset should contain a ground-truth field determined by the experimental protocol.

Recommended fields:

ground_truth_label

ground_truth_binary

ground_truth_source

ground_truth_confidence

annotation_status

Example:

ground_truth_label = truthful

ground_truth_binary = 0

or:

ground_truth_label = deceptive

ground_truth_binary = 1

Do not calculate ground truth from:

heart rate

SpO2

stuttering

blinking

gaze

model prediction

Those are features/predictions, not ground truth.

10. Physiological Channel

The physiological channel should contain the measurements actually available from your friend's hardware.

Core fields:

spo2_percent

heart_rate_bpm

perfusion_index

pulse_signal_quality

sensor_contact_quality

Baseline:

baseline_spo2_percent

baseline_heart_rate_bpm

baseline_perfusion_index

Derived:

spo2_change_from_baseline

heart_rate_change_from_baseline

heart_rate_percent_change

perfusion_index_change_from_baseline

11. Physiological Signal Features

If raw PPG/beat-level information is available:

mean_rr_interval_ms

median_rr_interval_ms

sdnn_ms

rmssd_ms

nn50_count

pnn50_percent

heart_rate_variability

Only include these if the hardware/data actually supports reliable beat-to-beat intervals.

Never fill unsupported physiological features with invented values.

12. Audio Channel

Core fields:

audio_duration_seconds

speech_duration_seconds

silence_duration_seconds

speech_to_silence_ratio

response_latency_ms

speaking_rate_wpm

articulation_rate_wpm

word_count

syllable_count

13. Speech Hesitation

Because your friend's project specifically considers audio stuttering:

pause_count

mean_pause_duration_ms

maximum_pause_duration_ms

filler_word_count

filler_word_rate

hesitation_count

hesitation_rate

false_start_count

restart_count

self_correction_count

repetition_count

word_repetition_count

syllable_repetition_count

prolongation_count

block_count

stutter_event_count

These are particularly relevant to the audio modality.

14. Voice Features

Recommended:

mean_pitch_hz

minimum_pitch_hz

maximum_pitch_hz

pitch_std

pitch_range_hz

pitch_slope

mean_rms_energy

rms_energy_std

zero_crossing_rate

spectral_centroid

spectral_bandwidth

spectral_rolloff

spectral_flatness

jitter_percent

shimmer_percent

hnr_db

15. MFCC Features

If the audio pipeline provides MFCCs:

mfcc_01_mean

mfcc_01_std

mfcc_02_mean

mfcc_02_std

...

mfcc_13_mean

mfcc_13_std

The exact number should match the actual feature extraction pipeline.

16. Computer Vision Channel

Core fields:

face_detected

face_detection_confidence

face_visibility_ratio

face_occlusion_ratio

facial_movement_score

facial_movement_variance

17. Eye Features

blink_count

blink_rate_per_minute

mean_blink_duration_ms

maximum_blink_duration_ms

eye_aspect_ratio_left

eye_aspect_ratio_right

mean_eye_aspect_ratio

eye_openness_variance

18. Gaze Features

gaze_detected

gaze_confidence

gaze_x

gaze_y

gaze_deviation

gaze_stability

gaze_shift_count

looking_away_ratio

time_looking_at_camera_seconds

time_looking_away_seconds

19. Head Pose

head_pose_confidence

head_yaw_degrees

head_pitch_degrees

head_roll_degrees

head_yaw_std

head_pitch_std

head_roll_std

head_movement_count

head_movement_frequency

head_motion_score

20. Facial Expression

If the CV model actually provides expression probabilities:

neutral_expression_probability

happy_expression_probability

sad_expression_probability

angry_expression_probability

fear_expression_probability

surprise_expression_probability

disgust_expression_probability

facial_expression_confidence

dominant_expression

expression_change_count

expression_stability

21. Mouth / Facial Movement

Useful for connecting speech with computer vision:

mouth_open_ratio

mouth_width

mouth_height

mouth_aspect_ratio

lip_movement_score

lip_movement_variance

mouth_movement_frequency

jaw_movement_score

22. Temporal Features

This is one of the most important parts of the schema.

Instead of only recording:

heart_rate = 95

we want:

baseline_heart_rate = 72

during_answer_heart_rate = 95

change = +23

Recommended:

baseline_window_seconds

question_window_seconds

answer_window_seconds

post_answer_window_seconds

pre_question_hr

during_question_hr

post_question_hr

pre_question_spo2

during_question_spo2

post_question_spo2

pre_question_blink_rate

during_question_blink_rate

post_question_blink_rate

23. Cross-Modality Features

These are derived features that connect modalities.

Examples:

audio_physio_response_latency

heart_rate_change_during_speech

pitch_change_during_response

blink_change_during_response

gaze_change_during_response

head_motion_during_response

These should be created only after the raw modality data is properly synchronized.

24. Data Quality

Every modality should have quality indicators.

Physiological

oximeter_signal_quality

physiological_missing_ratio

physiological_artifact_ratio

Audio

audio_quality_score

audio_snr_db

audio_clipping_ratio

audio_missing_ratio

Vision

video_quality_score

video_blur_score

video_brightness_score

face_detection_quality

face_missing_ratio

25. Hardware Metadata

Since your hardware is still being finalized, keep these fields flexible:

physiological_device_id

microphone_device_id

camera_device_id

microcontroller_device_id

physiological_device_model

microphone_model

camera_model

For example, don't hard-code:

ESP32_C3

into the fundamental data model yet.

The hardware team can finalize that later.

26. Environmental Metadata

Useful experimental metadata:

room_temperature_celsius

room_humidity_percent

ambient_noise_db

lighting_level

camera_distance_cm

camera_angle_degrees

microphone_distance_cm

These can help explain unexpected measurements.

27. Participant State Metadata

Optional but useful:

sleep_duration_hours

caffeine_consumed

caffeine_amount_mg

exercise_before_test

resting_time_before_test_minutes

time_since_last_meal_minutes

These should only be collected if the research protocol permits it.

28. Model Outputs

Keep model outputs separate conceptually from input features.

physiological_model_prediction

physiological_model_probability

audio_model_prediction

audio_model_probability

computer_vision_model_prediction

computer_vision_model_probability

fusion_model_prediction

fusion_model_probability

fusion_model_confidence

29. Dataset Management

Every record should support:

dataset_version

feature_schema_version

preprocessing_version

model_version

annotation_status

quality_control_status

missing_feature_count

outlier_flag

duplicate_record_flag

This will become extremely useful when you start training multiple versions of the model.

30. Recommended Master CSV

If you eventually create one flattened CSV, the logical order should be:

IDENTITY

→ EXPERIMENT

→ PARTICIPANT

→ SESSION

→ TRIAL

→ QUESTION

→ GROUND TRUTH

→ PHYSIOLOGY

→ AUDIO

→ VISION

→ TEMPORAL

→ CROSS-MODAL

→ QUALITY

→ HARDWARE

→ ENVIRONMENT

→ MODEL OUTPUT

→ DATASET METADATA

31. But Don't Force Everything Into One CSV

This is important.

For the actual implementation, I recommend not making a gigantic 300+ column CSV the primary storage format.

Instead:

participants.csv

sessions.csv

trials.csv

physiological_features.csv

audio_features.csv

vision_features.csv

predictions.csv

connected using:

participant_id

session_id

trial_id

Then, if your friend needs a single CSV for ML, generate:

mosaic_ml_dataset_v1.csv

from those tables.

This gives you much cleaner architecture.

32. Example of One Trial

Imagine:

participant_id = P023

session_id = S02301

trial_id = T02305

question_id = Q05

Physiology:

baseline_hr = 72

answer_hr = 91

spo2 = 98

Audio:

response_latency = 820 ms

pause_count = 4

stutter_events = 2

mean_pitch = 183 Hz

Vision:

blink_rate = 18/min

gaze_deviation = 0.31

head_motion = 0.18

Ground truth:

ground_truth_label = deceptive

ground_truth_binary = 1

The three modalities are connected because they all belong to:

T02305

33. The Most Important Rule

Don't invent columns based on what sounds scientifically interesting.

For every proposed column, ask:

Can our actual hardware/dataset produce this value reliably?

If yes:

Include it

If no:

Don't fabricate it

If it can be calculated from valid raw data:

Mark it as DERIVED

For example:

heart_rate_bpm

might be RAW/ACQUIRED.

Whereas:

heart_rate_change_from_baseline

is DERIVED.

34. Data Classification

Every column should eventually have one of these classifications:

This prevents accidental misuse of columns.

35. Example Data Dictionary Entry

Instead of just:

heart_rate_change

your final data dictionary should say:

This level of documentation should eventually exist for every feature.

36. Dataset Validation Rules

Before a dataset enters MOSAIC, it should be checked for:

Identity

participant_id exists

session_id exists

trial_id exists

Uniqueness

trial_id must be unique

Labels

ground_truth ∈ approved classes

Numeric values

Measurements must be within physically/experimentally reasonable ranges.

Missing data

Missing values must be explicitly represented.

Timestamps

All timestamps must follow the same standard.

37. Dataset Versioning

Use:

MOSAIC_DATA_v1.0

for the first approved schema/dataset.

If columns are added:

v1.1

If the structure changes significantly:

v2.0

This prevents your ML experiments from becoming impossible to reproduce.

38. What Happens When Your Friend Gives You the Dataset

This is the next step I recommend.

Don't immediately train the model.

First, we'll take her CSV and perform:

Dataset

↓

Column Inventory

↓

Data Dictionary Mapping

↓

Missing Value Analysis

↓

Data Type Validation

↓

Duplicate Analysis

↓

Participant/Trial Analysis

↓

Ground Truth Analysis

↓

Modality Mapping

↓

Data Leakage Check

↓

Final MOSAIC Schema

Then we'll know exactly what your actual dataset contains.

39. What You Can Work On Today

Since you're waiting for your teammates to finalize the hardware and your friend to give you the curated dataset, don't wait idle.

You can start with the software foundation that doesn't depend on either.

Today you can prepare:

MOSAIC/

│

├── docs/

│ ├── PRD.md

│ ├── DATA_DICTIONARY.md

│ ├── HARDWARE_SPEC.md

│ ├── ML_METHODOLOGY.md

│ └── IMPLEMENTATION.md

│

├── data/

│ ├── raw/

│ ├── processed/

│ └── sample/

│

├── models/

│

├── reports/

│

└── README.md

Don't implement the ML model yet.

Don't generate fake physiological values and train on them.

Don't lock the hardware architecture yet.

Build the project skeleton + documentation + data contract first.

40. Your Immediate Development Plan

Once the dataset arrives:

Step 1 — Dataset inspection

CSV

↓

columns

↓

rows

↓

participants

↓

trials

↓

labels

Step 2 — Schema mapping

Map every actual column to:

Physiology

Audio

Vision

Metadata

Ground Truth

Quality

Step 3 — Data quality

Check:

missing values

duplicates

outliers

invalid values

class balance

participant distribution

Step 4 — Leakage check

Especially:

same participant in train + test

duplicate trials

label-derived features

future information

Step 5 — Baseline models

Only then build:

Physiology model

Audio model

Vision model

Step 6 — Fusion

Finally:

Physiology

+

Audio

+

Vision

↓

MOSAIC Fusion

The key architecture we're building toward

┌───────────────────┐

│ MOSAIC │

│ Experiment Layer │

└─────────┬─────────┘

│

Experimental

Session

│

┌─────────────┼─────────────┐

│ │ │

▼ ▼ ▼

┌──────────┐ ┌──────────┐ ┌──────────┐

│PHYSIOLOGY│ │ AUDIO │ │ VISION │

│ │ │ │ │ │

│ SpO₂ │ │ Speech │ │ Face │

│ HR │ │ Stutter │ │ Eyes │

│ PPG │ │ Pitch │ │ Gaze │

└────┬─────┘ └────┬─────┘ │ Head │

│ │ │Expression│

│ │ └────┬─────┘

└─────────────┼─────────────┘

▼

┌────────────────┐

│ Feature Layer │

└───────┬────────┘

▼

┌────────────────┐

│ Modality Models│

└───────┬────────┘

▼

┌────────────────┐

│ MOSAIC FUSION │

└───────┬────────┘

▼

┌────────────────┐

│ Experimental │

│ Classification │

└────────────────┘

This is what I would build toward now. When your friend sends the actual curated dataset, we should treat her dataset as the source of truth and map it into this schema rather than forcing her data to match the columns we imagined.

| Version | Date | Status | Description |
| --- | --- | --- | --- |
| 0.1 | Initial | Draft | Initial project concept |
| 0.5 | TBD | Review | Requirements refinement |
| 1.0 | TBD | Baseline | Approved PRD |
| 1.1+ | TBD | Revision | Approved future changes |

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
| --- | --- | --- | --- | --- | --- |
| Physiological | TBD | TBD | TBD | TBD | TBD |
| Audio | TBD | TBD | TBD | TBD | TBD |
| Vision | TBD | TBD | TBD | TBD | TBD |
| MOSAIC Fusion | TBD | TBD | TBD | TBD | TBD |

| Field | Description |
| --- | --- |
| Column Name | Exact dataset field |
| Category | Physiological/Audio/Vision/etc. |
| Data Type | Integer/Float/String/Boolean |
| Unit | bpm, %, Hz, ms, etc. |
| Description | Meaning |
| Source | Sensor/model/manual |
| Required | Yes/No |
| Missing Allowed | Yes/No |
| Valid Range | Expected range |
| Derived | Yes/No |
| Derivation | How calculated |

| Column | Type | Unit | Description |
| --- | --- | --- | --- |
| participant_id | String | — | Unique participant identifier |
| heart_rate_bpm | Float | bpm | Heart rate during trial |
| spo2_percent | Float | % | Oxygen saturation |
| mean_pitch_hz | Float | Hz | Average fundamental frequency |
| blink_count | Integer | count | Number of detected blinks |
| ground_truth_binary | Integer | — | Experimental target label |

| Model | Accuracy | Precision | Recall | F1 |
| --- | --- | --- | --- | --- |
| Physiological | — | — | — | — |
| Audio | — | — | — | — |
| Vision | — | — | — | — |
| Fusion | — | — | — | — |

| Column | Type | Required | Description |
| --- | --- | --- | --- |
| experiment_id | string | Yes | Unique experiment identifier |
| experiment_name | string | Yes | Experiment name |
| experiment_version | string | Yes | Version of experimental protocol |
| experiment_date | date | Yes | Date of experiment |
| experiment_condition | categorical | Yes | Experimental condition |
| question_set_version | string | Yes | Version of question set |

| Column | Type | Required | Description |
| --- | --- | --- | --- |
| participant_id | string | Yes | Anonymous participant identifier |
| age | integer | Optional | Participant age |
| age_group | categorical | Optional | Age category |
| sex | categorical | Optional | Recorded demographic field if approved |
| language | categorical | Yes | Language used during experiment |
| dominant_hand | categorical | Optional | Left/right/ambidextrous |
| education_level | categorical | Optional | Education category |
| occupation_category | categorical | Optional | Occupation category |

| Column | Type | Description |
| --- | --- | --- |
| session_id | string | Unique session |
| session_start_timestamp | datetime | Session start |
| session_end_timestamp | datetime | Session end |
| session_duration_seconds | float | Session duration |
| session_status | categorical | Completed/failed/cancelled |
| number_of_trials | integer | Trials in session |

| Column | Type | Description |
| --- | --- | --- |
| trial_id | string | Unique trial |
| question_id | string | Associated question |
| question_number | integer | Question sequence |
| question_type | categorical | Question category |
| question_category | categorical | Experimental category |
| question_text | text | Question presented |
| participant_answer | text | Recorded/transcribed response |
| trial_start_timestamp | datetime | Trial start |
| trial_end_timestamp | datetime | Trial end |
| answer_start_timestamp | datetime | Response start |
| answer_end_timestamp | datetime | Response end |
| answer_duration_seconds | float | Response duration |

| Classification | Meaning |
| --- | --- |
| RAW | Directly acquired |
| DERIVED | Calculated from raw data |
| METADATA | Describes the experiment |
| GROUND_TRUTH | Experimental label |
| MODEL_OUTPUT | Produced by ML |
| QUALITY | Indicates data quality |

| Field | Value |
| --- | --- |
| Name | heart_rate_change_from_baseline |
| Type | Float |
| Unit | BPM |
| Category | Derived |
| Source | Physiological channel |
| Formula | Trial HR − baseline HR |
| Required | Yes |
| Missing allowed | Yes |
| Description | Difference between trial heart rate and baseline heart rate |
