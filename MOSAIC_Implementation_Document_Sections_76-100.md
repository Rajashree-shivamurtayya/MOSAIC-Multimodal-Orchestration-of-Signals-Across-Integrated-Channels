# MOSAIC — Implementation & Technical Design Document

## Sections 76–100

---

# Part XII — Security, Privacy & Data Governance

# 76. Security Architecture

## 76.1 Objective

MOSAIC must protect:

- participant information
- experimental recordings
- physiological data
- audio
- video
- extracted features
- model outputs
- authentication credentials
- research results

Security must be designed into the architecture rather than added after implementation.

## 76.2 Security Layers

```text
User Interface
      ↓
Authentication
      ↓
Authorization
      ↓
API Layer
      ↓
Service Layer
      ↓
Database / Storage
      ↓
Infrastructure
```

## 76.3 Security Principles

Implementation must follow:

- least privilege
- secure defaults
- input validation
- explicit authorization
- secure secret management
- auditability
- defense in depth

## 76.4 Authentication

Authentication should be handled centrally.

The backend must verify credentials before allowing protected operations.

## 76.5 Session Security

Authenticated sessions should have:

- session expiration
- token validation
- logout/invalidation
- refresh handling

where applicable.

## 76.6 Password Security

If passwords are implemented, never store plaintext passwords.

Use a strong password-hashing mechanism.

---

# 77. Authorization & Role-Based Access

## 77.1 Purpose

Different users should have different permissions.

Recommended roles:

```text
ADMIN
RESEARCHER
OPERATOR
VIEWER
```

## 77.2 Example Permissions

### ADMIN

Can:

- manage users
- manage configuration
- manage models
- manage datasets
- view system logs

### RESEARCHER

Can:

- create experiments
- manage datasets
- evaluate models
- generate reports

### OPERATOR

Can:

- run sessions
- operate devices
- view trial information

### VIEWER

Can:

- view permitted reports
- view evaluation results

## 77.3 Backend Enforcement

Permissions must be enforced by the backend.

The frontend hiding a button is **not** sufficient authorization.

## 77.4 Resource Authorization

The API should verify that the user is authorized to access the specific:

```text
experiment
participant
session
trial
recording
report
dataset
```

rather than checking only whether the user is logged in.

---

# 78. Input Validation

## 78.1 API Validation

All incoming requests must be validated.

Examples:

```text
required fields
data types
allowed ranges
enum values
string length
file type
file size
```

## 78.2 Physiological Validation

Example sanity checks:

```text
heart rate within configured valid range
SpO₂ within valid range
timestamp valid
signal quality available
```

Invalid measurements should be flagged rather than silently modified.

## 78.3 Audio Validation

Validate:

```text
file format
sample rate
duration
channel count
file size
```

## 78.4 Video Validation

Validate:

```text
format
resolution
frame rate
duration
file integrity
```

## 78.5 File Upload Security

Uploaded files must be:

- type-validated
- size-limited
- stored outside executable locations
- assigned safe filenames
- scanned/validated before processing where appropriate

---

# 79. Privacy Architecture

## 79.1 Privacy Objective

MOSAIC processes potentially sensitive research data, particularly:

- face/video
- voice/audio
- physiological signals
- participant metadata

Therefore, data minimization must be applied.

## 79.2 Data Minimization

Only collect information required for the approved experiment.

Avoid collecting unrelated personal information.

## 79.3 Participant Identifier

Use a research identifier such as:

```text
P001
P002
P003
```

rather than unnecessarily exposing a participant's real identity throughout the system.

## 79.4 Pseudonymization

Where possible:

```text
Participant Identity
        ↓
Private Mapping
        ↓
Research Participant ID
```

The research dataset should primarily operate on the research ID.

## 79.5 Separation of Identity

If personally identifying information is required, store it separately from experimental feature data where practical.

---

# 80. Consent Management

## 80.1 Consent Requirement

Participant consent must be obtained according to the approved academic/research protocol before data collection where applicable.

## 80.2 Consent Record

