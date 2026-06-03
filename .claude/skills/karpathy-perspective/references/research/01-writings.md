# Andrej Karpathy: Writings & Mental Models (2017--early 2024)

> **Scope:** 2012--early 2024. No mid-2024+ content, no invented quotes.
> **Orientation:** Prioritizes Karpathy's thinking about instructions, documentation, system prompts, agent behavior, and how to make complex systems understandable. Generic AI philosophy is secondary.
> **Confidence tags:** high (direct, verifiable quote or code) / medium (paraphrased from good notes) / low (I infer from pattern)

---

## 1. "Software 2.0" -- The Foundational Frame (2017)

### 1.1 Source & Date

- **Karpathy, Andrej.** "Software 2.0." Medium, 2017-11-11. https://karpathy.medium.com/software-2-0-a64152b37c35
- Type: blog | Date: 2017-11 | Confidence: high

### 1.2 Core Thesis

> "Neural networks are not just another classifier, they represent the beginning of a fundamental shift in how we develop software. They are Software 2.0." (primary, 2017-11)

He contrasts two paradigms:

| Software 1.0 | Software 2.0 |
|---|---|
| Human writes explicit instructions (.cpp, .py) | Human curates datasets + specifies architecture skeleton |
| Compiled into binary | Training compiles dataset into weights (the "binary") |
| Deterministic, verifiable line-by-line | Optimization-based, weights are "human-unfriendly" |
| Programmers write code | "Programmers" (data labelers) curate, clean, grow datasets |

### 1.3 Key Arguments

1. **The abstraction is the dataset, not the code.** (primary, 2017-11)
   > "In Software 2.0 most often the source code comprises 1) the dataset that defines the desirable behavior and 2) the neural net architecture that gives the rough skeleton of the code."

2. **Software 2.0 is computationally homogeneous.** (primary, 2017-11)
   > "A typical neural network is, to the first order, made up of a sandwich of only two operations: matrix multiplication and thresholding at zero (ReLU)."

3. **Modules meld into an optimal whole.** (primary, 2017-11)
   > "If two Software 2.0 modules that were originally trained separately interact, we can easily backpropagate through the whole."

4. **The programmer's job shifts from writing code to designing training signals.** This is the core redefinition of what "programming" means.

### 1.4 Predictions (from 2017)

- Short term: Software 2.0 "will become increasingly prevalent in any domain where repeated evaluation is possible and cheap, and where the algorithm itself is difficult to design explicitly." (primary, 2017-11)
- He called for "Software 2.0 IDEs" that help with dataset workflows, and "Software 2.0 Github" where repositories are datasets and commits are label edits.
- Long term: "When we develop AGI, it will certainly be written in Software 2.0." (primary, 2017-11)

### 1.5 Recurrence Check

"Software 2.0" as a frame appears in at least 6 contexts between 2017 and 2024:
- The original 2017 Medium post
- Tesla ScaledML 2020 talk: "the neural net is eating through the software stack"
- CVPR 2021 keynote: explicitly references the Software 2.0 frame for Autopilot's migration from C++ to neural nets
- "Gradient descent can write code better than you. I'm sorry." tweet (2017-08-04, primary)
- "Deep learning is human-assisted but mostly constraint-driven software development" tweet (2021-09-19, primary)
- Self-driving as a case study for AGI (2024-01, primary)

This is a core, persistent mental model.

---

## 2. "Leaky Abstractions" -- The Backprop Warning (2016-2019)

### 2.1 Source & Date

- **Karpathy, Andrej.** "Yes you should understand backprop." Medium, 2016-12-19. https://karpathy.medium.com/yes-you-should-understand-backprop-e2f06eab496b
- **Karpathy, Andrej.** "A Recipe for Training Neural Networks." karpathy.github.io, 2019-04-25. http://karpathy.github.io/2019/04/25/recipe/
- Type: blog | Date: 2016-12 and 2019-04 | Confidence: high

### 2.2 Core Argument

> "The problem with Backpropagation is that it is a leaky abstraction." (primary, 2016-12)

And in the Recipe post:
> "Backprop + SGD does not magically make your network work. Batch norm does not magically make it converge faster. RNNs don't magically let you 'plug in' text." (primary, 2019-04)

### 2.3 Two Foundational Observations (from Recipe, 2019-04)

1. **Neural net training is a leaky abstraction** -- unlike `requests.get(url)` which hides HTTP complexity, neural net libraries hide nothing crucial.
2. **Neural net training fails silently** -- misconfigured nets "will train but silently work a bit worse" with no exception thrown.

### 2.4 The Recipe Steps (procedural mental model)

1. **Become one with the data** -- spend hours inspecting thousands of examples manually
2. **Set up end-to-end eval skeleton + get dumb baselines** -- fix random seed, verify loss at init (`-log(1/n_classes)`), overfit one batch
3. **Overfit** -- get a model large enough to overfit training set, "Don't be a hero" on architecture, use Adam lr=3e-4
4. **Regularize** -- get more data > data augmentation > pretraining > dropout > weight decay > early stopping
5. **Tune** -- random search over grid search; "the state of the art approach" is an intern (joking)
6. **Squeeze out the juice** -- ensembles (~2% guaranteed gain), leave it training

