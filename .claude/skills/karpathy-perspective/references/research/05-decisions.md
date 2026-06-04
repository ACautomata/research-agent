---
**VERIFIED SCOPE: 2017 – early 2024.** Per user decision (2026-06-03), this skill is bounded to pre-mid-2024 Karpathy to avoid propagating unverified 2024-mid-to-2026 claims. Sections marked **[UNVERIFIED — quarantined]** preserve the original research for future re-verification but are NOT load-bearing for synthesis.
---

# 05 - Karpathy's Major Decisions & Turning Points

Research date: 2026-06-03
Focus: Decisions that reveal his thinking about AI instruction design, agent behavior, product philosophy, and the research-teach-build tradeoff.

---

## A) Each Major Decision

### Decision 1: Joining OpenAI as a Founding Member (December 2015)

**What:** Karpathy joined OpenAI as one of nine founding researchers, recruited by Greg Brockman from a list of top AI talent.

**Public reasoning at the time:** He said he joined "mainly because I heard about who else was on the team" and described it as "storming the temple." The mission (safe, beneficial AGI) and the team quality were the draws. He noted the "moral high ground" of being a nonprofit.

**Actual reasoning (inferred):** Karpathy was finishing his PhD at Stanford under Fei-Fei Li, had already interned at Google Brain (2011, 2013) and DeepMind (2015). He was a known quantity in deep learning. The founding team was a chance to work alongside Ilya Sutskever, John Schulman, and Wojciech Zaremba. His LinkedIn later says he "helped with much of the early recruiting/structuring." This was a bet on people over project -- he didn't know what OpenAI would work on, he knew who he'd work with.

**Outcome:** He worked on generative models (PixelCNN++) and reinforcement learning (agents controlling keyboard/mouse). The work was research-first, no product pressure. He stayed only ~18 months before Musk recruited him to Tesla. OpenAI succeeded in its recruiting mission partly because of Karpathy's public visibility (CS231n, blog, arxiv-sanity).

**Consistency with stated principles:** Joining for the team, not the mission details, is consistent with his later pattern of choosing collaborators over specific projects. He has never joined anything for the money.

**Sources:**
- https://futureoflife.org/recent-news/inside-openai-an-interview-by-singularityhub/ (2015-12-21 interview)
- https://openai.com/index/introducing-openai/ (founding announcement)
- https://linkedin.com/in/andrej-karpathy-9a650716

---

### Decision 2: Leaving OpenAI for Tesla (June 2017)

**What:** Musk poached Karpathy from OpenAI to become Tesla's Director of AI and Autopilot Vision, reporting directly to Musk.

**Public reasoning at the time:** Minimal public statement. He said on Reddit that "the focus will be much more applied than what I've done at OpenAI, and will use techniques more along the lines of ConvNets trained with supervised learning, at scale, and deployed on an embedded system." This was accurate and modest.

**Actual reasoning (revealed later):** On Lex Fridman's podcast years later, he described loving Tesla, loving Elon, and finding the applied work deeply satisfying. The move was essentially: Musk, who co-founded OpenAI and knew Karpathy's work, offered him a chance to deploy neural networks at massive scale on real hardware with a real fleet. For someone whose academic work was in computer vision and who had written the "Software 2.0" essay (published November 2017, just months after joining Tesla), this was the perfect testbed.

**Outcome:** He led Tesla's Autopilot vision team for 5 years, scaling from lane-keeping to city streets. He built the "data engine" pipeline: deploy in shadow mode, detect failures, mine fleet data, auto-label, retrain. This became the canonical example of Software 2.0 in production. He presented at Tesla AI Day 2021 and 2022, giving the most detailed public look at how Tesla trains and deploys neural networks.

**Relevance to AI instruction design:** The Tesla data engine is essentially a system for instructing AI at scale. The "data engine loop" (deploy, observe failure, collect examples, label, retrain) is the Software 2.0 equivalent of debugging a system prompt. The triggers (221 hand-crafted failure detectors running on the fleet) are the hard-coded equivalent of system prompt rules. The auto-labeling pipeline is the "ground truth" generation system.

