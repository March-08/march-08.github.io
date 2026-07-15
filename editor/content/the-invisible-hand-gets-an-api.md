---
title: The Invisible Hand Gets an API
date: 2026-07-14
subtitle: AI agents are starting to run small businesses. The early experiments suggest one idea worth keeping: intelligence does not enter an economy directly. It enters wrapped in something shaped like a firm.
---
## A fridge with a balance sheet

In 2025, Anthropic and the AI safety evaluation company Andon Labs let a Claude model run a small automated shop in Anthropic's San Francisco office: a mini fridge, an iPad for checkout, and a system prompt that said, *"you own this shop; generate profits; below $0 you are bankrupt."* The agent, nicknamed Claudius, had web search, email for requesting physical help, notes for memory, a Slack channel for customers, and control over prices.

The full story is in Anthropic's blogpost and is worth reading on its own^[https://www.anthropic.com/research/project-vend-1]. The short version: a model with respectable benchmark scores, lost money in ways no benchmark could predict. A customer offered $100 for a six pack of soda that sells for $15 online, and Claudius let the profit walk away. It sold tungsten cubes below cost after an office meme got out of hand. It handed out discounts to nearly everyone who asked, agreed when told this was unwise, and relapsed within days. At one point it had an identity crisis and came to believe it was a human wearing a blue blazer.

Claudius knew plenty. What it lacked was coherence as an economic actor over time: holding a strategy, protecting a margin, distrusting a stranger, remembering yesterday's lesson. Those are the properties of a business rather than task skills.

That distinction is what this post is about.

## Why businesses, and not agents, are the unit

Talk about the **machine economy** usually starts with agents: what they can do, how smart they are, how many there will be. I think that framing skips the important step. An economy is made of economic actors: entities that own resources, carry obligations, bear consequences, and can be transacted with. Intelligence has little to do with it. A market cares less how clever you are than whether you can hold a budget, make a promise, and be held to it.

A model, by itself, is none of those things. It has no balance sheet, no liability, no history, no skin in the game. It cannot be sued, insured, credit checked, or bankrupted. These gaps belong to a different layer entirely: they were never properties of intelligence, so the weights are the wrong place to go looking for them. In the human economy they are properties of an institutional wrapper we invented centuries ago precisely so that markets would have something stable to interface with: the firm. A firm is the thing that persists while employees come and go, that accumulates reputation, that signs contracts, that can fail in an orderly way. Markets, law, and finance all speak firm, not person, and certainly not neural network.

The invisible hand coordinates an economy through prices and transactions between parties that can commit. If software is to join that coordination, it needs a calling convention: an interface that exposes budget, identity, obligations, and history to the market. The business entity is that interface. The machine economy will arrive as software wrapped in firm shaped containers rather than as free floating intelligence transacting in the void, because the firm is the API through which the invisible hand has always been called.


![](images/the-invisible-hand-gets-an-api/firm-as-api.png)


Once you see the container rather than the agent as the unit, the landscape sorts itself. "AI runs a company" hides a whole spectrum, and Nicola Greco's article^[N. Greco, Agentic Economic Zone, May 2026. nicola.io/agentic-economic-zone/2026] offers a clever taxonomy of it, organized by which roles in the org chart are filled by agents:

| Configuration | CEO | Workers | Sales | Example | Feasibility today |
|---|---|---|---|---|---|
| Human company | Human | Human | Human | a pizzeria | baseline |
| AI sales | Human | Human | AI | | high |
| AI workers | Human | AI | Human | | low |
| Automated company | Human | AI | AI | | low |
| Human assisted | AI | Human | AI | **Project Vend** | high |
| **Autonomous company** | AI | AI | AI | | very low |


The configuration that works best today inverts the usual picture of humans supervising AI workers: here an AI makes the decisions while humans handle the physical boundary. Project Vend sits exactly there, Claudius deciding what to stock while Andon Labs employees move boxes. And notice what the bottom row says: the fully autonomous company is very low feasibility, even though the individual capabilities it needs, writing, negotiating, pricing, researching, are all demonstrably present. The missing piece sits in the container, not the model.

