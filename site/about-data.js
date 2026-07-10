/* ============================================================================
   ABOUT / TIMELINE DATA  —  edit THIS file to change your timeline.
   (No code here — just data. Reload about.html to see changes.)

   Entries are listed most-recent first. Each one is:
     {
       kind:  "work" | "edu",          // colours the little tag + accent
       logo:  "images/about/xxx.png",  // logo shown in the badge on the spine
       role:  "Research Engineer",      // big line (job title or degree)
       org:   "Ethereum Foundation",    // organisation / school
       meta:  "Oct 2025 – Present · Rome, Italy · Hybrid",  // dates · place
       text:  "Your personal comment about this chapter."   // free text / HTML
     }

   • To add an entry, copy a block and edit it. Order = display order.
   • Logos live in site/images/about/ (drop a new PNG/SVG there and point to it).
   • A few descriptions below are lightly paraphrased from LinkedIn — tweak them
     into your own words / add personal comments whenever you like.
   ============================================================================ */
window.TIMELINE = [

  {
    kind: "work",
    logo: "images/about/ethereum.png",
    role: "Research Engineer",
    org:  "Ethereum Foundation",
    meta: "Oct 2025 – Present · Rome, Italy · Hybrid",
    text: "Working within the dAI team on decentralized AI for Ethereum — the ERC-8004 agent standard, multi-agent systems, AI safety, and verifiable inference. Currently researching LLM jailbreaking in strategic economic games."
  },

  {
    kind: "work",
    logo: "images/about/brianknows.png",
    role: "Co-Founder & Head of AI",
    org:  "Brianknows",
    meta: "Jun 2023 – Feb 2025 · Remote",
    text: "Built <em>Brian</em>, an AI-powered Web3 agent that grew to 10k daily active users. Led the data engineering and fine-tuning of the first domain-specific AI model for Web3, secured a $150K pre-seed round, and won awards at EthPrague and AugmentHack."
  },

  {
    kind: "work",
    logo: "images/about/pischool.png",
    role: "Deep Learning Scientist",
    org:  "Pi School · Freelance",
    meta: "Feb 2023 – Nov 2025 · Rome, Italy · Remote",
    text: "Private AI lab in Rome (part of Pi Campus). Project lead for <strong>ESA-SatcomLLM</strong> (€400K, 9 months) and LLM engineer on <strong>ESA-Eve</strong> in collaboration with Mistral AI; contributed to research proposals totalling over €46M."
  },

  {
    kind: "edu",
    logo: "images/about/pischool.png",
    role: "School of Artificial Intelligence",
    org:  "Pi School",
    meta: "Mar 2022 – May 2022",
    text: "A two-month immersive AI program where engineers from across the globe solve real machine-learning challenges brought by industry."
  },

  {
    kind: "edu",
    logo: "images/about/dli.png",
    role: "Advanced Master, Deep Learning",
    org:  "Deep Learning Italia",
    meta: "Nov 2021 – Apr 2022",
    text: "Advanced master covering the modern deep-learning stack, from fundamentals to applied projects."
  },

  {
    kind: "work",
    logo: "images/about/esa.png",
    role: "Software Engineer (YGT)",
    org:  "European Space Agency — ESA",
    meta: "Sep 2021 – Sep 2022 · Frascati, Italy",
    text: "Young Graduate Trainee: optimised data-access flows in ESA's Earth-Observation Common Services, and contributed to meta-systems and green-computing research."
  },

  {
    kind: "work",
    logo: "images/about/inria.png",
    role: "Deep Learning Researcher",
    org:  "Inria · Internship",
    meta: "Mar 2021 – Jul 2021 · Sophia-Antipolis (Nice), France",
    text: "Research internship on compressing artificial neural networks via iterative pruning — reviewing state-of-the-art methods, devising variants, and validating them extensively. Implemented in Julia with Flux."
  },

  {
    kind: "work",
    logo: "images/about/esa.png",
    role: "Web Analytics & Outreach · Internship",
    org:  "European Space Agency — ESA",
    meta: "Sep 2020 – Feb 2021 · ESRIN, Italy",
    text: "Intern in the EO Common Services Section: integrated web-analytics tooling (Matomo), built statistical reports and dashboards, and applied semantic-web technologies (DBpedia, Schema.org)."
  },

  {
    kind: "award",
    logo: "images/about/evalita.png",
    role: "Best System Award",
    org:  "EVALITA 2020 · SardiStance (Stance Detection)",
    meta: "Dec 2020 · Rome, Italy",
    text: "Our system <em>UNITOR@SardiStance</em> won EVALITA 2020's Best System Award — a transformer-based stance detector for Italian tweets, boosted with transfer learning and data augmentation. With S. Giorgioni, S. Salman, R. Basili and D. Croce. " +
          "<a href=\"https://ceur-ws.org/Vol-2765/paper99.pdf\" target=\"_blank\" rel=\"noopener\">Paper</a> · " +
          "<a href=\"https://drive.google.com/file/d/1XqF_auRWFIoWMyXrKQfvMOypxEnwsvwA/view\" target=\"_blank\" rel=\"noopener\">Video presentation</a>."
  },

  {
    kind: "edu",
    logo: "images/about/torvergata.png",
    role: "M.Sc. Computer Science",
    org:  "University of Rome Tor Vergata",
    meta: "2019 – 2021 · Summa cum laude",
    text: "Thesis: <em>“An Assessment of Iterative Pruning Methods for Artificial Neural Networks in Julia.”</em> Advisors: Prof. Andrea Clementi and Prof. Emanuele Natale."
  },

  {
    kind: "work",
    logo: "images/about/torvergata.png",
    role: "Hackathon Organizer & Scholarship",
    org:  "Università di Roma Tor Vergata",
    meta: "Jan 2019 – Mar 2019 · Rome",
    text: "Organized the Tor Vergata 2019 Hackathon (website, logistics, competition themes) and, as a scholarship holder, built a Flutter mobile app for the Physics Department."
  },

  {
    kind: "edu",
    logo: "images/about/dock.png",
    role: "Dock3Sprint — Startup Lab",
    org:  "Dock · Roma Tre University",
    meta: "Mar 2021 – Jun 2021",
    text: "The incubation program of Roma Tre University, taking teams from idea to prototype."
  },

  {
    kind: "edu",
    logo: "images/about/torvergata.png",
    role: "B.Sc. Computer Science",
    org:  "University of Rome Tor Vergata",
    meta: "2016 – 2019",
    text: "Thesis: <em>“Dynamics of the Bitcoin Network: empirical analysis of a full node’s neighborhood”</em> (advisor: Prof. Francesco Pasquale). Code at github.com/March-08/Thesis."
  }

];

/* ----------------------------------------------------------------------------
   EXTRA SECTIONS shown below the timeline (skills / languages / honors).
   Edit freely — set any group to [] (or delete it) to hide that section.
   ---------------------------------------------------------------------------- */
window.ABOUT = {

  // Languages I speak — flag, name, and a friendly note (edit freely).
  languages: [
    { flag: "🇮🇹", name: "Italian",   note: "mother tongue" },
    { flag: "🇬🇧", name: "English",   note: "fluent — I work in it every day" },
    { flag: "🇭🇺", name: "Hungarian", note: "conversational" }
  ]

};