**Consistency:** This is one of his most consistent decisions. He believed in Software 2.0, he went to the place doing the most ambitious Software 2.0 deployment, and he made it work.

**Post-hoc revision:** None. He has consistently spoken positively about Tesla and Musk, even after leaving.

**Sources:**
- https://techcrunch.com/2017/06/20/tesla-hires-deep-learning-expert-andrej-karpathy-to-lead-autopilot-vision/
- https://electrek.co/2017/06/21/tesla-ai-autopilot-vision/ (Reddit comment about applied focus)
- https://www.technologyreview.com/2017/06/22/151095/teslas-new-ai-guru-could-help-its-cars-teach-themselves/
- https://dynamicallytyped.com/stories/2021/karpathy-autopilot-cvpr/ (CVPR 2021 talk summary)

---

### Decision 3: Writing "Software 2.0" (November 2017)

**What:** Published a blog post arguing that neural networks represent a fundamental shift in how software is written -- not just another ML technique, but a new programming paradigm.

**Public reasoning:** "Neural networks are not just another classifier, they represent the beginning of a fundamental shift in how we develop software." He argued that datasets are the new source code, weights are the new binaries, gradient descent is the new compiler.

**Why this matters for AI instruction design:** Software 2.0 is the intellectual framework that connects all his later work. If neural network weights are "Software 2.0 code," then system prompts are "Software 3.0 code" (his later term for LLM prompts). The same questions apply: how do you debug it? How do you version it? How do you make it observable? His Software 2.0 essay explicitly called for "Software 2.0 IDEs" that help with dataset curation, labeling, and error analysis -- the exact same tooling problem that exists for system prompt engineering today.

**Outcome:** The essay became one of the most cited AI blog posts of the decade. It predicted MLOps, data-centric AI, and the shift from code-writing to dataset-curation. In his 2025 YC talk, he extended it to "Software 3.0" -- prompts as programs -- making the explicit connection between weights-as-code and prompts-as-code.

**Consistency:** Extremely consistent. Every project since (Tesla data engine, nanoGPT, llm.c, vibe coding commentary) follows the Software 2.0/3.0 arc.

**Post-hoc revision:** He extended but never revised. Software 3.0 is additive, not corrective.

**Sources:**
- https://karpathy.medium.com/software-2-0-a64152b37c35 (original essay, 2017-11-11)
- https://www.ycombinator.com/library/MW-andrej-karpathy-software-is-changing-again (2025 YC talk extending to Software 3.0)

---

### Decision 4: Leaving Tesla (July 2022)

**What:** After a 4-month sabbatical, announced departure from Tesla via Twitter.

**Public reasoning at the time:** "It's been a great pleasure to help Tesla towards its goals over the last 5 years and a difficult decision to part ways." Follow-up: "I have no concrete plans for what's next but look to spend more time revisiting my long-term passions around technical work in AI, open source and education."

**Actual reasoning (revealed later):** On Lex Fridman's podcast, he said he "loves Tesla, loves Elon, loves the team" and would "be interested in revisiting it, maybe coming back at some point." He specifically mentioned wanting to "re-sharpen my technical edge" during the sabbatical. The sabbatical itself (announced March 2022) was framed as "rest and travel" but he also said he was "excited to get focused time to re-sharpen my technical edge and train some neural nets."

**Inferred reasoning:** After 5 years of managing a large team and doing applied work, he wanted to return to hands-on technical work and education. The Tesla role had become more managerial (directing hundreds of engineers) and less technical. The sabbatical was a trial separation that became permanent. He left without another job lined up, which suggests the pull was toward freedom rather than toward a specific opportunity.

**Outcome:** He spent ~7 months creating the "Zero to Hero" YouTube series, releasing nanoGPT, and building a public profile as an educator. Then he returned to OpenAI.

**Pattern note:** He leaves cleanly, praises the institution, maintains relationships. No bridge-burning. Musk responded kindly to his departure tweet.

**Consistency with stated principles:** "Open source and education" were cited as long-term passions. The departure directly led to pursuing those passions. Fully consistent.