### 2.5 Recurrence Check

- "Yes you should understand backprop" (2016-12) -- the thesis
- "A Recipe for Training Neural Networks" (2019-04) -- the full methodology, explicitly references the 2016 post
- CS231n assignments intentionally required manual backprop implementation (2015-2017)
- "Becoming a Backprop Ninja" section in Hacker's Guide to Neural Networks (pre-2015, primary)
- Makemore Part 4 lecture (2022-10): "backprop is a leaky abstraction" -- same phrase, 6 years later
- Tweet (2018-07-01): "Common neural net mistakes: not overfitting a single batch, forgetting train/eval mode..."

This is Karpathy's most persistent warning, spanning his entire career.

---

## 3. "Data Engine" -- The Operational Loop (2019-2022, Tesla era)

### 3.1 Source & Date

- **Karpathy, Andrej.** "AI for Full-Self Driving at Tesla." ScaledML Conference 2020, 2020-04-20. https://www.youtube.com/watch?v=hx7BXih7zx8
- **Karpathy, Andrej.** CVPR 2021 Workshop on Autonomous Driving keynote, 2021-06-20. https://www.youtube.com/watch?v=g6bOwQdCJrc
- **Karpathy, Andrej.** Tesla AI Day 2021 presentation, 2021-08-19. https://www.youtube.com/watch?v=j0z4FweCy4M
- Tweet (2022-12-05): "Competitive advantage in AI goes not to those with the best models but those with a data engine." (primary)
- Type: talks + tweet | Date: 2020-2022 | Confidence: high

### 3.2 Core Concept

The Data Engine is a closed-loop iterative process (primary, from ScaledML 2020):

1. Deploy models in "shadow mode" to the fleet
2. Observe predictions; detect lack of health (flicker, uncertainty, surprise)
3. Source difficult cases via "triggers" (221 manual triggers as of CVPR 2021)
4. Label them (human + auto-labeling offline with heavy models)
5. Add to training set and retrain
6. Repeat (7 shadow mode rounds for one release)

### 3.3 Key Quotes

> "Competitive advantage in AI goes not to those with the best models but those with a data engine." (primary, tweet, 2022-12-05)

> "We have lots of different ways of sourcing difficult cases and then we upload images and we look through them, we label some of them and incorporate them into our training set." (primary, ScaledML 2020)

> "We place just as much work into massaging the test sets as we do into training sets." (primary, ScaledML 2020)

> "A good neural network training pipeline has data that is large, clean, and diverse. With that, 'Success is guaranteed.'" (paraphrased from CVPR 2021, medium confidence)

### 3.4 "Operation Vacation"

The ultimate goal of the Data Engine: automation so thorough that "only the data labeling team is required as all other processes become automated for continuous self-driving improvement" -- the AI team could "go on actual vacation." (primary, PyTorch at Tesla talk, 2019-11)

### 3.5 Recurrence Check

- ScaledML 2020: full articulation of the data engine loop
- CVPR 2021: updated with 221 triggers, 7 shadow mode rounds, auto-labeling
- Tesla AI Day 2021: HydraNet architecture feeding the data engine
- Tweet (2022-12-05): the most succinct formulation
- "Sorting your dataset descending by loss guarantees finding something unexpected, strange and helpful" (tweet, 2020-10-02, primary)
- "The correct place to examine training data is immediately before it feeds into the network" (tweet, 2020-11-17, primary)

The Data Engine concept appears consistently across 3+ years of Tesla talks and tweets.

---

## 4. "The Hottest New Programming Language is English" -- Prompt Engineering as Programming (2023)

### 4.1 Source & Date

- **Karpathy, Andrej.** "The hottest new programming language is English." Twitter/X, 2023-01-24. https://twitter.com/karpathy/status/1617979122625712128
- **Karpathy, Andrej.** Follow-up thread providing supporting articles. Twitter/X, 2023-02-19. https://twitter.com/karpathy/status/1627366413840322562
- Type: tweet | Date: 2023-01 and 2023-02 | Confidence: high

### 4.2 Core Thread Content

Karpathy's viral tweet and his follow-up thread (9 tweets, 2023-02-19) lay out the evidence:

1. **GPT-3 paper** showed LLMs perform in-context learning and can be "programmed" inside the prompt with input:output examples (primary, referencing arxiv.org/abs/2005.14165)
2. **Prompt programming papers** (Large Language Models are Zero-Shot Reasoners, arxiv.org/abs/2205.11916; and others) show prompts can program the "solution strategy" for complex multi-step reasoning tasks (primary)
3. **"GPTs don't 'want' to succeed. They want to imitate. You want to succeed, and you have to ask for it."** (primary, 2023-02) -- one of his most important prompt design principles
4. **"Building A Virtual Machine inside ChatGPT"** -- rules and input/output specifications declared in English, conditioning the GPT into a particular role (primary)
5. **ChatGPT as voice assistant** -- "significantly more capable and personalized than Siri/Alexa/etc., and it was programmed in English" (primary)
6. **LLM as state machine** -- "use an LLM as 'logic' that takes state as JSON blob and modifies it based on English description" (primary)
7. **Bing Chat prompt** -- "the identity is constructed and programmed in English, by laying out who it is, what it knows/doesn't know, and how to act" (primary)
8. **Prompt engineer as "LLM psychologist"** -- "These examples illustrate how prompts 1: matter and 2: are not trivial, and why today it makes sense to be a 'prompt engineer' ... I also like to think of this role as a kind of LLM psychologist." (primary, 2023-02)
9. **GPTs run natural language programs by completing the document** -- "This new programming paradigm has the potential to expand the number of programmers to ~1.5B people." (primary, 2023-02)

