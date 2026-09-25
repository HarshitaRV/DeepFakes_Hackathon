# Explanation Guide: How We Reached the Current Prototype

## 1. Purpose of this document
This document explains the evolution of the project from the initial idea to the current local prototype. It is intended as an onboarding and explanation artifact for team members who need to understand:
- why the project exists
- what the product goals were
- what was discussed and decided
- how the spec-guided approach shaped the work
- how the prototype was implemented
- what the current system does and does not do
- how the validation loop was built

This guide is meant to be readable by both technical and non-technical team members. It is a narrative and process document, not just a technical file.

---

## 2. Starting point: the problem statement
The project began with a use case in the README: an explainable multimodal deepfake forensics and provenance tool.

The original problem description made several important points:
- deepfakes are often hybrid and partial rather than fully synthetic
- a simple real/fake score is not actionable
- users need localization of manipulation by time and region
- provenance and metadata matter
- the output should be explainable and human-review-oriented
- the tool should support research, verification, and trust & safety workflows

This was the first major decision: the project was not just “build a deepfake detector.” It was “build evidence-backed forensic analysis that explains itself and supports human judgment.”

That framing shaped the entire effort.

---

## 3. Initial product thinking: why a spec-first approach was needed
Before writing implementation logic, the team needed to answer a few foundational questions:
- who is this for?
- what problem are we solving?
- what does a successful outcome look like?
- what are the boundaries of the MVP?
- what should the prototype avoid claiming?

This is where the spec-driven-development approach became important.

Instead of jumping into code, we first translated the README into structured product artifacts:
- PRD
- technical specification
- backlog
- SDD guide
- product requirements and success criteria

This avoided two major mistakes that often happen in AI hackathons:
1. building a technically interesting but vague system without clear product intent
2. building a black-box classification tool that overclaims certainty

The team consciously avoided the trap of producing a definitive “real/fake” detector without evidence, because the project goal was explainability and review support, not certainty.

---

## 4. The core product decisions that shaped the solution
The requirements in the README led to several product decisions:

### 4.1 Focus on explanation, not binary verdicts
We decided the output should not be a final verdict like “fake” or “real.”
Instead, the system should explain:
- where suspicious signals occur
- which modality is suspicious
- how confident the system is
- whether the content has provenance evidence
- whether the case should go to human review

This became a central principle of the implementation and the narrative.

### 4.2 Support both video and audio analysis
The README emphasized that modern manipulations are often multimodal. The system needed to reason about both:
- visual artifacts in video
- audio anomalies and splice artifacts

This became the architecture basis for the local prototype: separate video and audio analysis pipelines, then merge their evidence.

### 4.3 Keep the solution local and hackathon-friendly
The project is a one-day hackathon. That immediately ruled out a production-scale cloud solution.
The implementation needed to be:
- easy to set up locally
- simple to run on one laptop
- understandable by team members quickly
- sufficient to demonstrate the concept convincingly

This led to the chosen stack: Python + Streamlit + OpenCV + Librosa.

### 4.4 Validate against synthetic data with both clean and suspicious cases
Since there was no existing test data in the repo, the team generated synthetic examples representing both expected positives and expected negatives.
This gave a concrete testing loop:
- clean sample should be low-risk
- suspicious sample should trigger warnings
- evaluation script should print pass/fail clearly

---

## 5. How the spec documents were created
The first major documentation tasks were product-oriented. They were not random documents; they were created to give the project a concrete foundation.

### 5.1 PRD
The PRD defined the product purpose, goals, users, user needs, functional requirements, non-functional requirements, risks, and definition of done.

This served as the “source of truth” for the product and made the project more than a code experiment.

### 5.2 Technical specification
This document described the engineering architecture, data contracts, workflows, and validation strategy.

It established the system design before implementation.

### 5.3 Backlog
The backlog converted the requirements into actionable tasks and release stages.
This gave the project a simple path:
- MVP
- pilot
- production readiness

### 5.4 SDD guide
This explained the broader philosophy: spec-driven development is about making requirements explicit before coding so the team is aligned on core behavior, uncertainty, and constraints.

This was particularly important for a deepfake project because overconfidence is a serious risk.

---

## 6. The prompts that guided the project
The project was developed iteratively, and the prompts were a big part of shaping the direction. The intention was to move from broad idea to concrete, manageable technical implementation.