**Sources:**
- https://techcrunch.com/2022/07/13/tesla-loses-top-ai-executive-who-led-autopilot-vision-team/
- https://www.cnbc.com/2022/07/13/tesla-ai-leader-andrej-karpathy-announces-hes-leaving-the-company.html
- https://electrek.co/2022/03/28/tesla-head-ai-andrej-karpathy-sabbatical-people-worried/ (sabbatical announcement)

---

### Decision 5: Starting the "Zero to Hero" YouTube Series (September 2022 - ongoing)

**What:** Began publishing a YouTube series building neural networks from scratch in code, starting with micrograd and progressing through makemore to building GPT from scratch.

**Public reasoning:** The GitHub repo says "A course on neural networks that starts all the way at the basics." His website frames it as two parallel tracks: technical and general-audience.

**Why YouTube:** He had been teaching since CS231n (2015). YouTube was the platform that maximized reach for educational content about AI. No university bureaucracy, no enrollment caps, no tuition. The format (long-form code-along videos with Jupyter notebooks) matches his belief that understanding comes from building, not from reading.

**Outcome:** The series became the de facto standard for learning deep learning fundamentals. It spawned nanoGPT, build-nanoGPT, and ultimately llm.c. The GitHub repo has tens of thousands of stars. The videos have millions of views.

**Relevance to AI instruction design:** The Zero to Hero series IS a case study in how to instruct a human (not an AI) through complex material. The structure -- start from nothing, build incrementally, each commit is a clean step, explain before implementing -- is the same structure he later advocates for system prompt design. His GitHub READMEs (nanoGPT: "~300-line boilerplate training loop and `model.py` a ~300-line GPT model definition") are the human equivalent of a well-structured system prompt: minimum surface area, maximum clarity, no unnecessary abstraction.

**Sources:**
- https://karpathy.ai/zero-to-hero.html
- https://github.com/karpathy/nn-zero-to-hero

---

### Decision 6: Releasing nanoGPT as Open Source (December 2022)

**What:** Released nanoGPT, "the simplest, fastest repository for training/finetuning medium-sized GPTs." A rewrite of minGPT prioritizing "teeth over education."

**Public reasoning:** minGPT had become "referenced across a wide variety of places (notebooks, blogs, courses, books, etc.) which made me less willing to make the bigger changes I wanted to make to move the code forward." He also "wanted to change the direction a bit, from a sole focus on education to something that is still simple and hackable but has teeth (reproduces medium-sized industry benchmarks, accepts some tradeoffs to gain runtime efficiency, etc)."

**The design philosophy:** ~300 lines of training loop, ~300 lines of model definition. "That's it." The code is "plain and readable." This is not an accident -- it's a deliberate choice to make the code a teaching tool first and a production tool second, but with enough "teeth" to actually reproduce GPT-2.

**Evolution into llm.c:** nanoGPT begat build-nanoGPT (the video companion) which begat llm.c (the C/CUDA reimplementation). The compression arc: micrograd (scalar autograd, ~150 lines) -> minGPT (~300 lines) -> nanoGPT (~600 lines) -> llm.c (~1000 lines C) -> microgpt (243 lines, pure Python, no dependencies). Each iteration strips away another layer of abstraction.

**Relevance to AI instruction design:** Each repo in this lineage is a masterclass in how to document a system for both humans and AIs. The READMEs have: (1) a one-line description of what the repo does, (2) a numbered file listing explaining each file's role, (3) a quick-start example, (4) explicit design constraints. This is exactly how a good system prompt should be structured.

**Post-hoc revision:** In November 2025, he added a note to nanoGPT: "nanoGPT has a new and improved cousin called nanochat. It is very likely you meant to use/find nanochat instead. nanoGPT (this repo) is now very old and deprecated but I will leave it up for posterity." Clean deprecation, no deletion.

**Sources:**
- https://github.com/karpathy/nanoGPT
- https://github.com/karpathy/minGPT (note about nanoGPT rewrite motivation)

---

### Decision 7: Returning to OpenAI (February 2023)

**What:** Announced on Twitter: "Some personal news: I am joining OpenAI (again :)). Like many others both in/out of AI, I am very inspired by the impact of their work and I have personally benefited greatly from it. The future potential is especially exciting; it is a great pleasure to jump back in and build!"

