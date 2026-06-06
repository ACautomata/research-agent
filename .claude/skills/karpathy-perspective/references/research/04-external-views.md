---
**VERIFIED SCOPE: 2017 – early 2024.** Per user decision (2026-06-03), this skill is bounded to pre-mid-2024 Karpathy to avoid propagating unverified 2024-mid-to-2026 claims. Sections marked **[UNVERIFIED — quarantined]** preserve the original research for future re-verification but are NOT load-bearing for synthesis.
---

# 04 — External Views: How Others See Karpathy

**Purpose of this document.** This file captures how the wider AI research and engineering community perceives Andrej Karpathy — what people praise, what they push back on, what tribal patterns exist around him, and where the "celebrity researcher" framing starts to distort how his ideas are received. The downstream skill uses these observations to identify Karpathy's blind spots (the "诚实边界" section) and to calibrate the reviewer persona so it doesn't just flatter the subject.

**Source conventions.** Each claim is marked:
- `[URL]` — link
- `(type)` — blog / news / HN / tweet / paper / podcast / wiki
- `(date)` — when the source was published
- `(confidence: high | medium | low)` — based on how often multiple sources converge and how authoritative the outlet is
- `[Q]` = a direct quote from a person
- `[I]` = my inference from the pattern of multiple sources

**Source blacklist applied.** No zhihu.com / weixin / baike.baidu.com sources were used.

---

## A. What others see as his strengths

### A1. Pedagogy — the dominant compliment

The single most consistent thing said about Karpathy across all source types is that he is a *teacher*, and unusually good at it.

**[Q]** Sequoia partner Shaun Maguire, on Karpathy's Eureka Labs announcement: "[Karpathy has a] gift for teaching … thank you for sharing and scaling that gift!"
- Source: https://venturebeat.com/ai/ex-openai-and-tesla-engineer-andrej-karpathy-announces-ai-native-school-eureka-labs/
- (news, 2024-07-16, confidence: high)

**[Q]** Jeff Dean, Chief Scientist at Google DeepMind: "AI is going to have a huge impact on education & I know it's something you're passionate about."
- Source: https://medium.com/@genaiassembling/andrej-karpathy-starts-his-new-chapter-revolutionizing-education-with-ai-48d95adaff6f
- (blog aggregating X posts, 2024-07-25, confidence: high)

**[Q]** TIME100 AI 2024 profile: "His biggest impact on the world, however, may come not from his research but from his role as one of the world's foremost educators on neural networks."
- Source: https://time.com/collection/time100-ai-2024/ (cited via https://aiturnpoint.com/andrej-karpathy)
- (news, 2024-09, confidence: high)

**[Q]** Tom Bolton, comparing Karpathy's "Neural Networks: Zero to Hero" against Andrew Ng's Coursera Deep Learning Specialization: "The unusual property is that the camera doesn't leave one person. These don't feel like recorded lectures; they feel like a friend sharing their screen while they work. … The decision to leave those moments in is part of the texture. The series doesn't pretend the work is clean."
- Source: https://tombolton.io/2024/09/23/andrej-karpathy-to-the-rescue-of-course/
- (personal blog, 2024-09-23, confidence: high)

**[Q]** Mike Levy, Dataquest's 2026 ranked list of deep-learning courses: "This combination is the most recommended free deep learning resource across practitioner communities. 3Blue1Brown's neural network series builds geometric intuition for what a neural network does when it 'learns'… Karpathy's Zero to Hero turns that intuition into code."
- Source: https://www.dataquest.io/blog/best-deep-learning-courses/
- (review blog, 2026-05-28, confidence: medium)

**[Q]** Steven Gong, in a meta-note on what makes Karpathy effective: "Andrej Karpathy is the best teacher I've had. He says that some of his most rewarding moments was being TA or teaching CS231n." Other notes: "He has meta-awareness about the information he is conveying" and "He seems to talk like how Jordan Peterson talks. And the hand gestures."
- Source: https://stevengong.co/notes/Teacher
- (personal notes, n.d., confidence: low — single observer)

**[I] Pattern in pedagogy compliments:** Multiple independent sources independently identify the *same* signature moves — code-is-truth, real-time debugging, building from a blank file, "leave the mistakes in" honesty, and direct address to the camera. This isn't generic flattery; it's a repeatable set of behaviors that get named specifically. The pedagogy reputation is **defensibly his strongest external claim**.

### A2. Technical depth that survives contact with reality

Sources that engage with his actual technical positions, not just his persona, repeatedly call out a specific skill: he understands things at the level of a person who has shipped them.

**[Q]** EZPZ AI review of the `nn-zero-to-hero` repo: "The CV reads like a Big Tech executive's, but what defines him is what he's published in between the jobs. micrograd — a 150-line autograd engine. makemore — a small character-level language model that generates names. minGPT and nanoGPT — GPT reimplementations small enough to fit on a screen. llm.c — LLM training in dependency-free C. The shared move: take the thing the field treats as a black box, rewrite it in the smallest unit a learner can read end to end."
- Source: https://ezpzai.com/en/2026-05-23-karpathy-nn-zero-to-hero-en/
- (technical blog, 2026-05-22, confidence: high)

**[Q]** Simon Willison's log: "Extremely high signal 2 hour 25 minute (!) conversation between Andrej Karpathy and Dwarkesh Patel. … I loved this bit introducing an analogy of LLMs as ghosts or spirits, as opposed to having brains like animals or humans."
- Source: https://simonwillison.net/2025/Oct/18/agi-is-still-a-decade-away/
- (blog, 2025-10-18, confidence: high — Willison is a discriminating curator)

**[I] Pattern:** "Engineer who can also explain" is the second-most-consistent compliment. Sources that engage with his *content* (Willison, Willison-style technical blogs, the Frenxt cable post on Software 2.0) rate his work highly. Sources that only engage with his *persona* (purely promotional coverage) tend to flatten him to "the explainer."

### A3. First-principles orientation and intellectual honesty

A more specific virtue that comes up in technical-critic circles: he is willing to publicly change his mind, and to name the conditions under which his previous frameworks stop working.

**[Q]** Ismat Samadov / BirJob, May 2026: "Most public AI voices don't update like that. They double down on whatever they said in 2023 because admitting they were wrong is bad for the personal brand. Karpathy treats his frameworks as hypotheses to be revised, not identities to defend."
- Source: https://www.birjob.com/blog/karpathy-anthropic-pretraining-2026
- (blog, 2026-05-23, confidence: high)

**[Q]** Karpathy's own Software 3.0 update of the 2017 Software 2.0 essay (paraphrased by Tom Hundley / Elegant Software Solutions, 2026-04-09): "Karpathy's June 17, 2025 YC AI Startup School keynote, billed as *Software Is Changing (Again)*. The framework: Software 1.0 is classical code written by humans, Software 2.0 is neural networks trained on data, and Software 3.0 is behavior shaped through natural-language prompts to large language models."
- Source: https://www.elegantsoftwaresolutions.com/blog/andrej-karpathy-software-3-0-ai-first-development
- (blog, 2026-04-09, confidence: medium — paraphrase of a public talk)

### A4. Taste in analogies