The system should record:

```text
consent_id
participant_id
consent_status
consent_version
consent_timestamp
recorded_by
```

## 80.3 Consent Versioning

If the consent document changes:

```text
consent_v1
consent_v2
```

must be distinguishable.

## 80.4 Consent Validation

Before starting a session:

```text
if consent_required
    verify consent
else
    prevent session start
```

## 80.5 Withdrawal

The architecture should provide a mechanism to record withdrawal requests and apply the project's approved data-retention/deletion policy.

---

# 81. Data Encryption

## 81.1 Data in Transit

Communication between services should use secure transport where applicable.

Examples:

```text
Frontend → API
API → Database
API → ML Service
API → Storage
```

## 81.2 Data at Rest

Sensitive stored data should use appropriate storage/database protections.

## 81.3 Secret Management

Secrets should be stored in:

```text
environment configuration
secret manager
deployment secret store
```

rather than source code.

## 81.4 Encryption Keys

Keys must not be committed to Git.

Key rotation should be possible where the deployment environment supports it.

---

# 82. Data Retention & Deletion

## 82.1 Retention Policy

The project must define how long each category of data is retained.

Example categories:

```text
Raw recordings
Processed recordings
Features
Predictions
Reports
Logs
Participant metadata
```

## 82.2 Deletion

Deletion must be deliberate and auditable.

## 82.3 Cascading Deletion

The implementation must carefully handle dependencies.

Deleting a participant may affect:

```text
sessions
trials
recordings
features
predictions
reports
```

Do not implement destructive cascading blindly.

## 82.4 Research Preservation

If records must be retained for academic evaluation, the system should archive them instead of deleting them immediately.

---

# Part XIII — Testing Strategy

# 83. Testing Architecture

## 83.1 Testing Layers

MOSAIC should use:

```text
Unit Tests
     ↓
Integration Tests
     ↓
Component Tests
     ↓
System Tests
     ↓
End-to-End Tests
     ↓
Model Evaluation
     ↓
Hardware Validation
```

## 83.2 Testing Objectives

Testing must verify:

- correctness
- reliability
- data integrity
- model pipeline integrity
- device connectivity
- API behavior
- UI behavior
- synchronization
- failure recovery

---

# 84. Unit Testing

## 84.1 Backend

Test:

- validation
- service functions
- database operations
- state transitions
- feature transformations

## 84.2 Frontend

Test:

- components
- state transitions
- validation
- formatting
- error states

## 84.3 ML

Test:

- preprocessing
- feature extraction
- feature ordering
- normalization
- model input generation

## 84.4 Example

```text
Input
 ↓
Preprocessor
 ↓
Expected feature vector
```

The expected output should be deterministic for controlled test data.

---

# 85. Integration Testing

## 85.1 Purpose

Verify that components work correctly together.

## 85.2 Important Integrations

```text
Frontend → API
API → Database
API → ML service
API → Storage
Worker → Database
Worker → ML service
Device → Device adapter
```

## 85.3 Example

```text
Start Trial
   ↓
Create Trial
   ↓
Start Recording
   ↓
Store Recording
   ↓
Extract Features
   ↓
Run Model
   ↓
Store Prediction
```

Every transition should be tested.

---

# 86. End-to-End Testing

## 86.1 Full Scenario

A complete E2E test should simulate:

```text
Login
 ↓
Create Experiment
 ↓
Register Test Participant
 ↓
Configure Questions
 ↓
Connect Test Devices
 ↓
Start Session
 ↓
Run Trial
 ↓
Capture Modalities
 ↓
Process Data
 ↓
Generate Prediction
 ↓
Complete Session
 ↓
Generate Report
```

## 86.2 E2E Test Data

Use synthetic or specifically approved test data.

Do not use real participant recordings unnecessarily.

## 86.3 E2E Success Criteria

The test should verify:

- no data loss
- correct trial association
- correct feature association
- correct model version
- prediction generated
- report generated

---

# 87. Hardware Integration Testing

## 87.1 Physiological Sensor