**Public reasoning:** Inspired by the impact of ChatGPT (released November 2022). Wanted to "build" at the frontier.

**Actual reasoning:** ChatGPT had changed everything. The organization he helped found was now the most important AI company in the world. He had spent 7 months doing education and open source. The pull of working on the actual frontier model (GPT-4 era) was irresistible. His later LinkedIn description says he "built a new team working on midtraining and synthetic data generation" -- a specific technical mandate, not a vague research role.

**Outcome:** He worked on midtraining and synthetic data generation for approximately one year. He was reportedly "instrumental in creating and polishing GPT-4." He then left again in February 2024, saying "nothing 'happened' and it's not a result of any particular event, issue or drama."

**Consistency:** His departure from Tesla was about education and open source. His return to OpenAI was about the frontier. The pattern: he oscillates between teaching and building, with each informing the other.

**Sources:**
- https://electrek.co/2023/02/08/tesla-former-head-ai-joins-elon-musk-founded-openai/
- https://techcrunch.com/2024/02/13/andrej-karpathy-is-leaving-openai-again-but-he-says-there-was-no-drama/
- https://karpathy.ai/ ("I came back to OpenAI where I built a new team working on midtraining and synthetic data generation.")

---

### Decision 8: Response to OpenAI Board Drama (November 2023)

**What:** When Sam Altman was fired by the OpenAI board on November 17, 2023, Karpathy posted on November 19: "I like and respect Sam and I think so does the majority of OpenAI. The board had a chance to explain their drastic actions and they did not take it, so there is nothing to go on except exactly what it looks like."

**What this reveals:** He did NOT sign the employee petition (505 of ~700 employees did). He did NOT post heart emojis. He did NOT threaten to quit. His response was measured, respectful, and slightly detached. He acknowledged the lack of information and refused to speculate.

**Inconsistency or consistency?** He was an OpenAI employee at the time, yet his response was closer to an outside observer than a partisan. He publicly stated respect for Altman but didn't join the revolt. This is consistent with his pattern of maintaining relationships with all sides without fully committing to any faction. He left OpenAI three months later, citing no drama.

**Relevance to AI instruction design:** His response mirrors his approach to debugging AI systems: "I don't have enough information to diagnose the problem, so I'll say exactly what I observe and no more." He doesn't speculate beyond the data.

**Sources:**
- https://www.aol.com/heart-emojis-confusion-wave-support-153900086.html (Karpathy quote)
- https://matthewharris.substack.com/p/the-rapid-unscheduled-disassembly (context of the quote)
- https://newsletter.pragmaticengineer.com/p/five-days-of-chaos-at-openai-and (full timeline)

---

### Decision 9: Second Departure from OpenAI (February 2024)

**What:** Left OpenAI after approximately one year, announcing on X: "Hi everyone yes, I left OpenAI yesterday. First of all nothing 'happened' and it's not a result of any particular event, issue or drama (but please keep the conspiracy theories coming as they are highly entertaining :))."

**Public reasoning:** "My immediate plan is to work on my personal projects and see what happens. Those of you who've followed me for a while may have a sense of what that might look like."

**Actual reasoning (inferred from timing and later actions):** He left exactly when llm.c was about to become his main project (released April 2024). He left knowing he wanted to start Eureka Labs (announced July 2024). The "personal projects" were llm.c, minbpe, and the groundwork for Eureka Labs. He had done his tour at the frontier (midtraining, synthetic data for GPT-4) and wanted to return to education and independent work.

**Outcome:** He released minbpe (February 2024), llama2.c (July 2023 -- actually before the second departure, showing the education itch was already strong), llm.c (April 2024), founded Eureka Labs (July 2024). The productivity burst after leaving OpenAI was extraordinary.

**Pattern note:** Every departure follows the same template: (1) no drama, (2) praise for the team, (3) vague next steps, (4) a burst of personal projects that were clearly planned in advance. He knows where he's going before he announces he's leaving.

**Post-hoc revision:** None. He has not revised his account of this departure.