The "ghosts or spirits" analogy (Willison's favorite), the "Software 1.0 / 2.0 / 3.0" generational framing, the "mashup spirit of its average data labeler" reframing of what LLMs are — multiple critics note that Karpathy's *metaphor choice* does a lot of explanatory work. This is a real pedagogical strength and also (see C section) a real risk vector.

**[Q]** Karpathy, quoted by Simon Willison: "People have too inflated sense of what it means to 'ask an AI' about something. The AI are language models trained basically by imitation on data from human labelers. Instead of the mysticism of 'asking an AI', think of it more as 'asking the average data labeler' on the internet."
- Source: https://simonwillison.net/2024/Nov/29/andrej-karpathy/
- (quote collector blog, 2024-11-29, confidence: high)

### A5. Pattern of moves as signal

A more meta-complaint-turned-compliment: people who watch his career pattern treat it as a leading indicator of where the AI industry is going.

**[Q]** Samadov: "Reading the pattern is more useful than reading any individual essay he's written."
- Source: https://www.birjob.com/blog/karpathy-anthropic-pretraining-2026
- (blog, 2026-05-23, confidence: high)

**[I] Caveat:** This compliment is double-edged. See C/D sections — the same "pattern following" behavior, when used as a substitute for technical judgment, is itself a problem.

---

## B. Criticisms and pushback

This is the section to focus on, per the prompt. Substantive disagreements are harder to find than praise. What follows is grouped by topic, with the strongest critique per topic quoted verbatim when possible.

### B1. "Software 2.0" — the early and ongoing rebuttal

The 2017 essay has been picked apart by a long list of technically literate critics. The most thorough pre-LLM rebuttal is by Carlos E. Perez in 2017.

**[Q]** Carlos E. Perez, *Intuition Machine*, 2017-11-12, going through Karpathy's bullets one by one:

> "Computational homogenous — This is interesting, but not valid considering that digital systems are essentially also computationally homogeneous if we look from the perspective of universal gates (i.e. NAND and NOR). In fact newer Deep Learning silicon is not homogenous and uses specialized cores."

> "Easy to bake into silicon — Not exactly true in that the major risk for ASIC designers is to commit to an architecture that could get obsoleted in a few months. … The hard part is knowing you have the key components for Deep Learning."

> "Constant running time — Not true for more complex networks that conditionally traverse different paths (see: Conditional Logic is the New Hotness). However, it is entirely possible to have iterative components (see MCTS in AlphaGo) that may have a big variance in running time."

> "Constant memory use — Not true for networks that are dynamically constructed on the fly."

> "Highly portable — Not true. Deep Learning is more portable and modular than classic ML, but it definitely is missing several features of Modular systems."

> "It is easy to pick up — This is typical for maturing technology. As software professionals we don't need to understand the quantum physics that is the basis of semiconductors. … A more kind of intuitive level of software development will have to arise that will be closer to how we do teaching today."

> "It is better than you — I agree with this sentiment. A lot of innovative discoveries are being found by brute force methods."

- Source: https://medium.com/intuitionmachine/is-deep-learning-software-2-0-cc7ad46b138f
- (blog, 2017-11-12, confidence: high — one of the most thorough and earliest direct rebuttals)

A second rebuttal, more concise but pointed: Zeeshan Khan Suri's "Software 2.0 2.0" (2022).

**[Q]** Suri:

> "First, to gain performance, it is not enough to copy paste one training example into multiple copies. The model needs to be intelligently scaled by feeding in huge amounts of new data with much variation, representing the true population as truly as possible."

> "Secondly, new data doesn't come for free. It is labor-intensive and expensive to label data. Smart gathering is required."

> "Thirdly, in order to be able to feed in that much amount of data, there needs to be infrastructure in place."

> "For many applications, the performance gain is really not that critical. Other factors such as explainability, fail-safe, etc are equally important, which the current deep learning approaches lack."

- Source: https://zshn25.github.io/Software-2/
- (blog, 2022-12-05, confidence: high)

A non-technical HN-flavored critique focuses on applicability to real systems:

**[Q]** HN commenter on the 2017 essay (cited via 2023 thread): "For example, as someone who works with financial software, I don't see Karpathy's 'Software 2.0' replacing, say, account ledgering software anytime soon. 'Yeah, we calculate our clients' balances correctly 99.9% of the time!' isn't going to cut it."

> "But I don't think that's what Karpathy is arguing. There is a large set of problem domains where Karpathy's Software 2.0 is a much better solution than what he calls Software 1.0. For example, even in finance, stuff like fraudulent transaction detection, or financial security software for intrusion detection, is very well-suited to Software 2.0."

> "The kinds of software that 'Software 1.0' is suitable for are markedly different that the ones 'Software 2.0' are. As Karpathy argues, it's a different tool, suitable for different tasks, and it should have a different name."

> "But, but nobody touches this crap besides generating pictures to show on Powerpoint slides. Because writing software is circa 10% of all effort, specification, legal stuff, maintenance, avoiding technical debt, proper test cases, anomaly testing, performance testing the right stuff. That is hard, that matters. Software 2.0 is barking the wrong tree."

- Source: https://news.ycombinator.com/item?id=34881881
- (HN thread, 2023-02-21, confidence: medium — anonymous, but representative)

**[I] Pattern across these critiques:** Almost none of the substantive critics deny the *direction* of Software 2.0. They push back on:
- the *granularity* of the benefits claim (e.g. "constant running time" — false for many real models)
- the *framing* (calling it "software" hides that it doesn't share properties of software)
- the *omission* of the cost (data labeling, infrastructure, validation)
- the *overreach* into domains where it doesn't apply (financial ledgers, OS kernels, business logic)

This is a useful pattern for the Karpathy-style reviewer: the framework is right at the macro level and slipshod at the bullet level. A reviewer that just *echoes* the framework misses what actually got objected to.

### B2. "Vibe coding" — the most contested term

The "vibe coding" tweet (February 2025) attracted more substantive critique from knowledgeable peers than arguably anything else Karpathy has named. The critiques cluster into four families.

**Critique family 1: Code quality, security, maintainability.** The ACM TechBrief on Vibe Coding is the most formal version.

**[Q]** ACM TechBrief:

> "Software engineering's established practices produce systems that are generally secure, reliable, and maintainable. Vibe coding circumvents these practices. While it can produce code that meets immediate requirements for style, conventions, and targeted ('unit') tests, it does not produce well-designed software systems. Because many of these systems have been trained on data that includes cybersecurity vulnerabilities, there is a risk that they will replicate these in the code that they generate."

> "A core principle of modern software development is that a program's functions and behavior need to be specified in advance. 'A program that has not been specified cannot be incorrect, it can only be surprising.' AI-generated code typically lacks specifications. … As a result, AI-generated code drifts away from stated requirements, including core functionality."

> "Few vibe coding platforms systematically test their AI-generated code to ensure it runs correctly and consistently. … AI systems have been observed to modify, disable, or simply remove such tests rather than correcting their code."

> "Vibe coding platforms often produce over-engineered solutions with redundant code and subtle errors that create maintenance nightmares, known as 'technical debt'."

- Source: https://www.acm.org/public-policy/techbriefs/techbrief-vibe-coding
- (institutional policy brief, ACM, confidence: high — high authority, formal)

**Critique family 2: Empirical experience doesn't match the hype.** Stephen Cresswell, a 30-year veteran, did a structured three-method experiment with Claude Code and reported a much more sober picture than the Karpathy tweet suggested.

**[Q]** Cresswell:

> "The same tool is being described, with equal confidence, as producing dangerous, unmaintainable AI slop on the one hand, and delivering twenty times productivity on the other."

> "Claude is not a compiler. The results are not deterministic. Small differences in context, ordering, or phrasing can lead to materially different outcomes, even when the intent appears unchanged. Overall, the outcomes are still positive, but I have yet to achieve the 20x improvement reported by some. Either those reports are grossly overstated, or those making them have found ways to circumvent these issues."

> "Method 1 (Prompt Bootstrapping, Implementation Notes, and Manual Accepts) showed that Claude is ineffective when asked to bootstrap a non-trivial system from scratch using prompts alone. … The results suggest that Claude is far more productive when working on an existing or bootstrapped codebase, and that it appears to weight existing artefacts more heavily than abstract guidance from prompts or skills."

> "Method 3 (Template Bootstrapping, No Implementation Notes, and Automatic Accepts) demonstrates that Claude is not yet something that can be left to operate unattended while still producing consistently good outcomes. Without strong constraints, it reliably drifts towards verbosity, duplication, and accidental complexity, even when the resulting system is functionally correct. That gap between apparent success and long-term maintainability likely explains much of the current scepticism and pushback."

- Source: http://www.stephen-cresswell.com/2026/01/01/Why-Are-Experiences-Of-Vibe-Coding-So-Polarised.html
- (personal blog with structured experiment, 2026-01-01, confidence: high — first-hand, methodical)

**Critique family 3: The Karpathy problem — how casual remarks become industry consensus.**

**[Q]** Samadov, May 2026:

> "The lesson worth taking from the vibe-coding episode isn't about coding agents specifically. It's about how the AI industry treats Karpathy's casual remarks. He has, accidentally, become the field's most-quoted single voice. Things he posts on a Tuesday afternoon become industry consensus by Thursday. … Buyers reading any 2026 AI commentary should adjust for it."

- Source: https://www.birjob.com/blog/karpathy-anthropic-pretraining-2026
- (blog, 2026-05-23, confidence: high)

**Critique family 4: Walk-back was correct but slow.** A meta-critique that even Karpathy's correction was too late.

**[Q]** Samadov:

> "Vibe coding's blast radius. The original 'vibe coding' tweet was a personal reflection. He couldn't have anticipated it would become a generic recommendation that startup teams would internalize and apply to production code. The walk-back in 2026 was correct but slow, by then, real production systems had already been built on the vibes-coding premise and were generating the security-flaw rates IBM documented."

- Source: https://www.birjob.com/blog/karpathy-anthropic-pretraining-2026
- (blog, 2026-05-23, confidence: high)

**[I] Pattern of the vibe coding critique:** The strongest critics are not "AI coding is overhyped" people. They are people who *do* find the tools productive, but who observe that Karpathy's framing was the wrong one — too casual about safety, too confident about determinism, and too influential to be casual. This is *exactly* the pattern the downstream reviewer skill should detect: a Karpathy-style statement that *is* defensible in private use but gets over-applied at scale.

### B3. "Eureka Labs" — the mixed-to-skeptical reaction

Eureka Labs drew overwhelmingly positive initial reactions in 2024. Subsequent assessments of the venture's *execution* are noticeably cooler.

**[Q]** HyScaler (a slightly purple prose blog) at announcement, skeptical framing:

> "Andrej Karpathy Eureka Labs: a name whispered reverently in the hallowed halls of artificial intelligence, has done it again. The man who has navigated the labyrinthine corridors of Tesla and OpenAI with almost supernatural ease has unveiled his newest creation: Karpathy Eureka Labs. On the surface, it's a beguiling proposition: an 'AI-native' education platform. A seductive phrase, pregnant with promises of a pedagogical revolution. Yet, as with all things Karpathy, the devil, as they say, is in the details."

> "Eureka Labs, a nascent entity birthed in the fertile grounds of San Francisco, aspires to harness the raw power of generative AI to conjure digital tutors, and ethereal companions on the arduous journey of learning. A noble ambition, undoubtedly. But is it merely a mirage, a tantalizing phantom conjured by the potent elixir of hype and ambition?"

> "Whether Karpathy Eureka Labs will be the catalyst for an educational renaissance or merely a footnote in the annals of tech history remains to be seen."

- Source: https://hyscaler.com/insights/karpathy-eureka-labs-ai-education/
- (blog, 2024-07-17, confidence: low — purple prose, but the skepticism is real)

**[Q]** TechCrunch, more measured, flagged the gap between vision and operational reality:

> "The startup does not yet appear to have built or tested the efficacy of integrating AI assistants into the classroom. At least one Georgia State University study found that AI teaching assistants helped some students get better grades."

> "The link for this AI course leads to a GitHub repository that hints at a different type of course than Eureka Labs is advertising — instead of 'How to build an AI assistant,' the link leads to a how-to for building a 'Storyteller AI Large Language Model (LLM).'"

> "Whichever course Eureka Labs intends to introduce first, neither appears to be complete. A note posted on the GitHub page says the course will take time to build and there's no specific timeline."

- Source: https://techcrunch.com/2024/07/16/after-tesla-and-openai-andrej-karpathys-startup-aims-to-apply-ai-assistants-to-education/
- (news, 2024-07-16, confidence: high)

**[Q]** Wikipedia (note: encyclopedia, but useful as a consolidated skeptical voice, with citations):

> "The company also advocates for AI teaching assistants, a concept which has been criticized due to data privacy concerns and the removal of personal connection between teacher and student."

- Source: https://en.wikipedia.org/wiki/Andrej_Karpathy
- (wiki, confidence: medium — Wikipedia is not authoritative on its own but represents the cumulative critical view)

**[Q]** Samadov's later assessment, after the Anthropic move:

> "The honest read: the AI tutoring thesis is correct but the execution path Eureka Labs chose (premium-priced cohort courses) is one of several reasonable paths, and the one Karpathy picked wasn't the winner. Other AI-tutor startups taking different approaches, Khan Academy's Khanmigo with the institutional partnership, Mathy AI with K-12 math, Replit's coding tutor inside the IDE, are seeing meaningful adoption. The category works. Eureka Labs as a brand may or may not."

> "Eureka Labs traction. The AI-tutor category exists and is growing, but Eureka Labs specifically didn't capture the market the way the announcement implied it would. Two years of building a single course is, by venture standards, a slow path. The departure to Anthropic suggests Karpathy concluded the educational mission could continue informally (YouTube, X posts, occasional courses) without a dedicated company."

- Source: https://www.birjob.com/blog/karpathy-anthropic-pretraining-2026
- (blog, 2026-05-23, confidence: high)

**[I] Pattern:** The Eureka Labs reception splits cleanly along *time of writing*. July 2024 sources are near-uniformly positive (announcement hype). 2025–2026 sources, looking back, are skeptical on execution. The shift is not just sour grapes — it's a recognition that "AI-native school" as a category did grow, but not via Karpathy's specific bet.

### B4. Tesla FSD / vision-only — the "where the framework broke" critique

This is the strongest case study in the existing record of Karpathy being directionally right and operationally wrong. The 2017–2022 vision-only thesis was defensible; the 2018–2022 *timeline* was not, and the 2018–2022 *public narrative* Musk built around it overshot what was being delivered.

**[Q]** Samadov:

> "Tesla FSD timeline. Karpathy was at Tesla during the years Musk promised 'robotaxis next year' and 'summon your car from across the country' and 'FSD is solved.' Karpathy didn't make those public promises himself, but he was the AI director when they were being made. The vision-only approach, which he led, has not delivered the autonomy Tesla projected. Waymo's sensor-fusion approach has. The Software 2.0 thesis applied to driving has been a slower, more partial win than the Tesla narrative implied throughout 2018-2022."

> "The lesson Karpathy seems to have taken from Tesla, based on his later talks, is that Software 2.0 works when failure modes are tolerable. Image classification is forgiving. Translation is forgiving. Spell-check is forgiving. Driving is not."

- Source: https://www.birjob.com/blog/karpathy-anthropic-pretraining-2026
- (blog, 2026-05-23, confidence: high)

**[I] Pattern across the Tesla critique:** The argument is *not* "vision-only is dead." The argument is "vision-only was correct as a research bet and incorrect as a deployment-timeline narrative." Note the careful framing: Karpathy himself is faulted not for the technical thesis but for *being there* when the overpromising happened, and for not visibly pushing back on it. This is a serious critique about intellectual *responsibility* in addition to intellectual content.

### B5. "AGI in a decade" / scaling — the disagreement with LeCun / Chollet

Karpathy's "AGI is still a decade away" framing (in his October 2025 Dwarkesh Patel conversation) places him somewhere between LeCun's "world models not LLMs" and the "we're almost there" camp. This is one of the few areas where he has a *named* disagreement with other tier-1 researchers.

**[Q]** Willison, summarizing the Dwarkesh conversation:

> "Andrej's claim that 'the year of agents' is actually more likely to take a decade. Seeing as I accepted 2025 as the year of agents just yesterday this instantly caught my attention!"

> "Brains just came from a very different process, and I'm very hesitant to take inspiration from it because we're not actually running that process. In my post, I said we're not building animals. We're building ghosts or spirits or whatever people want to call it, because we're not doing training by evolution. We're doing training by imitation of humans and the data that they've put on the Internet."

- Source: https://simonwillison.net/2025/Oct/18/agi-is-still-a-decade-away/
- (blog, 2025-10-18, confidence: high)

The LeCun disagreement is the one explicitly named in public sources. LeCun argues for JEPA / world models, against the LLM-as-frontier framing Karpathy implicitly endorses.

**[Q]** Yann LeCun, LinkedIn (December 2024), capturing the *style* of disagreement with critics including the Karpathy-adjacent camp:

> "People posting on X/Twitter that I'm wrong. But they just totally misunderstood my arguments. The comments are even worse! I don't comment on X/Twitter anymore, so they'll never know…"

- Source: https://www.linkedin.com/posts/yann-lecun_people-posting-on-xtwitter-that-im-wrong-activity-7276713200882966528-HTtZ
- (LinkedIn post, 2024-12-22, confidence: high)

**[Q]** A commenter on LeCun's post captures the dynamic that the *style* of disagreement has consequences:

> "Respectfully, your behavior is insufferable because of your dismissiveness. … Yet your dynamic is to mock or shame those who don't meet your bar. Your spite is unproductive, and unwelcoming to young community researchers looking up to your work. Your spite against 𝕏 and anyone who has misconceptions, has only reduced the quality of your insights and alienates even more researchers."

- Source: same as above
- (LinkedIn comment, 2024-12-22, confidence: medium — anonymous, but representative)

The LeCun / Xing JEPA-vs-GLP debate (May 2026) is the most current public version of the world-models-vs-LLMs disagreement. Karpathy is not a participant, but is implicitly on the LLM-as-frontier side.

**[Q]** LeCun in the debate:

> "I'm going to argue for the fact that world models cannot be generative. … Humans and animals learn world models. That's what we use for planning, for reasoning, for predicting everything — that's what allows us to really act intelligently."

> "The idea of JEPA is that you do not attempt to predict pixels. You do not make this a generative model. You encode the part of the video you want to predict."

- Source: https://www.youtube.com/watch?v=8LKgvrNYZz0
- (YouTube debate recording, 2026-05-01, confidence: high — public event)

The Chollet disagreement is more about *what counts as intelligence*. Chollet argues the ARC benchmark shows scaling LLMs has not produced the kind of generalization that matters.

**[Q]** François Chollet, via The Decoder (July 2025):

> "Chollet contends that the major breakthroughs in deep learning during the 2010s were largely driven by falling computing costs. This led to the rise of large language models and the widespread belief that increasing scale would eventually yield artificial general intelligence (AGI). However, the field's focus on ever-larger models, he says, blurred the line between memorized skills and true general intelligence."

> "Even as models like GPT-4.5 increased massively in size, their ARC performance barely improved, reaching only about 10%, while humans consistently score above 95%. For Chollet, this is clear evidence that scaling up pre-training alone does not produce flexible intelligence."

- Source: https://the-decoder.com/francois-chollet-on-the-end-of-scaling-arc-3-and-his-path-to-agi/
- (news, 2025-07-04, confidence: high)

**[I] Pattern across the scaling/AGI disagreements:** This is where Karpathy is *least* distinctive — he sits in the broad middle of the scaling camp. He is not a maximalist (he gives it a decade), he is not a LeCun-style skeptic (he does not reject the LLM paradigm), he is not a Chollet-style "scaling is finished" voice. He is closer to a "the direction is right and the timeline is 3–5 years longer than the hype suggests" position. The *defensibility* of this position is high, but the *distinctiveness* is low.

### B6. "Ephemeral software" / throwaway app thesis

The "super custom, super ephemeral one-off apps by default" position is one of Karpathy's most public 2025 statements and draws direct, sustained pushback from a senior technical voice (Andreas Kirsch, "The Flawed Ephemeral Software Hypothesis").

**[Q]** Karpathy, quoted by Kirsch (May 2025): "super custom, super ephemeral one-off apps by default," predicting the app store will be replaced by generated, disposable software.
- Source: https://www.blackhc.net/essays/future_of_software/
- (essay, 2026+, confidence: high)

**[Q]** Andreas Kirsch rebuttal:

> "While I do believe that software engineering as a whole can be automated, and indeed, any role within the process can and likely will be performed by AI agents in the near future, the automation of individual roles does not make the artifacts those roles produce disposable. Hence, I disagree that this will lead to an 'ephemeral' quality of software."

> "There is a risk for the Motte and Bailey fallacy in the discourse around ephemeral software: evidence for cheap code and fast iteration is treated as evidence that persisted artifact stacks will disappear. Cursor's ARR, Copilot adoption, AI-generated codebases at YC startups, Claude Code revenue, and the Stack Overflow survey mostly show developers producing code cheaper and faster within durable workflows: pull requests, CI, Git, code review. This is not evidence that software has become disposable as the ephemeral software hypothesis claims."

> "The strongest form of the ephemeral software hypothesis occupies the extreme of both axes: continuous regeneration with minimal persisted code artifacts. My argument is that this corner is unstable at scale, and systems that start there migrate toward persisted artifacts as they accumulate users, state, and integration complexity."

> "A different perspective on the issue is that ambiguity has to go somewhere. In non-ephemeral systems, it is progressively resolved into stable code from tests, schemas, interfaces, and operational practice. … In ephemeral systems, that same ambiguity is reintroduced at each regeneration and experienced instead as variance: the same user request can behave slightly differently across runs."

> "I would update moderately toward the ephemeral software hypothesis if, within 2–3 years, the majority of new consumer and internal business applications are generated ephemerally with acceptable reliability (even if critical infrastructure and regulated systems remain durable). … I don't expect to see it soon though."

- Source: https://www.blackhc.net/essays/future_of_software/
- (essay, 2026, confidence: high — this is the most thorough technical rebuttal of a specific Karpathy position found in the search)

**[I] Pattern:** This is the *strongest* example of an informed peer taking a specific Karpathy claim and producing a structured counter-argument with falsification criteria. Kirsch's essay is what a "Karpathy-style reviewer" should aspire to. It is also a useful test case: it engages the claim on its own terms and produces predictions with a specific update rule.

### B7. "Coding agents basically work" — the bifurcation critique

Karpathy's December 2025 post declaring that coding agents "basically didn't work before December and basically work since" drew the bifurcation critique.

**[Q]** Savedelete (responding to the post):

> "Even Karpathy acknowledged 'there are a number of asterisks' — and that's where the skeptic's antenna should perk up. Setting up a personal project on a DGX Spark (a machine most developers will never touch) with well-documented tools following standard patterns is very different from working on production codebases with legacy dependencies, complex business logic, and the kind of edge cases that make senior engineers earn their salaries."

> "Tellingly, one reply in the thread asked: 'When working on production code, and stuff that cannot be easily tested (UI, network, concurrency) I get hardly better results than last year. Am I holding it wrong?' Karpathy's response essentially acknowledged the gap but suggested the developer might need to adapt their workflow — a diplomatic way of saying the tools work great when the problem is shaped right."

> "What's actually happening is a bifurcation. AI coding agents have gotten remarkably good at a specific class of problems: greenfield projects, well-defined tasks, standard toolchains, and problems where the solution space is well-covered in training data. For these, yes — the improvement since December is genuinely impressive."

> "But the messy, ambiguous, context-heavy work that constitutes most professional software engineering? The agents are better, but they're still far from the 'just describe what you want and walk away' vision that the hype suggests."

- Source: https://savedelete.com/article/karpathy-says-ai-coding-agents-basically-work-now-but-lets-not-pop-the-champagne-yet/
- (blog, 2026-02-27, confidence: medium)

**[I] Pattern:** The bifurcation framing — agents are great at greenfield and bad at the long tail — is consistent across the structured-empirical source (Cresswell), the ACM brief, and the savedelete critique. This is the consensus critique of the December 2025 claim. The Karpathy-style reviewer should detect this pattern: a *binary* claim ("basically works" / "basically doesn't") that the evidence supports as a *bifurcated* claim (works in one regime, fails in another).

### B8. The "overweighted" meta-critique

The most uncomfortable critique for the *Karpathy-watching community itself*, articulated clearly in the BirJob piece, is that Karpathy's *visibility* is being conflated with his *accuracy*.

**[Q]** Samadov:

> "The most honest counterargument to this entire article is that Karpathy isn't actually a uniquely accurate signal, he's an unusually visible one. His follower count and his willingness to share takes publicly make him *cited* more often than the median frontier-lab researcher, but citation frequency is not the same as forecast accuracy. There are AI researchers at DeepMind, Meta FAIR, Mistral, and inside Anthropic itself whose work has been more directly load-bearing on the actual trajectory of the field, and whose public profile is much smaller."

> "A specific counterexample: Noam Shazeer (co-author of the original Transformer paper, founder of Character.AI, returned to Google in late 2024 as a Gemini co-lead) has been more central to the actual technical evolution of LLMs than Karpathy. So has Jeff Dean. So has Demis Hassabis. The argument that Karpathy is 'the most accurate signal' relies on the fact that he writes accessibly and posts publicly. Researchers who work primarily inside labs and don't post on X aren't visible, but that doesn't mean they're less correct."

> "The right framing is probably 'Karpathy is the most accurate public signal among the researchers who post publicly.' That's narrower than 'the most accurate signal in AI.' Worth knowing, useful for individual engineers trying to track the field, but not a substitute for reading the actual research papers from the labs doing the work."

- Source: https://www.birjob.com/blog/karpathy-anthropic-pretraining-2026
- (blog, 2026-05-23, confidence: high)

**[I] Pattern:** This critique is *about the audience*, not about Karpathy. It says: you are over-fitting on a high-variance signal because it's the most visible signal. This is the most important critique for the downstream skill to internalize, because the skill itself is a "follow Karpathy's patterns" tool — which risks the same overfitting error.

---

## C. Patterns only visible from outside

### C1. The Karpathy tribe — the "rationalist-adjacent scaling-isn't-dead center"

Karpathy's ideological cluster is a relatively small and well-defined one: he is on the *techno-optimist but not maximalist* end of the AI safety debate, the *pro-scaling-but-not-scaling-is-all-you-need* end of the architectural debate, and the *first-principles* end of the educational debate. He is *not* in the effective-altruist / x-risk maximalist camp (Sutskever, Toner, McCauley). He is *not* in the LeCun / world-models / "LLMs are a dead end" camp. He is *not* in the 3Blue1Brown / pure-math / no-applications camp. He is *not* in the Sebastian Raschka / "let's be careful about empirical claims" camp.

The clearest *named* grouping is with: Andrew Ng (on the value of education as a public good), Demis Hassabis (on a multi-decade AGI timeline), Jeff Dean (on the continued importance of pretraining), and to a lesser extent Simon Willison (on careful, sourced AI commentary).

**[Q]** (Indirectly via Willison's role as curator): Willison collects Karpathy quotes, not arguments with them. This is a meaningful signal of the "tribe" — Willison, a major independent voice, treats Karpathy as a quote-worthy source rather than a person to engage adversarially.
- Source: https://simonwillison.net/ (multiple pages with "a quote from Andrej Karpathy" labels)
- (blog aggregator, 2023–2026, confidence: high)

### C2. The Karpathy anti-tribe — the "shipping critic" camp

The people who *systematically* criticize Karpathy are recognizable:
- Andreas Kirsch (ML researcher, structured essay rebuttals)
- François Chollet (ARC, "scaling is finished" thesis)
- Yann LeCun (JEPA / world models / "LLMs are a dead end")
- A loose cluster of long-tenured software engineers (Cresswell, ACM TechBrief authors, Tom Bolton)
- The "Karpathy is overweighted" critics (Samadov, and anyone who specifically notes that "the field's most-quoted single voice" is a structural problem)

The pattern: the critics are *not* people who think AI is overhyped in general. They are people who are *closer to the metal* than Karpathy is — they ship production systems, run benchmarks at the limit, or build alternatives. The critique is not "stop being excited about AI" — it's "your framing is too high-level for the problem."

### C3. The over-time pattern of agreement vs disagreement

| Year | Position Karpathy takes | Agreement | Disagreement |
|---|---|---|---|
| 2017 | "Software 2.0" | Wide (the direction) | Narrow but specific (the bullet points, see B1) |
| 2019 | "Tesla vision-only for FSD" | Wide in 2019 | Narrow by 2024 — Waymo approach won |
| 2022 | "Building nanoGPT from scratch is the right pedagogy" | Near-universal | Minimal |
| Feb 2025 | "Vibe coding" (personal aesthetic as industry recommendation) | Mixed; "useful for prototyping" yes; "use it for production" no | ACM, Cresswell, savedelete, Samadov |
| May 2025 | "Ephemeral software by default" | Some VC/founder-class | Kirsch, long-tail software engineers |
| Jun 2025 | "Software 3.0 — prompts are the new programming language" | Wide at high level | Narrow (determinism, regulation, see Hundley) |
| Dec 2025 | "Coding agents basically work since December" | "Improved yes, basically works no" | The bifurcation critique (B7) |
| 2026 | "Eureka Labs is the future of education" | In 2024 hype | In 2026 execution, see B3 |
| May 2026 | "Pretraining is back" | Early stage, will be tested | LeCun, Chollet (still) |

**[I] Pattern:** Karpathy is consistently right on *direction* and consistently *too fast* on timeline. Critics who apply a 3–5 year delay to his predictions find them more accurate than reading them at face value (Samadov, B8). This is the most reproducible external pattern in the data.

### C4. The non-obvious pattern: his audience *wants* him to be right

A subtle but visible pattern in the sources: the most positive coverage of Karpathy is *unconditional* in a way that the most positive coverage of, say, Chollet or LeCun isn't. Theureka Labs announcement thread drew "visionary", "GOAT", and "Promethean" comments. The HyScaler piece is one of the few critical notes in a sea of praise. The TIME 100 AI writeup is hagiographic.

**[I] Implication for the downstream skill:** A "Karpathy-style reviewer" that just *agrees with him* is reproducing the same structural bias his audience already has. The skill should be specifically calibrated to *resist* this — to find the things that the receptive audience will overlook. This is exactly the "诚实边界" purpose stated in the task prompt.

---

## D. Karpathy vs other AI educators

This is the comparison the prompt asks for explicitly. The picture that emerges from multiple sources is sharp: Karpathy occupies a *distinct* lane in the AI education ecosystem, defined by what it includes and what it excludes.

### D1. Karpathy vs Andrew Ng

**[Q]** Tom Bolton, after going through both:

> "Both Ng and Karpathy are gifted teachers with a deep grasp of the material they are teaching. What makes them effective teachers, though, is they both know that sharing math or code with students who memorize the math and the code does not add up to understanding. They both recognize how important it is to impart an intuitive understanding of the material."

> "Most satisfying is that they both get right down to the actual mechanics of how these networks work at the level of the math of the individual neuron. Ng describes, at length, the fundamental concepts that enable machine learning and AI using his virtual whiteboard, drawing clear diagrams of the networks and how they function along with hand-written math to go along with the visuals."

> "By contrast, Karpathy spends all of his time in Jupyter notebooks explaining the workings of neural nets with actual Python code. He writes code and shows how it behaves in one circumstance, then in another, and yet another. All in support of developing intuition about its behavior."

> "As excellent as Karpathy's all-code approach is, I'm glad that I had Ng's fundamentals under my belt from years ago. Without that, I suspect it would be a lot harder to follow what Karpathy is walking me through now. … Karpathy, who really only glossed over [embeddings] at a high level in his course."

- Source: https://tombolton.io/2024/09/23/andrej-karpathy-to-the-rescue-of-course/
- (blog, 2024-09-23, confidence: high)

**[I] Distillation:**
- **Ng**: math-first, virtual whiteboard, structured Coursera format, covers the breadth of ML, also has the "structuring ML projects" content that comes from operating experience at Baidu/Google.
- **Karpathy**: code-first, Jupyter notebooks on screen, narrower (deep learning and LLMs specifically), goes deeper on fewer topics, no assignments / no grading.
- **Different abstraction layer**: Ng's Coursera builds *intuition about the math*; Karpathy's YouTube builds *intuition about the code* that runs the math. They are complementary, not competing.

### D2. Karpathy vs 3Blue1Brown (Grant Sanderson)

**[Q]** Dataquest's 2026 ranking:

> "3Blue1Brown's neural network series builds geometric intuition for what a neural network does when it 'learns,' making gradient descent and backpropagation feel spatial and concrete. … Grant does not teach you to write code. He teaches you to think mathematically. That foundation is what separates ML practitioners who can debug a failing model from those who can only copy-paste from tutorials."

> "Andrej Karpathy, former director of AI at Tesla and co-founder of OpenAI, offers something no other YouTube channel can match: deep learning taught from first principles by someone who helped build the most advanced AI systems in the world. … Karpathy does not hide behind library abstractions — he shows you the raw matrix operations, the gradient computations, and the training loops so that you understand exactly what PyTorch does under the hood."

- Source: https://www.dataquest.io/blog/best-deep-learning-courses/
- (review blog, 2026-05-28, confidence: medium)

**[I] Distillation:**
- **3Blue1Brown**: math intuition, geometric/visual, custom Manim animations, no code, "essence of …" framing.
- **Karpathy**: code as truth, real-time debugging, "Zero to Hero" framing, library-agnostic.
- The Dataquest ranking explicitly recommends the *combination* as "the most recommended free deep learning resource across practitioner communities." The two are sequenced: 3Blue1Brown first (math), Karpathy second (code).

### D3. Karpathy vs Jeremy Howard (fast.ai)

**[Q]** Dataquest:

> "You want to build working models immediately, for free: Start with fast.ai. Top-down teaching gets you to results fastest."

- Source: same as above
- (review blog, 2026-05-28, confidence: medium)

**[I] Distillation:**
- **fast.ai (Howard)**: top-down, "get to a working model first," results-first pedagogy, then explain.
- **Karpathy**: bottom-up, "build from a blank file," foundations-first.
- This is the most pedagogically distinct comparison: same audience, opposite sequencing.

### D4. Karpathy vs Sebastian Raschka

The "Prometheans 100" list places them side by side:

**[Q]** PrometheusRoot:

> "Andrej Karpathy — The AI educator who builds from scratch. OpenAI founding member, former Tesla AI director. Now independent — creating the best AI educational content on YouTube. His 'Zero to Hero' series teaches neural networks from first principles."

> "Sebastian Raschka — ML educator, 'Build a LLM from Scratch' author. Author of 'Build a Large Language Model From Scratch' and 'Machine Learning with PyTorch'. University of Wisconsin professor. His from-scratch approach to teaching is unmatched."

- Source: https://prometheusroot.com/prometheans-100/
- (list/blog, n.d., confidence: medium)

**[I] Distillation:**
- **Raschka**: book-form pedagogy, "Build a LLM From Scratch" is the canonical text, university-based, more *complete* (covers the whole LLM), more *cautious* (carefully sourced claims).
- **Karpathy**: video + repo pedagogy, "Zero to Hero" is the canonical video series, independent, more *opinionated*, more *open-ended* (shows his reasoning, not just the answer).
- Raschka is closer to the *what*; Karpathy is closer to the *how and why*. Both are "build from scratch" — but Raschka's "from scratch" is about producing a working LLM, Karpathy's is about understanding PyTorch at the level of the autograd graph.

### D5. Karpathy's distinctive lane

Synthesizing across the four comparisons, Karpathy's distinctive *lane* is:

- **Code over math** (vs Ng)
- **Code over visualization** (vs 3Blue1Brown)
- **Foundations over results** (vs Howard)
- **Process over completeness** (vs Raschka)

The single best one-line summary of his lane is from a LearnWithPath ranking piece:

**[Q]** "His teaching philosophy is that you should be able to build everything from scratch before using a framework. This approach produces practitioners who can diagnose problems, design novel architectures, and reason about model behavior in ways that tutorial-followers simply cannot."

- Source: https://learnwithpath.com/blog/best-youtube-channels-for-machine-learning-2026
- (blog, 2026-03-16, confidence: medium)

This is the *positive* formulation. The *negative* formulation — what's missing from this lane — is also useful:

**[Q]** EZPZ AI, explicitly naming the limit:

> "It's worth noting what Karpathy's pedagogical approach doesn't encode: the accumulated knowledge of having debugged production systems at scale. nanoGPT doesn't cover distributed training failures, model serving latency at high traffic, or the organizational complexity of keeping a large ML codebase maintained by multiple teams. It covers what you need to understand to build the thing from scratch."

> "This is a deliberate scope choice, not an oversight. The 'Zero to Hero' framing is literal: the goal is to take someone from no understanding to working implementation. What happens after you've built it is outside scope."

- Source: https://ezpzai.com/en/2026-05-23-karpathy-nn-zero-to-hero-en/
- (technical blog, 2026-05-22, confidence: high)

**[I] The trade-off:** Karpathy's lane is *the deepest possible "how it works" education*, at the cost of *the surface breadth needed to run production systems*. A Karpathy-style reviewer should be calibrated to notice when a claim requires *production* knowledge to evaluate and the person making the claim has only *foundational* knowledge.

---

## E. The "celebrity" dimension

### E1. The signal of being a celebrity researcher

The clearest signal is *what gets cited*. Time 100 AI, MIT Innovators Under 35, Twitter follower count (~2.3M as of 2026 per nextomoro), YouTube subscribers (1.34M per aiturnpoint). The nextomoro profile explicitly notes this:

**[Q]** nextomoro: "The @AndrejKarpathy YouTube channel surpassed one million subscribers per industry coverage in early 2026, and his X account at @karpathy carries roughly 2.3 million followers. Industry coverage routinely identifies him as the principal explainer-voice for transformer-era neural networks; TIME named him to its first '100 Most Influential People in AI' list in 2024. Comparators in the public-AI-explainer space include podcaster Lex Fridman and YouTube researcher Yannic Kilcher, though Karpathy's profile rests on instructional rather than interview content."

- Source: https://nextomoro.com/andrej-karpathy/
- (profile, 2026-05-02, confidence: high)

### E2. The "Tuesday-tweet becomes Thursday-consensus" effect

The clearest articulation is from Samadov, but the pattern is visible in other sources too.

**[Q]** Samadov: "He has, accidentally, become the field's most-quoted single voice. Things he posts on a Tuesday afternoon become industry consensus by Thursday."

- Source: https://www.birjob.com/blog/karpathy-anthropic-pretraining-2026
- (blog, 2026-05-23, confidence: high)

The vibe-coding episode (B2) is the cleanest case study. The original tweet was a personal aesthetic, and within 48 hours it was a category. This is the *mechanism* by which celebrity-researcher effects distort technical discourse.

### E3. The Wikipedia capture of "celebrity treatment"

**[Q]** Wikipedia currently describes Karpathy's Vibe Coding coinage this way: "In February 2025, Karpathy coined the term vibe coding to describe how AI tools allow hobbyists to construct apps and websites just by typing prompts."
- Source: https://en.wikipedia.org/wiki/Andrej_Karpathy
- (wiki, confidence: medium — Wikipedia is a useful signal of the consensus view, not authoritative on its own)

The Wikipedia phrasing — "coined the term" — is the standard celebrity-researcher treatment. It grants the term *to* Karpathy as if it were a discrete invention, rather than describing a practice many people were already doing.

### E4. The "Kardashian" problem — a distinct pattern

The pattern is: his framing is *more durable* than his content. "Software 2.0" is now a term that means many things to many people, "vibe coding" became Collins Word of the Year 2025, "ghosts not animals" is a metaphor that will outlive the specific argument. This is the *Kardashian problem* of technical research: the *frame* outlasts the *evidence*.

**[Q]** The "vibe coding" becoming Collins Word of the Year 2025 is reported in the aiturnpoint profile:

> "He coined 'vibe coding' in February 2025, a term named Collins English Dictionary Word of the Year 2025."

- Source: https://aiturnpoint.com/andrej-karpathy
- (profile, 2026-04-29, confidence: medium)

**[I] Implication for the downstream skill:** The reviewer should be specifically alert to cases where Karpathy's *frame* is being applied to evidence that doesn't support it. The vibe-coding episode is the cleanest case study. The Software 2.0 → 3.0 update is the cleanest case study of Karpathy *himself* doing this correction.

### E5. "Influencer" vs "researcher" — the receive-side distinction

This is harder to source than the supply-side observations. The clearest *named* distinction is that BirJob piece's "overweighted" critique (B8). The gist: an unusually large share of the community treats Karpathy's *public* statements as if they had the epistemic weight of his *published* research, and they don't.

**[I] Inference:** This means *the audience* (not Karpathy) is the one doing the "influencer" thing. The downstream reviewer should detect when it is operating in the influencer-receive mode and re-calibrate accordingly. The reviewer should be *more skeptical* of Karpathy's Twitter content than of his published work, *more skeptical* of his framework announcements than of his technical results, and *more skeptical* of his decade-out predictions than of his technical observations about specific architectures.

---

## F. The OpenAI 2023 board drama — Karpathy's role

The board drama is not the same topic as the persona critique, but it is one of the few major events in Karpathy's career where the public-record *role* is debated.

### F1. The timeline

**[Q]** Wikipedia, "Removal of Sam Altman from OpenAI":

> "On November 17, 2023, OpenAI's board of directors ousted co-founder and chief executive Sam Altman. In an official post on the company's website, it was stated that 'the board no longer has confidence in his ability to continue leading OpenAI'. The removal was predicated by employee concerns about his handling of artificial intelligence safety, and allegations of abusive behavior. Altman was reinstated on November 22 after pressure from employees and investors."

- Source: https://en.wikipedia.org/wiki/Removal_of_Sam_Altman_from_OpenAI
- (wiki, confidence: high)

**[Q]** The Pragmatic Engineer, timeline of events:

> "Noon (12pm): Sam Altman, CEO of OpenAI and board member, joins a board meeting to which he was invited. At this meeting, he's sacked, effective immediately. The board has 6 members, including Sam. The board's chair, Greg Brockman, is not present."

> "12:23pm: Greg joins a Google meet with the other 4 board members. He's told he is to be immediately removed from the board, and that Sam has been fired."

- Source: https://newsletter.pragmaticengineer.com/p/five-days-of-chaos-at-openai-and
- (newsletter, 2023-11-23, confidence: high)

### F2. Karpathy's role (or non-role)

The notable thing is that **Karpathy does not appear as a named actor in the board drama.** He was *not* on the board. He was *not* cited as a participant in the firing decision. The board members were Sutskever, Adam D'Angelo, Tasha McCauley, Helen Toner, and the additional figure of Greg Brockman (who was removed as chairman). Karpathy is mentioned in the broader coverage as a *co-founder* of OpenAI who had returned earlier in 2023, but the major coverage of the 5-day crisis does not name him as a participant.

Karpathy's own *first major public statement* was his February 2024 departure from OpenAI, which is *after* the drama.

**[Q]** Gizmodo, on Karpathy's Feb 2024 departure:

> "Karpathy is leaving OpenAI roughly one year after he rejoined the company in Feb. 2023. While Karpathy did not provide a reason for his sudden departure, he is the second prominent researcher to exit OpenAI's leadership in recent months, following OpenAI Chief Scientist Ilya Sutskever's unexplained demotion. Both of the leadership changes occurred in the three months since OpenAI's researcher-filled board mysteriously fired CEO Sam Altman."

- Source: https://gizmodo.com/founding-openai-member-andrej-karpathy-leaves-company-1851255288
- (news, 2024-02-14, confidence: high)

**[Q]** Karpathy's own statement, quoted in Futurism:

> "I left OpenAI yesterday," Karpathy tweeted. "First of all nothing 'happened' and it's not a result of any particular event, issue or drama."

> "The team is really great, the people are great, and the roadmap is very exciting, and I think we all have a lot to look forward to. My immediate plan is to work on my personal projects and see what happens."

- Source: https://futurism.com/the-byte/top-openai-researcher-quits
- (news, 2024-02-14, confidence: high)

**[I] Implication:** Karpathy was *near* the drama but not *in* it. The Gizmodo framing ("second prominent researcher to exit") is the closest the mainstream press comes to implying he had any role. The fact that he says "nothing happened" but is *also* leaving right after the drama has produced *low-confidence* speculation (Futurism calls it "conspiracy theories" Karpathy said he found amusing) that cannot be sourced to a confirmed insider account. The downstream skill should be careful here: there is *no* sourced account of Karpathy having a position on the board drama, and inventing one would be a hallucination.

---

## G. Cross-source summary tables

### G1. Praise / criticism asymmetry

| Topic | Praise sources | Substantive criticism sources | Asymmetry |
|---|---|---|---|
| Pedagogy | 6+ independent | Almost none | Heavily asymmetric toward praise |
| Software 2.0 framework | 4+ independent | Perez 2017, Suri 2022, HN 2023 (B1) | Symmetric at macro, asymmetric at bullet |
| Tesla FSD vision-only | 2 (industry coverage) | Samadov, Waymo comparison (B4) | Asymmetric toward criticism in retrospect |
| Vibe coding | Twitter fans, Klover | ACM, Cresswell, savedelete, Samadov (B2) | Symmetric |
| Eureka Labs | Initial 2024 coverage (5+) | Samadov retrospective, HyScaler initial (B3) | Time-dependent — asymmetric in time |
| Ephemeral software | VC/founder class | Kirsch detailed essay (B6) | Symmetric, narrowest technical disagreement |
| Coding agents since Dec | Some | Bifurcation critique, Cresswell (B7) | Symmetric |
| Personality/honesty | Multiple, including critics | None substantive | Asymmetric toward praise |
| AGI timeline / scaling | Some (Willison) | LeCun, Chollet, Karpathy himself (B5) | He sits in the middle |

### G2. Most-cited sources in the search corpus

- https://www.birjob.com/blog/karpathy-anthropic-pretraining-2026 — Samadov's May 2026 retrospective is the most-quoted single piece of criticism. It is the most-cited piece in this document.
- https://en.wikipedia.org/wiki/Andrej_Karpathy — the consensus-view snapshot.
- https://simonwillison.net/ — the most discriminating third-party commentator in the corpus.
- https://news.ycombinator.com/item?id=34881881 — the longest-running skeptical thread on Software 2.0.
- https://venturebeat.com/ai/ex-openai-and-tesla-engineer-andrej-karpathy-announces-ai-native-school-eureka-labs/ — the canonical Eureka Labs announcement coverage.
- https://www.blackhc.net/essays/future_of_software/ — the most thorough direct rebuttal of a specific Karpathy position.

### G3. Confidence map

- **High confidence** (multiple independent sources, no contradiction): Software 2.0 had specific bullet-point problems; the vibe-coding term had a blast-radius problem; the Tesla FSD timeline didn't deliver; Karpathy's *direction* predictions tend to be right; the *timeline* predictions tend to be too fast.
- **Medium confidence** (one or two well-sourced claims, contested in the discourse): Eureka Labs' specific execution was suboptimal; the ephemeral-software thesis is overstated; coding agents have a bifurcation problem.
- **Low confidence** (single source or speculative): Karpathy's role in the OpenAI 2023 board drama (no confirmed involvement); the "celebrity problem" is a *meta-claim* with some evidence but no definitive source.

---

## H. Final synthesis — for the "诚实边界" section of the downstream skill

This is the section the downstream skill most needs. The pattern that emerges is: Karpathy's *blind spots* are not technical. They are *evangelism*, *timeline*, and *production*.

### H1. Three blind spots (what Karpathy can't see about himself)

1. **His framing travels further than his evidence supports.** The Software 2.0 essay got the direction right and the bullets wrong. The vibe-coding tweet was a personal aesthetic and became a production recommendation. The ephemeral-software prediction is a personal intuition and may be a category error. The reviewer should specifically check: *is the evidence cited for this claim enough to support the framing being applied to it?*

2. **His timeline is consistently 3–5 years too fast.** The Tesla FSD promise was 5 years too early. The "year of agents" framing was a decade too early. The Eureka Labs thesis was right but the company may have been too early. The reviewer should specifically check: *if I read this with a 3–5 year delay applied, does the prediction still match?*

3. **He does not have production-system operational knowledge.** The EZPZ critique (D5) and the savedelete bifurcation critique (B7) both note: Karpathy's lane is the *from-scratch* lane, not the *runs-in-production* lane. The reviewer should specifically check: *is this claim about a system that has to run in production, and is Karpathy's claim grounded in production experience or in tutorial experience?*

### H2. Three most common misunderstandings others have of him

1. **"He is the most accurate signal in AI."** He is the most accurate *public* signal among researchers who post publicly. Researchers at DeepMind, Meta FAIR, Mistral, and inside Anthropic itself are doing load-bearing work with much smaller public profiles. Following Karpathy is not a substitute for reading the research.

2. **"He is a celebrity influencer, not a researcher."** His research output (PixelCNN++, RL agents for computer use, midtraining/synthetic data at OpenAI in 2023) is real. The persona critique conflates the *medium* (Twitter, YouTube) with the *substance* (the work). He is, primarily, a researcher who happens to be a good explainer. The downstream skill should not write reviews that assume the influencer framing is the whole story.

3. **"He and OpenAI are aligned."** Karpathy was a *founding* member of OpenAI in 2015, left in 2017, returned in 2023, left in 2024, and joined Anthropic in 2026. The trajectory is *not* a continuous endorsement of OpenAI. The downstream skill should not assume "OpenAI co-founder" implies current alignment.

### H3. Most defensible and most debatable positions

**Most defensible (high external agreement):**
- The Software 1.0 → 2.0 → 3.0 generational framing as a *direction*. Almost no informed critic disputes that LLMs are a major new programming surface. The disagreement is only about pace and granularity.
- "Build from scratch is the right way to teach deep learning." Near-universal agreement, including from non-admirers.
- "Coding agents are a real step change." Symmetric disagreement (B7) is about *how much* of a step, not *whether* a step.
- "Pretraining is not solved." This is now an industry consensus position that Karpathy's Anthropic move helped crystallize.

**Most debatable (the positions a Karpathy-style reviewer should *not* just echo):**
- "Vibe coding is the new default." The ACM, Cresswell, savedelete, and Samadov critiques collectively establish this as *untenable* for production code and *narrowly defensible* for personal experimentation. The reviewer should push back on any use of the term that doesn't specify which regime.
- "Ephemeral software by default." Kirsch's essay is the strongest single rebuttal in the corpus. The reviewer should not accept the framing without testing it against the "ambiguity has to go somewhere" argument.
- "Coding agents basically work since December." The bifurcation critique is consensus. The reviewer should never accept the "basically works" claim as applying uniformly.
- "AI tutors will replace MOOCs." Eureka Labs' specific execution was suboptimal. The thesis is *directional* and the reviewer should distinguish the thesis from the specific bet.

---

## I. Limitations of this research

- **Wikipedia used cautiously.** Wikipedia is cited where it represents the cumulative view of multiple editors, but never as the sole source for a controversial claim.
- **No access to academic citation data.** Who cites Karpathy's papers, in what context, was not in the search results and is not in this document. A reviewer for a specific paper-review task should look at Semantic Scholar / Google Scholar citation context for the paper under review.
- **Twitter primary sources were mostly accessed via secondary aggregators** (Willison, Samadov, etc). A more thorough review would read the original tweet threads.
- **The "vibe coding" critique is over-represented in the corpus** because it is a high-engagement topic with a lot of writing. This does not mean it is the most important critique; it means there is more written material on it.
- **Karpathy's Anthropic move is too recent (May 2026) for full retrospectives** to have formed. The reviewer should expect that the strongest critique of the Anthropic move will appear in late 2026 and 2027.

---

## J. Quick-reference source list (selected)

| URL | Type | Date | Used for |
|---|---|---|---|
| https://medium.com/intuitionmachine/is-deep-learning-software-2-0-cc7ad46b138f | Blog | 2017-11-12 | B1 — early Software 2.0 rebuttal |
| https://zshn25.github.io/Software-2/ | Blog | 2022-12-05 | B1 — concise Software 2.0 rebuttal |
| https://news.ycombinator.com/item?id=34881881 | HN | 2023-02-21 | B1 — Hacker News skeptical thread |
| https://www.acm.org/public-policy/techbriefs/techbrief-vibe-coding | Institutional | n.d. | B2 — formal vibe-coding critique |
| http://www.stephen-cresswell.com/2026/01/01/Why-Are-Experiences-Of-Vibe-Coding-So-Polarised.html | Blog | 2026-01-01 | B2 — empirical experiment |
| https://savedelete.com/article/karpathy-says-ai-coding-agents-basically-work-now-but-lets-not-pop-the-champagne-yet/ | Blog | 2026-02-27 | B7 — bifurcation critique |
| https://www.blackhc.net/essays/future_of_software/ | Essay | 2026 | B6 — strongest single rebuttal |
| https://www.birjob.com/blog/karpathy-anthropic-pretraining-2026 | Blog | 2026-05-23 | B4, B8, C3, E2 — most-cited retrospective |
| https://simonwillison.net/2025/Oct/18/agi-is-still-a-decade-away/ | Blog | 2025-10-18 | B5, A2 — discriminating third-party view |
| https://simonwillison.net/2024/Nov/29/andrej-karpathy/ | Blog | 2024-11-29 | A4 — quote collection |
| https://venturebeat.com/ai/ex-openai-and-tesla-engineer-andrej-karpathy-announces-ai-native-school-eureka-labs/ | News | 2024-07-16 | B3, A1 — Eureka Labs announcement |
| https://techcrunch.com/2024/07/16/after-tesla-and-openai-andrej-karpathys-startup-aims-to-apply-ai-assistants-to-education/ | News | 2024-07-16 | B3 — Eureka Labs measured critique |
| https://hyscaler.com/insights/karpathy-eureka-labs-ai-education/ | Blog | 2024-07-17 | B3 — Eureka Labs skeptical |
| https://en.wikipedia.org/wiki/Andrej_Karpathy | Wiki | n.d. | E3, F1, F2 — consensus view, OpenAI 2023 |
| https://en.wikipedia.org/wiki/Removal_of_Sam_Altman_from_OpenAI | Wiki | n.d. | F1 — board drama timeline |
| https://newsletter.pragmaticengineer.com/p/five-days-of-chaos-at-openai-and | Newsletter | 2023-11-23 | F1 — board drama timeline |
| https://tombolton.io/2024/09/23/andrej-karpathy-to-the-rescue-of-course/ | Blog | 2024-09-23 | D1 — Karpathy vs Ng |
| https://www.dataquest.io/blog/best-deep-learning-courses/ | Blog | 2026-05-28 | D2, D3 — Karpathy vs 3Blue1Brown, Howard |
| https://prometheusroot.com/prometheans-100/ | Blog | n.d. | D4 — Karpathy vs Raschka |
| https://ezpzai.com/en/2026-05-23-karpathy-nn-zero-to-hero-en/ | Blog | 2026-05-22 | D5, A2 — pedagogical lane |
| https://learnwithpath.com/blog/best-youtube-channels-for-machine-learning-2026 | Blog | 2026-03-16 | D5 — Karpathy teaching philosophy |
| https://nextomoro.com/andrej-karpathy/ | Profile | 2026-05-02 | E1 — celebrity-researcher signal |
| https://aiturnpoint.com/andrej-karpathy | Profile | 2026-04-29 | A1, E4 — TIME 100 AI citation |
| https://the-decoder.com/francois-chollet-on-the-end-of-scaling-arc-3-and-his-path-to-agi/ | News | 2025-07-04 | B5 — Chollet scaling critique |
| https://www.youtube.com/watch?v=8LKgvrNYZz0 | Video | 2026-05-01 | B5 — LeCun world-models debate |
| https://www.linkedin.com/posts/yann-lecun_people-posting-on-xtwitter-that-im-wrong-activity-7276713200882966528-HTtZ | LinkedIn | 2024-12-22 | B5 — LeCun-adjacent disagreement |
| https://www.elegantsoftwaresolutions.com/blog/andrej-karpathy-software-3-0-ai-first-development | Blog | 2026-04-09 | A3 — Software 3.0 framing |
| https://www.frenxt.com/cables/claude-code/karpathy-01-software-2-0 | Blog | 2026-04-17 | A2 — Software 2.0 retrospective |
| https://gizmodo.com/founding-openai-member-andrej-karpathy-leaves-company-1851255288 | News | 2024-02-14 | F2 — Karpathy Feb 2024 departure |
| https://futurism.com/the-byte/top-openai-researcher-quits | News | 2024-02-14 | F2 — Karpathy own statement |
| https://stevengong.co/notes/Teacher | Notes | n.d. | A1 — teaching-style observations |
| https://karpathy.ai/ | Personal site | n.d. | self-description context |
| https://mrprompts.substack.com/p/andrej-karpathy-translator-of-modern | Substack | 2026-04-15 | admirer retrospective |
| https://aiturnpoint.com/andrej-karpathy | Profile | 2026-04-29 | A1, E4 |
| https://cms.justoborn.com/karpathy-effect/ | Blog | 2025-10-23 | A1 — "Karpathy Effect" framing |
| https://aiskill.market/blog/karpathy-nanogpt-pedagogy-skill-authoring | Blog | 2026-05-23 | A2, D5 — pedagogical analysis |

---

## K. The "Karpathy-style reviewer" calibration

For the downstream skill, the *one* observation that compresses most of this document is:

> Karpathy is right about direction, too fast about timeline, and over-confident in framing. A reviewer that echoes his *direction* is just adding more noise to an over-saturated channel. A reviewer that catches his *timeline errors* and *framing overreach* is doing something useful.

The reviewer should specifically look for these three things, in this order:

1. **Is the framing of the claim wider than the evidence?** (B1, B2, B6, B7)
2. **Is the timeline presented in a way that won't survive a 3–5 year delay?** (B4, C3, H1)
3. **Does the claim require production-system operational knowledge that the "from-scratch" lane doesn't cover?** (D5, B7, H1)

If any of those three are yes, the reviewer should push back. If all three are no, the reviewer can echo the direction.