Test:

```text
device detection
connection
signal acquisition
sampling
disconnect
reconnect
signal quality
```

## 87.2 Power Validation

For the hardware architecture, test the actual selected ESP32-C3 board and power circuit rather than assuming all "C3 Super Mini" boards have identical pin/power behavior.

Verify:

```text
battery voltage
TP4056 output
regulated supply, if used
ESP32 operating voltage
current consumption
charging behavior
```

## 87.3 Sensor Integration

Verify:

```text
MAX30102
SDA
SCL
GND
3.3V
```

against the exact board schematic/datasheet being used.

## 87.4 Microphone

Test:

```text
device detection
sample rate
recording
noise floor
clipping
disconnect
```

## 87.5 Camera

Test:

```text
camera detection
resolution
FPS
lighting
face detection
frame drops
```

---

# 88. Hardware Failure Testing

## 88.1 Sensor Disconnect

Simulate:

```text
sensor connected
      ↓
sensor disconnected
```

Expected behavior:

```text
warning displayed
recording state preserved
error logged
reconnection supported
```

## 88.2 Power Interruption

Test what happens when power is interrupted.

## 88.3 Communication Failure

Simulate lost communication between:

```text
ESP32
computer
backend
```

## 88.4 Recovery

The system should recover gracefully wherever technically possible.

---

# 89. Signal Quality Testing

## 89.1 Purpose

Poor signal quality should not automatically become a model prediction.

## 89.2 Quality Pipeline

```text
Raw Signal
   ↓
Quality Assessment
   ↓
GOOD ─────→ Feature Extraction
   │
WARNING ──→ Feature Extraction + Flag
   │
POOR ─────→ Reject / Retry
```

## 89.3 Physiological Quality

Evaluate:

```text
signal continuity
noise
motion artifacts
sensor contact
missing samples
```

## 89.4 Audio Quality

Evaluate:

```text
noise
clipping
silence
speech detectability
SNR
```

## 89.5 Video Quality

Evaluate:

```text
blur
lighting
face visibility
occlusion
frame drops
```

---

# 90. Data Pipeline Testing

## 90.1 Pipeline

```text
Raw Data
 ↓
Cleaning
 ↓
Segmentation
 ↓
Feature Extraction
 ↓
Validation
 ↓
Dataset
```

## 90.2 Schema Tests

Verify:

- required columns exist
- correct types
- no unexpected schema changes
- feature order matches model expectations

## 90.3 Missing Data

Test:

```text
no audio
no video
no physiological signal
partial trial
```

## 90.4 Duplicate Data

Detect duplicate:

```text
trial_id
recording_id
feature_set_id
```

where uniqueness is required.

---

# 91. ML Pipeline Validation

## 91.1 Reproducibility

Training should record:

```text
dataset version
random seed
feature version
preprocessing version
model configuration
software version
```

## 91.2 Train/Validation/Test Separation

Never evaluate the final model on data used for training.

## 91.3 Participant-Level Splitting

If multiple trials belong to the same participant:

```text
Participant P001
 ↓
ALL trials
 ↓
same split
```

This prevents participant leakage.

## 91.4 Class Distribution

Before training, report:

```text
truthful samples
deceptive samples
participant counts
trial counts
```

---

# 92. Model Evaluation

## 92.1 Required Metrics

At minimum:

```text
Accuracy
Precision
Recall
F1-score
ROC-AUC
```

## 92.2 Confusion Matrix

Store:

```text
True Positive
True Negative
False Positive
False Negative
```

## 92.3 Modality Evaluation

Evaluate separately:

```text
Physiological
Audio
Vision
Fusion
```

## 92.4 Cross-Validation

Where dataset size permits, use an appropriate participant-level validation strategy.

## 92.5 Confidence Intervals

For the final academic evaluation, confidence intervals or variability estimates should be reported where practical.

---

# 93. Multimodal Fusion Validation

## 93.1 Purpose

Verify whether combining modalities provides useful performance compared with individual models.