### 4.3 Key Additional Tweet on AutoGPTs

> "Next frontier of prompt engineering imo: 'AutoGPTs'. 1 GPT call is just like 1 instruction on a computer. They can be strung together into programs. Use prompt to define I/O device and tool specs, define the cognitive loop, page data in and out of context window, .run()." (primary, tweet, 2023-04-02)

> "Interesting non-obvious note on GPT psychology is that unlike people they are completely unaware of their own strengths and limitations. E.g. that they have finite context window. That they can just barely do mental math. That samples can get unlucky and go off the rails. (so I'd expect the good prompts to explicitly address things like this)" (primary, tweet, 2023-04)

### 4.4 Recurrence Check

- "GPT is a general-purpose computer reconfigurable at runtime via natural language prompts" (tweet, 2022-11-18)
- "Humans program each other via prompt engineering too; programming becomes applied psychology of neural nets" (tweet, 2022-02-26)
- The entire 9-tweet thread from 2023-02
- State of GPT talk at Microsoft Build 2023: whole section on prompt engineering, chains, agents
- "I really am mostly programming in English now" (2025 tweet about his coding workflow, referencing the earlier thread)

---

## 5. "State of GPT" -- The LLM OS & Prompt Engineering Methodology (2023)

### 5.1 Source & Date

- **Karpathy, Andrej.** "State of GPT." Microsoft Build 2023 talk, 2023-05. https://www.youtube.com/watch?v=bZQun8Y4L2A
- Also: 1-hour "Intro to Large Language Models" talk, 2023-11-23. https://www.youtube.com/watch?v=zjkBMFhNj_g
- Type: talks | Date: 2023-05 and 2023-11 | Confidence: high

### 5.2 Training Recipe (4 Stages)

1. **Pretraining** -- 99% of compute, internet-scale data, thousands of GPUs, months
2. **Supervised Finetuning** -- small, high-quality human-written prompt-response pairs
3. **Reward Modeling** -- train a reward model on comparisons
4. **Reinforcement Learning (RLHF)** -- PPO to optimize the policy against the reward model

### 5.3 LLM Psychology (from the talk)

> "LLMs don't want to succeed. They want to imitate training sets with a spectrum of performance qualities. You want to succeed and you should ask for it." (primary, 2023-05)

> "They don't reflect, they don't sanity check, they don't correct their mistakes along the way." (primary, 2023-05)

> "Prompting is making up for this difference between these two architectures: Human brains vs LLM Brains." (paraphrased, medium confidence)

### 5.4 Key Techniques for Prompting (from both 2023 talks)

- **Chain of thought** -- ask the model to think step by step
- **Ask for reflection** -- explicitly request the model to check its own work
- **Chains / Agents** -- "Think less 'one-turn' Q&A and more chains, pipelines, state machines, agents" (primary)
- **Condition on good performance** -- include examples of excellent work in the prompt
- **Tool use / plugins** -- offload tasks LLMs aren't good at (math, search, code execution)
- **Retrieval-Augmented LLMs** -- add relevant documents to the prompt
- **Constrained prompting** -- "Prompting languages" that interleave generation, prompting, logical control

### 5.5 The LLM OS Analogy (from Nov 2023 talk)

Karpathy compares LLMs to operating system kernels:
- LLM is the kernel that processes language
- Tools, retrieval, memory management are like OS subsystems
- The prompt is the command-line interface (or the program)
- Security issues: jailbreaks, prompt injection, data poisoning

### 5.6 System 1/2 Thinking

> "LLMs currently only do System 1 thinking -- fast, automatic. They need to develop System 2 -- slow, deliberate, reflective." (paraphrased from Nov 2023 talk, medium confidence)

---

## 6. Minimalism & "Everything Else is Just Efficiency" (2014-2024)

### 6.1 Source & Date

- micrograd README (2020): "A tiny Autograd engine" -- ~100 lines engine + ~50 lines nn library
- nanoGPT README (2022-2023): "The simplest, fastest repository for training/finetuning medium-sized GPTs" -- ~300-line training loop
- **Karpathy, Andrej.** "New art project. Train and inference GPT in 243 lines of pure, dependency-free Python. This is the *full* algorithmic content of what is needed. Everything else is just for efficiency. I cannot simplify this any further." Twitter/X, 2023-04. (primary) -- Later refined to 200 lines
- llama2.c README (2023-07): "one simple 700-line C file (run.c)" -- "focus on minimalism and simplicity"
- minbpe README (2024-02): "Minimal, clean code for the Byte Pair Encoding algorithm"
- llm.c README (2024-04): "LLMs in simple, pure C/CUDA with no need for 245MB of PyTorch or 107MB of cPython"
- Type: GitHub READMEs + tweets | Date: 2020-2024 | Confidence: high

### 6.2 The Core Philosophy