### Prompt 1: Problem framing
A prompt was used to understand the use case and translate it into a product-level description.

Core intent:
- describe the business problem
- identify target users
- define the desired product function
- focus on explainability and provenance

This produced the initial README-driven framing and the first rough product direction.

### Prompt 2: “Based on the README, generate a plan following spec-driven development principles”
This is where the project turned from a concept into a structure.
The resulting work included:
- core product spec
- requirements
- user goals
- milestone roadmap
- risk register
- acceptance criteria

This step was critical because it established the engineering direction before code creation.

### Prompt 3: “Yes” — create formal SDD artifacts
After the initial plan, the work was expanded into formal artifacts:
- PRD
- technical spec
- backlog
- SDD guide

This was done to make the project understandable to a larger team and to create tangible artifacts that could be referenced later.

### Prompt 4: “Explain SDD and why it matters”
This was a communication step, not only a technical step. It clarified the rationale for the process to team members who may not be familiar with spec-driven work.

This mattered because it explained why the project was deliberately built around requirements, not just an AI demo.

### Prompt 5: “Make the process simple and a working prototype which can run locally too”
This was the pivot toward practical delivery.
It changed the project from a broad conceptual vision into a feasible one-day implementation plan.

The important decision here was to avoid a complex full-stack production architecture and instead build a local, explainable prototype with a strong demo story.

### Prompt 6: “Generate test data or download sample videos”
This created the validation layer.
Since no local media existed, synthetic generation was chosen as the quickest and most controllable approach for a hackathon.

This step created the evaluation loop that distinguishes:
- clean / low-risk cases
- suspicious / signal-rich cases

### Prompt 7: “Add a tiny evaluation script that scores these cases automatically and prints pass/fail results”
This completed the TDD-like validation loop. It gave the project a repeatable quality gate with clear pass/fail output.

This is important because it moves the project from “it seems to work” to “the system has a validation check.”

### Prompt 8: “Generate hackathon submission deck and explain code and architecture with architecture diagrams, sequence diagrams”
This completed the communication side of the project.
It made the work understandable not just to engineers, but also to judges, stakeholders, and future team members.

---

## 7. The architecture decisions made during iteration
As we moved from planning to prototype implementation, a few key design decisions were made.

### 7.1 Keep the app simple and local
We avoided building distributed infrastructure or cloud deployment because the goal was a hackathon demo. This kept the prototype easy to run and explain.

### 7.2 Use a single-file app as the MVP starting point
The initial implementation used a simple Streamlit app in a single file. This was intentionally minimal and easy to reason about.

The app did the following:
- accepted uploaded media
- extracted metadata information
- analyzed stored frames using OpenCV
- processed audio using Librosa
- showed suspicious ranges and a report summary

This was an excellent MVP because it demonstrated the flow cleanly.

### 7.3 Separate reasoning by modality
We intentionally separated the logic into:
- video analysis
- audio analysis
- metadata/provenance summary
- final report generation

This is closer to the real domain problem, where media authenticity often requires multiple evidence streams rather than a single signal.

### 7.4 Keep the report cautious and transparent
The output language was designed to avoid making definitive truths. Instead, it says:
- suspicious segment detected
- risk tier medium
- recommend human review

This aligns strongly with the original README and the SDD principles.

---

## 8. Why the code is intentionally lightweight
The current code is intentionally minimal because the project is a 1-day hackathon prototype. It favors clarity over complexity.

This means:
- fewer moving pieces
- easier debugging
- easier explanation to stakeholders
- faster demo readiness
- less risk of getting stuck in infra or deployment complexity

This design is a deliberate tradeoff and is aligned with the use case.

---

## 9. End-to-end implementation flow
This section explains the actual journey from concept to working prototype.

### Step 1: Understand the problem and write the spec
The README described a clear problem and intended product. The first work was to convert that into structured requirements.

Result:
- product requirements and architecture direction were created
- team alignment improved
- the project stopped being vague and started being concrete

### Step 2: Convert requirements into working backlog and milestone plan
The backlog broke down the work into manageable pieces and set realistic hackathon scope.

This helped avoid overcommitting to a production-grade system.