## 93.2 Comparison

```text
Physiology
      │
Audio ─┼─→ Individual Models
      │
Vision
      │
      ↓
Fusion Model
```

## 93.3 Fusion Tests

Compare:

```text
Physiology only
Audio only
Vision only
Audio + Vision
Physiology + Audio
Physiology + Vision
All modalities
```

where supported by available data.

## 93.4 Missing-Modality Testing

Test:

```text
All available
Audio missing
Vision missing
Physiology missing
```

The system should clearly indicate degraded modality availability.

---

# 94. Ablation Testing

## 94.1 Purpose

Determine whether each modality contributes meaningful information.

## 94.2 Method

Train/evaluate:

```text
Model A = Physiology
Model B = Audio
Model C = Vision
Model D = Physiology + Audio
Model E = Physiology + Vision
Model F = Audio + Vision
Model G = All
```

## 94.3 Reporting

Report:

```text
accuracy
precision
recall
F1
ROC-AUC
```

for each configuration.

## 94.4 Interpretation

Do not automatically assume that adding a modality improves performance.

If performance decreases, report the result honestly and investigate why.

---

# 95. Error Analysis

## 95.1 Purpose

Aggregate metrics alone are insufficient.

The system should identify where predictions fail.

## 95.2 Error Categories

Possible categories:

```text
False Positive
False Negative
Poor Signal
Audio Noise
Face Occlusion
Missing Modality
Incorrect Ground Truth
Data Synchronization Problem
```

## 95.3 Error Review

For each important error, allow researchers to inspect relevant metadata and quality information subject to access controls.

## 95.4 Common Patterns

Look for patterns such as:

```text
high noise → false positives
poor lighting → vision failures
motion artifacts → physiological failures
```

These should be treated as hypotheses to investigate, not automatically assumed causal relationships.

---

# 96. Performance Testing

## 96.1 API Performance

Measure:

```text
request latency
throughput
error rate
```

## 96.2 Processing Performance

Measure:

```text
feature extraction time
model inference time
report generation time
```

## 96.3 Real-Time Requirement

Define a target processing latency appropriate to the prototype.

Example:

```text
Signal Window
     ↓
Feature Extraction
     ↓
Inference
     ↓
UI Update
```

must complete within the chosen real-time threshold.

The exact threshold should be configurable rather than arbitrarily hard-coded.

## 96.4 Load Testing

Test:

```text
multiple sessions
multiple simultaneous API requests
multiple processing jobs
```

---

# 97. CI/CD Pipeline

## 97.1 Purpose

Every code change should pass automated validation before integration.

## 97.2 Pipeline

```text
Git Push
   ↓
Lint
   ↓
Unit Tests
   ↓
Integration Tests
   ↓
Build
   ↓
Security Checks
   ↓
Deploy/Test
```

## 97.3 Frontend Checks

Run:

```text
format
lint
unit tests
build
```

## 97.4 Backend Checks

Run:

```text
format
lint
type checking
unit tests
integration tests
build
```

## 97.5 ML Checks

Run lightweight tests for:

```text
preprocessing
feature schema
model loading
inference
```

Do not retrain large models on every commit unless specifically required.

---

# 98. Git & Branching Strategy

## 98.1 Branch Structure

Recommended:

```text
main
develop
feature/*
fix/*
experiment/*
```

## 98.2 Feature Branches

Example:

```text
feature/audio-processing
feature/vision-processing
feature/device-integration
feature/fusion-model
feature/evaluation-dashboard
```

## 98.3 Pull Requests

Every PR should include:

```text
purpose
changes
testing performed
known limitations
screenshots where relevant
```

## 98.4 Scope Control

A PR should remain focused.

Do not combine:

```text
feature implementation
unrelated refactoring
mass formatting
dependency changes
```

unless necessary.

## 98.5 Commit Strategy

Prefer meaningful commits:

```text
feat: add audio feature extraction
feat: add trial processing API
fix: handle missing sensor data
test: add fusion inference tests
```

---

# 99. API Contract & Versioning