**Sources:**
- https://techcrunch.com/2024/02/13/andrej-karpathy-is-leaving-openai-again-but-he-says-there-was-no-drama/
- https://venturebeat.com/ai/andrej-karpathy-confirms-departure-again-from-openai/

---

### Decision 10: Founding Eureka Labs (July 2024)

**What:** Announced Eureka Labs, "a new kind of school that is AI native." The concept: human teachers design course materials, AI teaching assistants guide students through them at scale.

**Public reasoning:** "Eureka Labs is the culmination of my passion in both AI and education over ~2 decades. My interest in education took me from YouTube tutorials on Rubik's cubes to starting CS231n at Stanford, to my more recent Zero-to-Hero AI series. My work in AI spanned academic research at Stanford, real-world products at Tesla, and AGI research at OpenAI. All of my work combining the two so far has only been part time, as side quests to my 'real job', so I am quite excited to dive in and build something great, professionally and full time."

**First product:** LLM101n -- an undergraduate-level course teaching students to build their own AI (a "Storyteller AI" LLM). Course materials on GitHub, with planned digital and physical cohorts.

**Why this decision matters for AI instruction design:** Eureka Labs is Karpathy's thesis about how AI should be instructed, applied to education. The core idea is "teacher + AI symbiosis": the human designs the curriculum (the "system prompt"), the AI teaching assistant handles the 1-on-1 delivery (the "inference"). He's literally building a product that instructs an AI to instruct humans. The recursion is the point.

**Outcome:** Still early. Eureka Labs appears to be self-funded (LLC filed in Delaware, signed by Karpathy alone). The LLM101n course materials are on GitHub. He announced he was building publicly. As of 2026, the company's trajectory is still forming -- he joined Anthropic in May 2026 while saying he "remains deeply passionate about education and plans to resume my work on it in time."

**Post-hoc revision:** The decision to join Anthropic in 2026 while Eureka Labs is still young could be seen as a revision of the "full time" commitment, though he frames it as a pause rather than a pivot.

**Sources:**
- https://techcrunch.com/2024/07/16/after-tesla-and-openai-andrej-karpathys-startup-aims-to-apply-ai-assistants-to-education/
- https://venturebeat.com/ai/ex-openai-and-tesla-engineer-andrej-karpathy-announces-ai-native-school-eureka-labs/
- https://www.theverge.com/2024/7/16/24199970/andrej-karpathys-next-venture-a-new-kind-of-school-that-is-ai-native

---

### Decision 11: Releasing llm.c (April 2024)

**What:** Released llm.c, an implementation of LLM training in "simple, pure C/CUDA with no need for 245MB of PyTorch or 107MB of cPython."

**Public reasoning:** "Ultimately my interest in llm.c is to have a nice, clean, minimal, super dependency-light repo in direct C/CUDA implementation, which I find aesthetically pleasing. And on top of that, educational."

**Design constraints (from README):** "If there is a PR that e.g. improves performance by 2% but it 'costs' 500 lines of complex C code, and maybe an exotic 3rd party dependency, I may reject the PR because the complexity is not worth it." Root folder is held to higher simplicity standards than dev/ folder.

**Why this matters for AI instruction design:** llm.c is the most extreme example of his "minimum viable abstraction" philosophy. The constraints he imposes on PR acceptance are essentially system prompt design principles: (1) every line must earn its complexity, (2) the default experience must be simple, (3) complexity lives in designated areas, (4) the maintainer (or prompt author) must be able to understand the whole thing at once.

**Sources:**
- https://github.com/karpathy/llm.c
- https://news.ycombinator.com/item?id=40502090 (Karpathy's HN comments on design philosophy)

---

### Decision 12: Coining "Vibe Coding" (February 2025)

**What:** Posted on X: "There's a new kind of coding I call 'vibe coding', where you fully give in to the vibes, embrace exponentials, and forget that the code even exists." He described accepting all diffs without reading them, copy-pasting error messages with no comment, and building projects where "the code grows beyond my usual comprehension."

**Public reasoning:** He framed it as "not too bad for throwaway weekend projects, but still quite amusing." A shower thought, not a manifesto.