> "Everything else is just for efficiency." (primary, multiple sources)

This is Karpathy's most frequently repeated statement about code. It encodes:
- The algorithm is simple; complexity is optimization
- Understanding comes from stripping away optimization
- The essence fits in a few hundred lines
- All frameworks are just efficiency wrappers

### 6.3 Design Principles (from llama2.c README)

> "This repo is not a complex framework with a 1000 knobs controlling inscrutable code across a nested directory structure of hundreds of files. Instead, I expect most applications will wish to create a fork of this repo and hack it to their specific needs and deployment platforms." (primary, 2023-07)

> "This repo still cares about efficiency, but not at the cost of simplicity, readability or portability." (primary, 2023-07)

From llm.c:
> "Root-folder code should remain simple and readable. PRs that improve performance by 2% at the cost of 500 lines of complex C code or exotic third-party dependencies may be rejected." (primary, 2024-04)

### 6.4 zerogpt (243-to-200 line GPT)

The evolution from 243 lines to 200 lines is itself a statement. Karpathy publicly shared the optimization process:
> "I spent more test time compute and realized that my micrograd can be dramatically simplified even further. You just return local gradients for each op... Huge savings from 243 lines of code to just 200 (~18%)." (primary, tweet, 2023-04)

### 6.5 Recurrence Check

- micrograd (2020): ~100 lines + ~50 lines
- nanoGPT (2022): "simplest, fastest"
- "243 lines" tweet (2023-04) followed by "200 lines" refinement (2023-04)
- llama2.c (2023-07): "simplest, smallest, most hackable"
- minbpe (2024-02): "Minimal, clean code"
- llm.c (2024-04): "simple, pure C/CUDA"
- microgpt (2026-02): the further reduction, calling it the culmination of "a running obsession spanning maybe a decade or two of simplifying and boiling down LLMs to their bare essence" (No Priors podcast)

This is likely Karpathy's most persistent theme, stretching from 2014 to 2026 (with the core being pre-2024).

---

## 7. The "No-Framework Website" Sensibility (2016-2024)

### 7.1 Source & Date

- **Karpathy's website footer:** "0 frameworks were used to make this simple responsive website because I am becoming seriously allergic to 500-pound websites. This one is pure HTML and CSS in two static files and that's it." https://karpathy.ai/ (primary)
- **His blog #3:** "I write it directly and from scratch in simple, readable HTML/CSS. There are no frameworks, static site builders, analytics or RSS feeds, it's just a few .html and .css files that I text edit directly and it works great." https://karpathy.ai/blog/ (primary)
- Type: website | Date: ongoing, visible by at least 2022 | Confidence: high

### 7.2 Significance

This is an expression of the same minimalism in a non-AI domain. It shows that Karpathy's minimalism is not just about code pedagogy -- it is an aesthetic and philosophical position about technology: complexity must justify itself, and it usually doesn't.

### 7.3 Related: arxiv-sanity approach

> "I am running this code currently on the smallest 'Nanode 1 GB' instance indexing about 30K papers, which costs $5/month." (primary, arxiv-sanity-lite README, 2021)

His from-scratch rewrite of arxiv-sanity (arxiv-sanity-lite) was explicitly about simpler, more maintainable, more scalable. He abandoned the old version for being too complex.

---

## 8. "Self-driving as a case study for AGI" (2024-01)

### 8.1 Source & Date

- **Karpathy, Andrej.** "Self-driving as a case study for AGI." karpathy.github.io, 2024-01-21. (primary)
- Type: blog | Date: 2024-01 | Confidence: high

### 8.2 Core Argument

> "Recent developments in our ability to automate driving is a very good early case study of the societal dynamics of increasing automation, and by extension what AGI in general will look and feel like." (primary, 2024-01)

Karpathy defines AGI as: "An autonomous system that surpasses human capabilities in the majority of economically valuable work." (primary, 2024-01)

### 8.3 Key Observations about Automation Dynamics

- The transition to full automation is gradual, not sudden
- Human oversight persists far longer than optimists predict
- Automation happens task by task, not job by job
- "The rate at which this happens will be much slower than what people naively expect" (inferred from the discussion, medium confidence)
- Society is both observer and participant; regulation, labor, materials, and energy constrain expansion
- "The world will not collapse because of this, but will adapt, change, and restructure" (paraphrased from the post, medium confidence)

### 8.4 Intellectual Heirs

The framing -- automation as a gradual process that replaces tasks not jobs, with persistent human oversight, constrained by real-world factors -- draws on the same mental model as the Data Engine. It is Software 2.0 applied to the economy.

---

## 9. CS231n & Teaching Philosophy (2015-2017)

### 9.1 Source & Date

- CS231n course website: https://cs231n.github.io/ (2015-2017)
- **Karpathy, Andrej.** "Hacker's guide to Neural Networks." karpathy.github.io/neuralnets/ (pre-2015)
- Type: course + tutorial | Date: 2014-2017 | Confidence: high

### 9.2 Teaching Approach