## 99.1 API Design

All API endpoints must have documented:

```text
method
path
authentication
request schema
response schema
errors
status codes
```

## 99.2 Versioning

Use a versioned API namespace, for example:

```text
/api/v1/
```

## 99.3 Example Resource

```text
GET /api/v1/experiments
GET /api/v1/experiments/:id
POST /api/v1/experiments
PATCH /api/v1/experiments/:id
```

## 99.4 Prediction Endpoint

Conceptually:

```text
POST /api/v1/predictions
```

Request:

```json
{
  "trial_id": "TRIAL001",
  "model_version": "fusion_v1"
}
```

Response should identify:

```text
prediction
probability
confidence
model_version
processing_status
```

## 99.5 Error Contract

Use a consistent structure.

Example:

```json
{
  "error": {
    "code": "INVALID_TRIAL",
    "message": "The specified trial is not available for processing."
  }
}
```

## 99.6 Backward Compatibility

Changes to APIs should not unexpectedly break existing clients.

Breaking changes should result in a new API version when appropriate.

---

# 100. Deployment Verification & Release Checklist

## 100.1 Application Verification

Before release:

```text
☐ Frontend builds successfully
☐ Backend builds successfully
☐ Database migrations succeed
☐ Authentication works
☐ Authorization works
☐ APIs respond correctly
☐ Error handling works
```

## 100.2 Hardware Verification

```text
☐ Physiological sensor detected
☐ Signal quality verified
☐ Microphone detected
☐ Audio recording verified
☐ Camera detected
☐ Face detection verified
☐ Power system verified
☐ Disconnect/reconnect tested
```

## 100.3 ML Verification

```text
☐ Model loads
☐ Feature schema matches
☐ Preprocessing version matches
☐ Inference succeeds
☐ Prediction is stored
☐ Model version recorded
```

## 100.4 Data Verification

```text
☐ Trial IDs unique
☐ Session relationships valid
☐ Recordings associated correctly
☐ No accidental participant leakage
☐ Dataset version recorded
☐ Ground truth available for evaluation
```

## 100.5 Security Verification

```text
☐ No secrets committed
☐ Authentication verified
☐ Authorization verified
☐ File uploads validated
☐ Sensitive data protected
☐ Logs do not expose unnecessary personal information
```

## 100.6 Release Verification

The final release should have:

```text
application version
API version
database version
dataset version
feature version
model version
```

recorded together.

---

# Implementation Principle for Sections 76–100

The entire implementation should preserve this fundamental MOSAIC pipeline:

```text
                    MOSAIC
                       │
                       ▼
              ┌────────────────┐
              │ Experiment     │
              │ Configuration  │
              └───────┬────────┘
                      ▼
              ┌────────────────┐
              │ Participant /  │
              │ Session        │
              └───────┬────────┘
                      ▼
              ┌────────────────┐
              │ Trial          │
              └───────┬────────┘
                      ▼
       ┌──────────────┼──────────────┐
       ▼              ▼              ▼
  Physiology        Audio          Vision
       │              │              │
       ▼              ▼              ▼
  Preprocess       Preprocess     Preprocess
       │              │              │
       ▼              ▼              ▼
  Features         Features       Features
       │              │              │
       └──────────────┼──────────────┘
                      ▼
              ┌────────────────┐
              │ Multimodal     │
              │ Fusion         │
              └───────┬────────┘
                      ▼
              ┌────────────────┐
              │ Prediction     │
              └───────┬────────┘
                      ▼
              ┌────────────────┐
              │ Evaluation     │
              └───────┬────────┘
                      ▼
              ┌────────────────┐
              │ Reports        │
              └────────────────┘
```

This keeps the **PRD → implementation → Codex/Antigravity** workflow clean:

- The **PRD** defines *what MOSAIC must do*.
- The **Implementation & Technical Design Document** defines *how the engineering team should build and validate it*.
- The **Codex/Antigravity rules** should instruct the agents to follow both documents and avoid implementing features outside their defined scope.