**What happened:** The term went viral. Within weeks it had a Wikipedia page. By year-end, 25% of YC's Winter 2025 batch had codebases that were 95% AI-generated. Collins Dictionary named it Word of the Year.

**His evolution on the term:** By April 2026 (Sequoia AI Ascent talk), he had refined the concept into "agentic engineering": "Vibe coding is about raising the floor for everyone in terms of what they can do in software. Agentic engineering is about preserving the quality bar of what existed before in professional software." He emphasized that agentic engineering is "a craft with both art and science, requiring professional skills."

**Relevance to AI instruction design:** Vibe coding -> agentic engineering is the live evolution of his thinking about human-AI collaboration. The shift from "forget the code exists" to "you're still responsible, just faster" mirrors the shift from naive prompt-and-pray to structured context engineering. His key insight: "I just don't want to do anything. What is the thing I should copy paste to my agent?" -- he wants documentation written for agents, not humans.

**Post-hoc revision:** Substantial. He coined a term for a casual practice, watched it become a movement, then spent the next year refining it into something more disciplined. The original vibe coding post is almost the opposite of his actual engineering practice.

**Inconsistency:** He advocates vibe coding for throwaway projects but his actual work (nanoGPT, llm.c) is the most meticulous, hand-crafted code in AI. The tension is real and he acknowledges it: vibe coding is for when you don't care about quality; his actual standard is extreme care.

**Sources:**
- https://www.youtube.com/watch?v=96jN2OCOfLs (Sequoia AI Ascent 2026 talk)
- https://aihola.com/article/karpathy-2025-llm-year-review (comprehensive 2025 retrospective)
- https://www.devclass.com/ai-ml/2025/03/26/the-paradox-of-vibe-coding-it-works-best-for-those-who-do-not-need-it/1623968

---

### Decision 13: Joining Anthropic (May 2026)

**What:** Announced he joined Anthropic's pretraining team, under Nick Joseph, to build a new team focused on using Claude to accelerate pretraining research.

**Public reasoning:** "I think the next few years at the frontier of LLMs will be especially formative. I am very excited to join the team here and get back to R&D. I remain deeply passionate about education and plan to resume my work on it in time."

**What this reveals:** He chose pretraining (the most fundamental, least product-facing part of LLM development) over applied work. He chose Anthropic over OpenAI (his founding organization) at a time when OpenAI was losing senior talent. He explicitly paused Eureka Labs to do this.

**Significance for AI instruction design:** Pretraining is where the model's "default behavior" is established -- the analog of a system prompt at the most fundamental level. Karpathy is now in a position to shape how a frontier model behaves before any prompt is ever written.

**Sources:**
- https://techcrunch.com/2026/05/19/openai-co-founder-andrej-karpathy-joins-anthropics-pre-training-team/
- https://www.cnbc.com/2026/05/19/anthropic-hires-openai-cofounder-andrej-karpathy-former-tesla-ai-lead.html

---

## B) The Pattern of Decisions

### When he ships, does he ship MVPs or polished products?

He ships MVPs that are so clean they feel polished. nanoGPT's ~600 lines, micrograd's ~150 lines, minbpe's clean 4-file structure -- these are MVPs by any definition (minimal feature sets, narrow scope). But they are so carefully constructed that they feel like finished products. The polish is in the minimalism, not in feature completeness.

His design pattern: (1) identify the minimum viable unit of a complex system, (2) implement it with zero unnecessary abstraction, (3) structure the repo so each file's purpose is immediately clear from the README, (4) ensure the git history is a teaching tool.

This is directly relevant to system prompt design: a good system prompt is an MVP of a behavioral specification. It should be minimal, clean, and have each section's purpose be immediately clear.

### When he leaves, does he leave cleanly or burn bridges?

Always clean. Every departure follows the same pattern:
1. Announce on X/Twitter
2. Praise the team and institution
3. Say nothing negative
4. Cite personal passions as the reason
5. Maintain relationships (Musk says "Andrej will always be welcome at Tesla"; he says he loves Tesla, Elon, and the team)

He has never publicly criticized an employer, even when the circumstances (the OpenAI board drama) would have given him ample justification. This is partly temperament and partly strategy: he values long-term relationships over short-term catharsis.