> "My personal experience with Neural Networks is that everything became much clearer when I started ignoring full-page, dense derivations of backpropagation equations and just started writing code. Thus, this tutorial will contain very little math (I don't believe it is necessary and it can sometimes even obfuscate simple concepts)." (primary, Hacker's Guide to Neural Networks, pre-2015)

> "I will instead develop the topic from what I refer to as hackers's perspective. My exposition will center around code and physical intuitions instead of mathematical derivations." (primary, pre-2015)

### 9.3 Course Design

- **Bottom-up build approach:** Start from kNN/linear classifiers, then backprop, then full architectures
- **Deliberately painful assignments:** Students wrote forward and backward passes in raw numpy -- intentionally (2016 blog post explains why)
- **"If this makes sense, you understand backpropagation."** (primary, from the Hacker's Guide)
- **Practical readiness before theory:** Software setup and Python/Numpy tutorial in Module 0

### 9.4 "Becoming a Backprop Ninja"

A recurring pedagogical device. The phrase appears in:
- Hacker's Guide to Neural Networks (pre-2015)
- CS231n assignments (2015-2017)
- Makemore Part 4 lecture title (2022-10-11): "Becoming a Backprop Ninja"

This framing -- that manual backprop is a skill you master like a martial art -- reveals his view that deep understanding comes from doing, not reading.

---

## 10. Documentation, Instructions & Agent Design (2022-2024)

### 10.1 Key Sources

- Twitter thread about prompt engineering (2023-01, 2023-02)
- State of GPT talk (2023-05)
- Intro to Large Language Models (2023-11)
- No Priors podcast discussing microgpt (dates unclear but references the pre-2024 micrograd/nanoGPT lineage)
- Various tweets on system prompts

### 10.2 Positions on System Prompts and Instruction Design

**On prompt structure (inferred from his analyses):**
- Identity should be constructed explicitly: "who it is, what it knows/doesn't know, and how to act" (primary, analyzing Bing Chat prompt, 2023-02)
- Rules and I/O specifications should be "declared in English" (primary, 2023-02)
- LLMs should be explicitly told about their own limitations because they are "completely unaware of their own strengths and limitations" (primary, tweet, 2023-04)
- Good prompts address things like finite context window, poor mental math, and unlucky samples

**On agent design:**
> "1 GPT call is just like 1 instruction on a computer. They can be strung together into programs. Use prompt to define I/O device and tool specs, define the cognitive loop, page data in and out of context window, .run()." (primary, tweet, 2023-04-02)

This is essentially a specification for an agent framework: define sensors/actuators, define the loop, manage context window as memory, and execute.

**On the role of documentation (from No Priors podcast, referencing microGPT):**
> "It used to be that you'd write documentation for human users. But you shouldn't do that anymore; instead of HTML documents for humans, you have Markdown documents for agents. If agents get it, they can explain all the different parts." (primary, podcast)

> "I'm not explaining to people anymore; I'm explaining it to agents. If you can explain it to agents, then agents can act as the router." (primary, podcast)

**On "skills" as a documentation format:**
> "A skill is just a way to instruct the agent on how to teach a concept. I could have a skill for microGPT outlining the progression I imagine the agent should take you through." (primary, podcast)

### 10.3 The "Idea File" Concept

> "In this era of LLM agents, there is less of a point/need of sharing the specific code/app, you just share the idea, then the other person's agent customizes & builds it for your specific needs." (primary, tweet, 2025 -- slightly post scope but consistent with pre-2024 themes)

### 10.4 Coding Workflow Observations (from his coding workflow thread)

Note: the full coding workflow thread is from late 2025, which is out of scope. But several observations echo pre-2024 themes:
- "Don't tell it what to do, give it success criteria and watch it go" -- declarative over imperative
- "Get it to write tests first and then pass them" -- test-driven development through agent
- "Change your approach from imperative to declarative to get the agents looping longer and gain leverage" -- this extends the prompt engineering philosophy

---

## 11. Scientific & Intellectual Influences

### 11.1 Books and Papers He Cites (pre-2024)

- **"Attention is All You Need"** (Vaswani et al., 2017) -- the Transformer paper, cited repeatedly in lectures and repos
- **GPT-3 paper** (Brown et al., 2020, arxiv.org/abs/2005.14165) -- cited as evidence for in-context learning as "programming"
- **Whisper paper** (OpenAI, 2022) -- commended for its "vanilla Transformer + massive weakly-labeled dataset + multi-task" approach
- **TinyStories paper** -- referenced in llama2.c as evidence that small LLMs have "surprisingly strong performance if you make the domain narrow enough"
- **Yann LeCun et al. (1989)** backprop paper -- the subject of his 2022 blog post
- **Hamming, "You and Your Research"** -- cited in PhD guide for the principle "have an attack" (problems must be important AND have a plausible approach)
- **J.C.R. Licklider, "Man-Computer Symbiosis" (1960)** -- extensively discussed in a 2023 tweet thread
- **David Foster Wallace, "Roger Federer as Religious Experience"** -- listed in his recommended reading (via edu notes reference)
- **Richard Sutton's "The Bitter Lesson"** -- implicit influence, not explicitly cited but the themes of compute-scale over hand-crafted knowledge are clearly aligned

### 11.2 Physics as Mental Training

> "My most valuable college classes were physics, but for general problem solving intuitions alone: modeling systems with increasingly more complex terms, extrapolating variables to check behaviors at limits, pursuit of the simplest most powerful solutions." (primary, tweet, 2022-04-16)

### 11.3 Intellectual Style

- **From-code-to-concept:** Starts with running code, derives understanding from it, not the reverse
- **Progressive disclosure:** Builds complexity one piece at a time, always with a tangible demo
- **Concrete over abstract:** Shows the actual integers of secp256k1, then generates a keypair, then traces to an address, then broadcasts a live transaction
- **Normalizing struggle:** "Understanding it took me a good half of a day" (Bitcoin post, 2021-06)
- **Self-deprecation as pedagogy:** "I cannot simplify this any further" implies you, the reader, already have everything you need

---

## 12. Criticisms of Common Practice

### 12.1 Against Framework Worship

- Against "500-pound websites" (karpathy.ai footer)
- Against "a complex framework with a 1000 knobs controlling inscrutable code" (llama2.c README)
- Against "245MB of PyTorch or 107MB of cPython" (llm.c README) -- though he uses PyTorch, he insists on understanding what's underneath
- The entire micrograd/nanoGPT/minbpe/llm.c lineage is an argument against opaque tooling

### 12.2 Against "Magical Thinking" in Deep Learning

- "Backprop + SGD does not magically make your network work" (2019)
- "Don't be a hero" -- use battle-tested architectures (2019)
- Neural net training "fails silently" (2019) -- the most dangerous kind of failure
- "A 'fast and furious' approach to training neural networks does not work" (2019)

### 12.3 Against Overcomplication

- "Don't be a hero" on architecture design (2019) -- copy the simplest architecture from the most related paper
- Against grid search when random search is better for neural nets (2019)
- Against unnecessary complexity: "models really like to overcomplicate code and APIs, they bloat abstractions" (2025, post-scope observation consistent with pre-2024 minimalism)

### 12.4 Against "Laundry List" Papers

> "A paper is not a random collection of some experiments you ran." (primary, PhD guide, 2016-09)

> "Avoid incremental-sounding terms like 'combine,' 'modify,' or 'expand.'" (primary, PhD guide, 2016-09)

### 12.5 Against "Cockroach Papers"

> "Avoid incremental work ('cockroach papers') -- they get accepted but have little impact." (primary, PhD guide, 2016-09)

### 12.6 Against Gaming Metrics

> "Academia is small and interconnected -- shortcuts and dishonest practices will catch up to you." (paraphrased from PhD guide, 2016-09, medium confidence)

---

## 13. Self-Coined Terminology (pre-2024)

| Term | First Seen | Definition | Confidence |
|------|-----------|-----------|------------|
| **Software 2.0** | 2017-11 | Neural networks as a new programming paradigm; dataset = source code, training = compilation | high |
| **Data Engine** | 2020-04 | Closed-loop iterative data acquisition: deploy, detect failures, source examples, label, retrain | high |
| **HydraNet** | 2020-04 | Multi-headed neural network with shared backbone, enabling amortized inference and decoupled task finetuning | high |
| **Leaky Abstraction** | 2016-12 | Backprop (and neural net training generally) is an abstraction that hides critical details; applied to backprop then generalized to all NN training | high |
| **Operation Vacation** | 2019-11 | The goal state where the AI pipeline is so automated that the team could theoretically go on vacation | high |
| **LLM Psychologist** | 2023-02 | Alternative name for "prompt engineer" -- someone who understands the "psychology" of LLMs | high |
| **Software 1.0 vs. 2.0** | 2017-11 | Dichotomy: traditional deterministic code vs. learned neural network weights | high |
| **Backprop Ninja** | pre-2015 | Someone proficient at writing manual backward passes; used as motivational framing | high |
| **Shadow Mode** | 2020-04 | Running a new neural network in the background on the fleet without controlling the vehicle, to evaluate its performance before deployment | high |
| **Auto-labeling** | 2020-04 | Using heavy offline neural networks (too slow for real-time) to generate training labels, then cleaned by humans | high |
| **Fails Silently** | 2019-04 | Neural net training bugs produce worse performance without crashing; diagnostic skill is essential | high |
| **Recurrent RNN** (as description of architecture evolution) | 2021-08 | Not a typo -- describing the pattern of RNNs re-appearing at different levels of the architecture stack | medium |

---

## 14. Summary & Synthesis

### 14.1 Sources Found

**Primary sources (direct, verifiable):**
- 10+ blog posts on karpathy.github.io (2012-2024), including: Software 2.0 (2017 via Medium), A Recipe for Training Neural Networks (2019), Deep Neural Nets: 33 years ago (2022), A Survival Guide to a PhD (2016), Hacker's Guide to Neural Networks (pre-2015), Yes you should understand backprop (2016 via Medium), Self-driving as a case study for AGI (2024)
- 70+ fave tweets spanning 2014-2022 (karpathy.ai/tweets.html)
- Key Twitter threads: "Hottest new programming language is English" (2023-01), the follow-up 9-tweet thread (2023-02), AutoGPTs prompt engineering (2023-04)
- 5 major GitHub READMEs: micrograd (2020), nanoGPT (2022), llama2.c (2023), minbpe (2024-02), llm.c (2024-04)
- 4 major talks: ScaledML 2020, CVPR 2021, Tesla AI Day 2021, State of GPT at Microsoft Build 2023
- CS231n course materials (2015-2017)
- No Priors podcast (discussing microGPT and education)
- Karpathy's website footer/design notes

**Secondary sources (notes, summaries, annotations):**
- David Silver's annotated CVPR talk notes (2021)
- ThinkAutonomous blog analysis of HydraNet (2021)
- Pharath Palesuvaran's talk notes (2020)
- Various transcript sites and thread readers

**Date range of primary sources:** 2012-10-22 (state of Computer Vision post) through 2024-04 (llm.c README)

### 14.2 Top 5 Recurring Themes (within verified 2017-2024 scope)

1. **Minimalism and "everything else is just efficiency."** Spans micrograd (2020) through llm.c (2024) through his website design. The algorithm is the thing; frameworks add overhead. Code should be readable, hackable, and stripped to essentials. This is not just an educational technique -- it is an aesthetic and philosophical commitment.

2. **The primacy of data over code.** From Software 2.0 (2017) through the Data Engine (2020-2022) through his tweet about competitive advantage (2022-12). The dataset IS the source code. The architecture is just a skeleton. The training loop is just a compiler. The real work of AI "programming" is data curation, cleaning, and sourcing.

3. **Leaky abstractions demand understanding.** From "Yes you should understand backprop" (2016) through "A Recipe" (2019) through "Becoming a Backprop Ninja" (2022). Abstractions hide failure modes rather than eliminating them. Neural nets "fail silently." You cannot trust the framework. You must understand what is underneath. This applies to autograd, batch norm, RNNs, and by extension, all abstractions.

4. **Prompt as programming.** From "GPT is a general-purpose computer reconfigurable at runtime via natural language prompts" (2022-11) through "The hottest new programming language is English" (2023-01) through AutoGPTs as cognitive loops (2023-04) through the State of GPT talk (2023-05). LLMs are programmable via natural language; prompts are programs; prompt engineering is a new form of programming; good prompts explicitly define identity, limitations, I/O schemas, and cognitive loops.

5. **Iterative, test-driven development.** From the Recipe's "verify loss at init, overfit one batch, build from simple to complex" (2019) through the Data Engine's "deploy, observe failures, retrain, repeat" (2020-2022) through his tweet "success in deep learning is proportional to raw experimental throughput" (2021-01-16). Progress comes from tight feedback loops, concrete verification at each step, and systematic iteration.

### 14.3 Contradictions / Tensions Observed

1. **Minimalism vs. Scale.** Karpathy advocates for minimal code and simplicity while simultaneously working on systems (Tesla Autopilot) that require "14,000 GPUs, 30 petabytes of video cache, 400,000 Python instantiations tracked every second" (Tesla AI Day 2022). The tension is implicit but never explicitly reconciled. [I infer: he sees minimalism as a design principle for understanding, and scale as an operational necessity -- different domains, different rules.]

2. **"Don't be a hero" vs. "Be ambitious."** In the Recipe (2019), he tells practitioners to copy the simplest architecture from the most related paper. In the PhD Guide (2016), he says "a 10x more important problem is at most 2-3x harder to achieve" and urges ambition. These are not contradictory (different contexts -- production ML vs. research) but the tension is instructive: copy architecture, ambition in problem selection.

3. **Optimization as compilation vs. the Data Engine.** Software 2.0 frames training as compilation (one-shot: data + architecture -> weights). The Data Engine is explicitly iterative (deploy, observe, retrain, repeat). The two frames coexist but describe different timescales -- training is compilation, but deployment is continuous improvement. [I infer: he sees single-training as compilation and fleet deployment as CI/CD.]

4. **"English is the hottest programming language" vs. "Backprop is a leaky abstraction."** One celebrates the simplicity of prompting; the other warns that abstraction hides danger. Natural language programming is arguably the leakiest abstraction of all. Karpathy does not explicitly address this tension, but his practical advice (explicitly tell LLMs about their limitations, define I/O schemas carefully) suggests he treats natural language as a programming language that requires equally careful engineering.

5. **Foundation models vs. Train-from-scratch.** In the 33 Years post (2022-03), he predicts that training from scratch becomes obsolete: "in 2055, you will ask a 10,000,000X-sized neural net megabrain to perform some task by speaking (or thinking) to it in English." Yet his own projects (nanoGPT, llama2.c, llm.c) are all about training from scratch. The tension: he predicts the end of self-training while spending enormous energy making self-training more accessible. [I infer: he sees training from scratch as essential for understanding even if it becomes practically unnecessary.]

### 14.4 Known Gaps / Not Found

- **"Hazy recollection"** as a neologism: not found in verified pre-2024 sources. May be from a 2025+ interview.
- **Specific positions on system prompts for AI agents** (beyond the Bing Chat analysis): Karpathy's 2023 tweet analyzing the Bing Chat prompt is the closest we get. He has not (within scope) published a full "how to write system prompts" guide. His analysis focuses on identity construction, limitation declaration, and I/O schemas.
- **"Vibe coding"**: Not found in scope. This term emerged in 2025 and is post-scope.
- **Agentic workflow opinions before 2024**: Limited to his AutoGPT tweet (2023-04) and his State of GPT talk (2023-05). He was more focused on prompt chains and tool use as of 2023; the full "agent swarm" discussion appears in late 2025, out of scope.
- **His views on Claude specifically**: Not found in scope. He occasionally references LLM capabilities generically.
- **Detailed positions on RLHF mechanism design**: His State of GPT talk covers the 4-stage training recipe but does not go deep into RLHF reward model design.

---

## 15. Extended Analysis: What Karpathy Would Say About AGENTS.md Files

Given this skill's purpose -- to use Karpathy's mental models to review system prompts for AI agents -- here is my synthesis of how his pre-2024 thinking applies:

### 15.1 He Would Insist on Explicit Identity and Limitations

From his analysis of the Bing Chat prompt (2023-02), Karpathy identified three critical components of a good system prompt:
1. **Who the agent is** (identity)
2. **What it knows and doesn't know** (knowledge boundaries)
3. **How to act** (behavioral specification)

An AGENTS.md without these explicit declarations would fail his "leaky abstraction" test -- the agent would silently fail in unspecified ways.

### 15.2 He Would Demand Verifiability

From the Recipe (2019): "verify loss at init" and "overfit one batch." Applied to AGENTS.md: every behavior specification should be verifiable. Can you construct a test that the agent follows instruction X? If not, the instruction is ornamental.

### 15.3 He Would Favor Minimalism

From his entire GitHub corpus: "Everything else is just efficiency." Applied to system prompts: every line that doesn't change agent behavior is dead weight. Karpathy would likely argue that most AGENTS.md files are too long, with too many aspirational instructions that cannot be verified and too much context that dilutes the critical signals.

### 15.4 He Would Design for the Cognitive Loop

From his AutoGPT tweet (2023-04): "define I/O device and tool specs, define the cognitive loop, page data in and out of context window, .run()." An AGENTS.md should specify:
- What tools/sensors the agent has
- What the main loop looks like (read, think, act, observe)
- How memory/context management works
- What the stopping conditions are

### 15.5 He Would Treat Natural Language as a Programming Language

From "The hottest new programming language is English" (2023-01): prompts are programs. System prompts should be engineered with the same care as code: clear variable bindings, explicit control flow, no ambiguous references, testable assertions.

### 15.6 He Would Warn about "Silent Failure"

From the Recipe (2019): misconfigured neural nets "will train but silently work a bit worse." Applied to agents: a poorly-written system prompt won't cause the agent to crash -- it will produce subtly worse behavior that is hard to diagnose. The quality of a system prompt cannot be judged by whether the agent "works"; it must be judged by specific behavioral tests.

### 15.7 He Would Structure Documentation for Agents, Not Humans

From the No Priors podcast: "instead of HTML documents for humans, you have Markdown documents for agents." An AGENTS.md should be written to be parsed and followed by an LLM, not just read by a human developer. This means: clear structure, explicit rules, no implied context, testable directives.

---

## 16. Selected Verbatim Quotes (Quick Reference)

| Quote | Source | Date |
|-------|--------|------|
| "Neural networks are not just another classifier, they represent the beginning of a fundamental shift in how we develop software. They are Software 2.0." | Software 2.0 blog | 2017-11 |
| "Gradient descent can write code better than you. I'm sorry." | Twitter/X | 2017-08-04 |
| "The problem with Backpropagation is that it is a leaky abstraction." | Yes you should understand backprop | 2016-12 |
| "Neural net training fails silently." | A Recipe for Training Neural Networks | 2019-04 |
| "Don't be a hero." (on architecture selection) | A Recipe for Training Neural Networks | 2019-04 |
| "3e-4 is the best learning rate for Adam, hands down." | Twitter/X | 2016-11-24 |
| "Competitive advantage in AI goes not to those with the best models but those with a data engine." | Twitter/X | 2022-12-05 |
| "The hottest new programming language is English." | Twitter/X | 2023-01-24 |
| "GPTs don't 'want' to succeed. They want to imitate. You want to succeed, and you have to ask for it." | Twitter/X thread | 2023-02-19 |
| "I also like to think of this role as a kind of LLM psychologist." (on prompt engineers) | Twitter/X thread | 2023-02-19 |
| "Everything else is just for efficiency." | Twitter/X | 2023-04 |
| "I cannot simplify this any further." | Twitter/X | 2023-04 |
| "LLMs are completely unaware of their own strengths and limitations." | Twitter/X | 2023-04-02 |
| "1 GPT call is just like 1 instruction on a computer. They can be strung together into programs." | Twitter/X | 2023-04-02 |
| "A paper is not a random collection of some experiments you ran." | A Survival Guide to a PhD | 2016-09 |
| "Success in deep learning is proportional to raw experimental throughput." | Twitter/X | 2021-01-16 |
| "The Transformer is a magnificient neural network architecture because it is a general-purpose differentiable computer." | Twitter/X | 2022-10-19 |
| "0 frameworks were used to make this simple responsive website because I am becoming seriously allergic to 500-pound websites." | karpathy.ai footer | ongoing |
| "You should not have to feel scared to read the code and understand how it works." | minbpe README | 2024-02 |
| "Sorting your dataset descending by loss guarantees finding something unexpected, strange and helpful." | Twitter/X | 2020-10-02 |
| "If this makes sense, you understand backpropagation." | Hacker's Guide to Neural Networks | pre-2015 |