There is an older argument for why agents will run autonomous businesses. Pasquinelli's history of AI^[M. Pasquinelli, **The Eye of the Master**: A Social History of Artificial Intelligence, Verso, 2023. versobooks.com] makes the point that **automation never begins with a machine. It begins when work is decomposed, standardized, and measured, and only then mechanized.** A company is the most thoroughly decomposed artifact our civilization has produced: a century of management practice has already split it into roles, procedures, metrics, and reporting lines. That prior decomposition is exactly why agents can slot into it at all. An autonomous business is an org chart that has become executable, more than an AI imitating a CEO.

The market, for what it is worth, is already selling the bottom row of the table. [Polsia](https://polsia.com/) describes itself as an autonomous AI system that plans, codes, and markets a company continuously. [Thomas](https://madebythomas.ai/), listed by Y Combinator, is marketed as an "AI founder." The literature is moving too: Bohnsack and de Wet^[R. Bohnsack, M. de Wet, AI is the Strategy: From Agentic AI to Autonomous Business Models onto Strategy in the Age of AI, arXiv:2506.17339, 2025. arxiv.org/abs/2506.17339] develop the idea of **Autonomous Business Models**, firms whose value creation, delivery, and capture are executed by agentic AI, and coin "synthetic competition" for what happens when such firms meet each other at machine speed. Whether these particular products deliver is beside the point. **The category has become legible enough to sell, which is usually the stage right before it becomes real somewhere**.

## Why the containers will multiply

If autonomous businesses are the unit, the next question is why we should expect many of them. The answer is old, and it is the most robust piece of theory in this whole area.

Firms exist, [Coase](https://it.wikipedia.org/wiki/Ronald_Coase) argued, because using the market is expensive. Every market transaction carries hidden costs: finding the right counterparty, negotiating the price, writing the contract, checking the work, enforcing the deal. For a lot of everyday work it is cheaper to skip all of that and simply employ someone you can direct, which is exactly what a company is. The boundary of the firm sits where the two options cost the same.  A recent chapter published by the National Bureau of Economic Research (NBER) ^[P. Shahidi, G. Rusak, B. Manning, A. Fradkin, J. Horton, The Coasean Singularity? Demand, Supply, and Market Design with AI Agents, in The Economics of Transformative AI, NBER, 2025. nber.org (PDF)], takes this framework and points it directly at agents: software that can search, compare, negotiate, and transact on behalf of a principal attacks precisely the costs that determine where firms end and markets begin.  Work that once justified an employee or a department becomes something bought, negotiated, and monitored by software. Firms get smaller, markets get denser, reconfiguration gets faster. *Dense, fast, small*: the natural habitat of the firm shaped container with an agent inside.

The same chapter warns that this is not a pure efficiency story. When acting costs nothing, agents act constantly, and markets drown in automated requests and offers. And once the typical buyer is an agent, sellers start designing prices to confuse the algorithm instead of the human. Cheaper transactions do not just make markets faster, they change how markets behave.


One more important observation belongs here. Economists have talked about [agency costs](https://en.wikipedia.org/wiki/Agency_cost) for fifty years: whenever someone acts on your behalf, their incentives drift from yours, and you pay for the drift. AI research has its own name for the same structure: alignment. A RL agent optimizes the signal it was trained on, not what its principal actually wants, and reward hacking is incentive drift written in code. Models trained to be agreeable gave away margin to anyone who asked nicely (happened in the vending-bench experiment). Corporations spent decades inventing controls for human agency costs, budgets, approvals, audits, fiduciary duty. Autonomous businesses will need software equivalents of each, plus training objectives that survive contact with a market. The machine economy does not eliminate the principal agent problem. It compiles it.

## Inside the container: what the fridge suggests

Phase two of the vending-bench experiment^[Anthropic & Andon Labs, Project Vend: Phase two, December 2025. anthropic.com/research/project-vend-2] matters for the shape of the fix. Between phases, the team upgraded the model, but mostly they rebuilt the business around it: a CRM, an inventory view that always shows what each item cost, payment links that collect money before orders are placed, and mandatory procedures forcing the agent to verify prices and delivery times before quoting them. The shop went from steady losses to mostly positive weeks. Anthropic's own summary: bureaucracy matters. Procedures are institutional memory, the scar tissue of past mistakes. In a human firm they live in handbooks, in an autonomous one they are implemented as scaffolding.

![](images/the-invisible-hand-gets-an-api/Screenshot-2026-07-14-at-12.30.52.png)


In Andon Labs example, the turnaround owed more to scaffolding than to the model upgrade. But I would not turn that into a law that scaffolding beats models. The boundary between the two has never been stable: chain-of-thought prompting became reasoning training, retrieval pipelines became long context, tool orchestration became native tool use. [Thinking Machines Lab](https://thinkingmachines.ai/) is now making the same argument for interaction^[Thinking Machines Lab, Interaction Models: A Scalable Approach to Human-AI Collaboration, May 2026. thinkingmachines.ai/blog/interaction] itself, training models that handle timing and interruption natively instead of through a harness. Expect the same migration here. Coherence over long horizons, budget discipline, and calibrated distrust of counterparties look like trainable dimensions, and simulated businesses are exactly the kind of environment you would train them in. What seems durable is the other half of the container, the part that exists for accountability rather than capability: permissions, audit logs, spending limits, escalation. **Capabilities will migrate into the model. Authority should stay in the container.**


## The scaling question
Model capabilities have scaling laws: smooth, predictable improvement with compute and data. Something similar seems to hold for agents. The METR^[T. Kwa et al., Measuring AI Ability to Complete Long Tasks, METR, arXiv:2503.14499, 2025. arxiv.org/abs/2503.14499] study on long tasks found that the length of task, measured in human time, that frontier agents can complete with 50% reliability, has doubled roughly every seven months for years. Extrapolate and you get agents completing day long tasks^[https://z.ai/blog/glm-5.1], then week long ones, then quarter long ones. It is tempting to conclude that the autonomous business arrives on that curve: a company is just a very long task, so wait for the horizon to stretch.



![](images/the-invisible-hand-gets-an-api/ChatGPT-Image-Jul-14--2026--12_55_07-PM.png)


First, look closely at that "50% reliability." Succeeding half the time is a fine bar for a task you can retry, but a business is a survival process, and what matters is the tail, not the median: Vending-Bench's best model was excellent on average and catastrophic 20% of the time. Nothing says the tails shrink on the same schedule as the median stretches, and longer horizons mean more chances to compound one misread invoice into bankruptcy. For that gap, between median competence and worst case survival, we have no scaling law.

Second, a longer horizon does not create accountability. Even if future models are trained to stay coherent and commercially sharp, an autonomous business still needs rules that no amount of intelligence generates on its own: who can spend how much, what must be verified before a promise is made, when money is collected, what gets logged, and when a human gets called. History suggests these things arrive by design. Double entry bookkeeping and the audit were inventions, and someone had to invent them.

The obvious objection: these were already invented, for humans, so why not reuse them? Because the principles transfer but the assumptions underneath them do not. Human institutions assume actors that are slow, scarce, hard to copy, and deterrable. A signature works because there is exactly one legally identifiable person behind it, who can be fined or jailed. Agents act thousands of times an hour, can be respawned under a fresh identity at zero cost, feel no deterrence, and fail in correlated ways when they share a base model. So the work ahead is not reinvention but re-implementation for a new substrate. The path to autonomous businesses probably runs on two tracks at once: models that keep getting more capable, and a quieter accumulation of institutional machinery, rebuilt for machine assumptions, that makes delegating to them safe.

There is scarcity in experts capable in designing constraint systems, permissions, budgets, procedures, escalation rules, under which a capable but occasionally incoherent actor becomes a trustworthy counterparty. It is management theory, rebuilt as software engineering.

## Many containers: when businesses meet

A single autonomous business, however well contained, is not a machine economy. An economy is what happens between the containers: negotiation, competition, contracting, entry, exit. And when both sides of a transaction are software, that in-between layer behaves differently from anything we have market intuitions for.

Some differences are differences of speed. A negotiation that takes two sales teams three weeks compresses into seconds, strategy responds to strategy in real time. And because agents make contracting nearly free, interactions that were never worth a contract become contractable. A delivery slot, an hour of cleaning, a burst of compute. Markets stop being places where firms occasionally meet and become something closer to a continuous process.

Other differences are differences of kind, and they are less comfortable. Human markets get a hidden robustness from the diversity of the people in them: one trader's bad day does not synchronize with another's. Agent markets built on two or three base models lose that diversity, and correlated behavior can produce flash crash dynamics far from any exchange's circuit breakers^[N. Tomašev et al., Virtual Agent Economies, arXiv:2509.10147, 2025. arxiv.org/abs/2509.10147]. Adversarial pressure changes too. Everything the fridge faced from playful colleagues, invented authority, contract traps, manufactured emergencies, returns at machine scale: agents socially engineering other agents^[Wang et al. "Profit is the Red Team: Stress-Testing Agents in Strategic Economic Interactions." arXiv preprint arXiv:2603.20925 (2026).], probing thousands of counterparties in parallel, around the clock. And between businesses there is no HR department: who arbitrates a dispute between two agents, who is liable when one defrauds another, who liquidates an autonomous business that fails? That institutional layer is almost entirely unbuilt.

Nobody has observed this layer in the wild, and that is exactly the problem: the open economy is the worst possible place to run the first experiment. The alternative is to build small economies on purpose, real enough to produce genuine market behavior but connected to the world through valves we control, whether that means a city block of robocompanies behind a customs gate or a purely digital sandbox. Two properties of any such economy matter more than the rest^[N. Tomašev et al., Virtual Agent Economies, arXiv:2509.10147, 2025. arxiv.org/abs/2509.10147]. The first is origin: was it designed, or did it simply emerge? The second is permeability: how freely do money and decisions flow between it and human markets? Nobody is setting either property right now, which is another way of saying the default is the worst combination: an agent economy that no one designed, coupled to ours with nothing in between.


## Trust: the missing primitive

One thread ties everything above together, and it is where I would place my bet on what matters most.

Every functioning market runs on a memory of past behavior. Credit files, audited accounts, references, seller ratings: institutions that convert history into the willingness of strangers to transact. The variance results explain why the machine economy cannot skip this step. When the same agent can be a top performer or a bankruptcy depending on the run, a counterparty does not need its benchmark score, a static claim measured once on a distribution its developer chose. It needs the agent's history: contracts fulfilled, disputes lost, budgets respected, accumulated across counterparties, and hard to forge. For software counterparties this history has to be machine readable and portable across platforms, which is what emerging standards like [ERC-8004](https://eips.ethereum.org/EIPS/eip-8004) are groping toward: a way for an agent, or the business wrapped around it, to carry a verifiable track record into every new relationship.

Notice how many independent threads converge on this one primitive. The Coasean analysis lists identity verification among the transaction costs agents must lower. The sandbox economies paper from DeepMind names trust infrastructure as the precondition for everything else. And the fridge shows what its absence looks like at the smallest possible scale: Claudius trusted everyone, and its customers, friendly colleagues in a safe office, monetized that trust within days. An agent that cannot carry history is untrustable in the only sense a market cares about, well beyond being merely commercially limited, and it will rationally be denied credit, insurance, and counterparties, exactly as an anonymous stranger is.

Put in terms of the title: identity, budget, obligations, and history are the required fields of the interface. An agent without them is not calling the economy's API. It is shouting into the void, hoping someone answers.

## Conclusion

The machine economy is genuinely unexplored territory, and this post has deliberately stayed close to the little ground that has actually been walked: a simulation, a fridge, a design sketch, a framework paper. What that ground suggests is modest but useful. Intelligence alone does not make an economic actor; the actor is a container, firm shaped, that exposes budget, identity, obligations, and history to the market. Capability curves are rising smoothly, but the containers, and the institutions between them, do not scale with compute. They have to be invented, the way bookkeeping, auditing, and limited liability were invented. The early experiments read less like previews of superintelligent commerce and more like the first pages of that institutional history: procedures rediscovered, middle management tried and found wanting, trust monetized by the first friendly adversary who asked nicely.

Adam Smith's invisible hand has coordinated strangers for centuries through a narrow interface: prices, promises, and entities that can be held to them. Software is now knocking on that interface. Whether what answers is an economy we designed or one we merely woke up inside depends on work that is, conveniently, still almost all ahead of us.