### How does he choose between "do the research" vs "teach the research" vs "build the product"?

He oscillates in a roughly 2-year cycle:
- 2015-2017: Research (OpenAI founding)
- 2017-2022: Build (Tesla Autopilot)
- 2022-2023: Teach (Zero to Hero, nanoGPT)
- 2023-2024: Research (OpenAI midtraining)
- 2024-2025: Teach/Build (Eureka Labs, llm.c)
- 2026: Research (Anthropic pretraining)

The oscillation is not random. Each phase informs the next: Tesla gave him the real-world experience that made Zero to Hero compelling. Teaching gave him the clarity to identify what was missing (midtraining, synthetic data). Working at the frontier gave him the insight to design Eureka Labs.

His revealed preference: teaching is his default state. He returns to it whenever he's not actively pulled to the frontier by a specific opportunity. The two "build" phases (Tesla, Eureka Labs) are the exceptions; teaching is the rule.

---

## C) Inconsistencies

### 1. Vibe Coding vs. Actual Practice

**The tension:** He coined "vibe coding" to describe a practice of blindly accepting AI output without reading it. His actual code (nanoGPT, llm.c, microgpt) is the most meticulously hand-crafted, human-understood code in the AI ecosystem. He rejects PRs that add 500 lines of complexity for 2% speedup.

**Has he reconciled it?** Yes, by distinguishing "raising the floor" (vibe coding) from "preserving the quality bar" (agentic engineering). But the original vibe coding post remains his most viral contribution, and it describes a practice he doesn't actually follow.

### 2. "No Drama" Departures from Dramatic Situations

**The tension:** He left OpenAI three months after the most dramatic board coup in tech history, claiming "nothing happened." He was an employee during the event. His measured response (not signing the petition, not joining the revolt) suggests either (a) he genuinely had no strong feelings or (b) he was already planning to leave and didn't want to burn bridges on the way out.

**Has he reconciled it?** He has never publicly discussed the board drama in detail beyond his November 19 tweet. The silence itself is the resolution: he chose not to engage.

### 3. Education Company -> Frontier Lab

**The tension:** In July 2024 he announced Eureka Labs as his "full time" commitment to education. In May 2026 he joined Anthropic, saying education would resume "in time." For someone who frames everything as consistent with his passions, pausing a company after two years to go back to R&D is a meaningful shift.

**Has he reconciled it?** Partially. He says "the next few years at the frontier of LLMs will be especially formative" -- implying the education work needs better frontier models to be truly effective. This is plausible but also convenient.

### 4. Software 2.0 Prophet -> Software 3.0 Advocate

**The tension:** In 2017, he argued that neural network weights would replace human-written code. By 2025, he's arguing that English prompts (Software 3.0) are the new programming language. These aren't contradictory -- he frames them as layers of the same stack -- but the emphasis shift is real. Software 2.0 was about datasets replacing code. Software 3.0 is about prompts replacing code. The "code" being replaced is different in each case, but the rhetorical structure is identical.

**Has he reconciled it?** Yes, explicitly. Software 1.0 (explicit code), 2.0 (weights), and 3.0 (prompts) coexist. You choose the right paradigm for each problem. The framework is additive.

---

## D) The "Instructing AI" Decisions Specifically

### How does he structure system prompts in his own projects?

He hasn't publicly shared system prompts for specific products. But his GitHub READMEs are the closest analog, and they reveal a clear structure:
1. **One-line description** of what the thing does (e.g., "The simplest, fastest repository for training/finetuning medium-sized GPTs")
2. **Numbered file listing** explaining each component's role
3. **Quick-start example** showing the minimal usage
4. **Explicit design constraints** (what the project is NOT)
5. **Scope boundaries** (e.g., llm.c: "I'd like this repo to only maintain C and CUDA code")

This maps directly to good system prompt design: (1) identity, (2) tool/function descriptions, (3) example usage, (4) guardrails, (5) scope.

### What's his public position on how AI agents should be instructed?