### Step 3: Choose a local prototype stack
The project selected a stack that is easy to install and run locally:
- Streamlit
- OpenCV
- Librosa
- NumPy
- SciPy
- Pillow
- Mutagen

This stack allows media processing without a heavy cloud environment.

### Step 4: Generate synthetic test media
Because there was no test corpus, the team created synthetic clips and audio files that model:
- clean baseline behavior
- suspicious anomaly behavior

This created a controlled validation set.

### Step 5: Build validation logic
The evaluation script compares generated samples against expected thresholds and prints pass/fail outputs.
This is a crucial step because it forms the automated regression check for the prototype.

### Step 6: Build the local app
The Streamlit app loads a file, analyzes it, and displays a report.
It is not a production product, but it demonstrates the entire pipeline end-to-end.

### Step 7: Validate and iterate
The team ran the validation script, identified mismatches, adjusted the synthetic thresholds, and re-ran the checks until the pipeline behaved as intended.

This is a good example of practical iterative engineering in a short timeframe.

### Step 8: Package the narrative for the demo
The hackathon presentation deck and explanation guide were created to make the project understandable to audiences beyond the technical implementation team.

This is crucial because many hackathon projects fail not because the code is bad, but because the story is not communicated clearly.

---

## 10. The actual code logic and its meaning
The prototype contains a few simple but important heuristics.

### 10.1 Video anomaly detection
The code compares consecutive video frames and computes the mean absolute difference between grayscale values.

Why this matters:
- abrupt inconsistencies often suggest visual manipulation or flicker
- frame-to-frame differences can flag suspicious transitions or hybrid edits

This is intentionally lightweight and explainable.

### 10.2 Audio anomaly detection
The code loads the audio signal, computes chunk magnitudes, and identifies segments with unusually high energy variance.

Why this matters:
- audio tampering often introduces suspicious discontinuity or sudden amplitude shifts
- it is a rough but effective approximation for a hackathon prototype

### 10.3 Metadata and provenance summary
The code reads the file metadata and surfaces a provenance message like:
- no clear provenance chain detected

This is important because provenance is not a proof of authenticity, but it is useful supporting evidence.

### 10.4 Final report generation
The app assembles a plain-language summary with:
- suspicious video findings
- suspicious audio findings
- provenance notes
- risk level
- recommendation for human review

This is the heart of the product position: human-readable forensic explanation.

---

## 11. Why the prototype is honest about limitations
A key product decision in this project is to avoid false certainty.

The current system does not say:
- “this video is definitely fake”
- “this audio is definitely synthetic”

Instead, it says:
- suspicious signal detected
- medium risk
- recommend human review

This is a responsible design and a core part of the product. It is one of the biggest reasons the project aligns with the SDD principles.

---

## 12. Lessons learned from the process
Several important lessons emerged from the work:

### Lesson 1: Product intent matters more than algorithm complexity
A simple but clearly targeted system is more useful than a complex but unclear one.

### Lesson 2: Spec-first work reduces wasted time
By defining the requirement and constraints early, the team avoided unnecessary detours.

### Lesson 3: Local prototypes can still demonstrate meaningful product ideas
A local proof-of-concept is enough to make the concept credible in a hackathon.

### Lesson 4: Synthetic data is valid for quick validation
When real data is unavailable, controlled synthetic tests are a practical method for validating the pipeline and demonstrating logic.

### Lesson 5: Communication is part of the engineering work
The deck, explanation guide, and pitch script are not optional extras—they are part of the product story and the execution quality.

---

## 13. Final state of the project
At this point, the project is a working local prototype with:
- a structured spec foundation
- a realistic hackathon task plan
- local installation instructions
- synthetic validation data
- pass/fail evaluation checks
- local UI and reporting flow
- a clear narrative and deck for demo presentation

This is the result of a methodical but compact end-to-end process from problem framing to runnable prototype.

---

## 14. Summary
The work we did was not just coding. It was a structured progression from a product problem to a working prototype.

We started with a README use case, translated it into a product and engineering specification, reduced the scope to a realistic one-day goal, built a local app, generated validation media, and automated the evaluation process.

This is the story of how we reached the current implementation. It is a strong example of how a spec-driven, hackathon-friendly workflow can turn a conceptual idea into a working local prototype with clear evidence and a persuasive demo narrative.