From his latent.space interview (2025): "Pretraining is for knowledge. Finetuning (SL/RL) is for habitual behavior. [But] a lot of human learning feels more like a change in system prompt... It feels more like taking notes for yourself... LLMs are quite literally like the guy in Memento, except we haven't given them their scratchpad yet."

He has argued for a third paradigm: "system prompt learning," where the model learns to edit its own instructions based on experience. This is distinct from both pretraining (changing weights) and finetuning (changing habitual behavior). It's about changing explicit instructions -- the closest thing to a human "realizing something and writing it down."

### Any demos of him debugging AI agent behavior in public?

His entire YouTube channel is a demo of debugging AI behavior, but from the training side. The Zero to Hero series shows him debugging neural networks by examining loss curves, gradient magnitudes, and activation statistics. The Tesla data engine presentations show him debugging deployed models by mining the fleet for failure cases. These are the Software 2.0 debugging patterns.

For Software 3.0 (LLM prompting), his vibe coding discourse is the closest thing to a public debugging demo. He describes copying error messages into the prompt without comment and watching the model fix itself. He describes asking for "random changes until [the bug] goes away." These are anti-patterns that he later refined into "agentic engineering."

### His GitHub READMEs as "case studies" in how he documents for both humans and AIs

From the aiskill.market analysis: "Karpathy's public code is pedagogically engineered to be fully understandable by a single person in a single sitting. That design philosophy -- minimum surface area, maximum transparency, no abstractions unless the abstraction earns its complexity -- shows up again in the karpathy-guidelines skill."

Key documentation patterns across his repos:
- **The git history IS the documentation.** build-nanoGPT's commits are kept "step by step and clean so that one can easily walk through the git commit history to see it built slowly."
- **The README is the instruction manual.** Each file is listed with its purpose.
- **Constraints are explicit.** "I'd like this repo to only maintain C and CUDA code" (llm.c). "This repo is not a complex framework with a 1000 knobs" (llama2.c).
- **Anti-goals are stated.** "This repo still cares about efficiency, but not at the cost of simplicity, readability or portability" (llama2.c).

These are exactly the principles that make a system prompt effective: explicit identity, explicit scope, explicit anti-goals, and structured for a single-pass read.

---

## Summary

**Three decisions that most reveal his values:**

1. **Leaving Tesla without a plan (2022):** He walked away from one of the most powerful positions in AI -- reporting directly to Musk, leading the Autopilot vision team -- with "no concrete plans." This reveals that autonomy and the ability to follow his own intellectual curiosity matter more than power or money.

2. **Writing Software 2.0 (2017):** This was not a career decision but an intellectual one. He chose to frame neural networks as a new programming paradigm at a time when most people saw them as "just another classifier." This reveals his commitment to clear mental models over trend-following. The essay predicted a decade of AI development.

3. **Founding Eureka Labs instead of joining any existing company (2024):** After leaving OpenAI for the second time, every major AI lab would have hired him. He chose to start an education company instead. This reveals that teaching is not his side quest -- it's his core mission, and everything else (Tesla, OpenAI, Anthropic) serves it eventually.

**Two cases of clear evolution:**

1. **Vibe coding -> Agentic engineering (2025-2026):** He coined a term for casual AI-assisted coding, watched it become a movement, and then refined it into a disciplined practice. The evolution shows his willingness to engage with messy reality (people are actually vibe coding!) and then impose structure on it.

2. **Software 2.0 -> Software 3.0 (2017-2025):** He extended his neural-networks-as-new-software thesis to include LLM prompts as a new programming language. The framework is additive, not corrective, showing that his original insight was deep enough to accommodate a paradigm shift he didn't predict.

**One contradiction he has not reconciled:**

He says education is his deepest passion and that Eureka Labs is the culmination of two decades of work. He also keeps leaving education to work at frontier AI labs (OpenAI twice, now Anthropic). The stated reason -- that frontier model capabilities need to advance before education can be truly transformed -- is plausible but also conveniently allows him to oscillate forever between teaching and building without fully committing to either. As of 2026, Eureka Labs appears to be on hold while he does pretraining at Anthropic. He has not resolved whether he is fundamentally a teacher who builds, or a builder who teaches.
