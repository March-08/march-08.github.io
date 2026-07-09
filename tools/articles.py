#!/usr/bin/env python3
"""Generate articles.tsv (id, slug, title, page-date, list-date) and the home index.html.
Dates: real Notion 'Created' where distinct; otherwise spread 9 days apart descending
(older Medium posts only carry a bulk-import date)."""
import re, os
from datetime import datetime, timedelta

SITE = os.path.join(os.path.dirname(__file__), '..', 'site')

# (id, Name, Created) in DESC order by Created
ROWS = [
 ("30f0edd2-4b9c-8015-9066-d000386c621f","Is the Universe a Computer?","2026-02-22"),
 ("2e30edd2-4b9c-805b-9404-e8533faecd17","Introduction to ERC-8004: The Trust Layer for AI Agents","2026-01-09"),
 ("2910edd2-4b9c-80e1-a721-f1a52899bf13","Ethereum: The Infinite World Computer","2025-10-19"),
 ("2870edd2-4b9c-8027-9e4d-d9a38283a223","Blockchain: The Most Misunderstood Technology","2025-10-09"),
 ("26e0edd2-4b9c-809a-b6c8-c1c2e00a147b","Rule-based Matching for Information Extraction with SpaCy","2025-09-14"),
 ("26e0edd2-4b9c-808d-b855-fdd27ebf5514","POS Tagging, Dependency Parser and Named Entity Recognition with SpaCy","2025-09-14"),
 ("26e0edd2-4b9c-80b8-b93a-f882ca40e6b8","Learn about Tokenization, Lemmatization and the Core Operations with SpaCy","2025-09-14"),
 ("2350edd2-4b9c-8076-876c-c78d44a3ddc9","KPOP Optimiser Explained — An Algorithm for Apple Silicon from Exo","2025-07-19"),
 ("2310edd2-4b9c-8075-9ed8-c72fdfae948c","Introduction to Multimodality with LLaVA","2025-07-15"),
 ("2300edd2-4b9c-80a3-8c57-f243597e002f","ZK Proofs — ZKBoo and ZKBoo+","2025-07-14"),
 ("1c20edd2-4b9c-80a7-9bc7-d2dee11df2fb","Manage Environment Variables with Pydantic","2025-03-26"),
 ("1c20edd2-4b9c-80b8-83a9-f02b61cfc34e","Data Engineering — ORM and ODM with Python","2025-03-26"),
 ("1c20edd2-4b9c-8013-a997-ca8170fa0ef5","Design Patterns with Python for ML Engineers: Template Method","2025-03-26"),
 ("1c20edd2-4b9c-80ea-9a1f-dce7521b593b","Level Up Your Coding Skills with Python Threading","2025-03-26"),
 ("1c20edd2-4b9c-80ed-90da-ef79ae96c9b0","Leverage Python Inheritance in ML Projects","2025-03-26"),
 ("1c20edd2-4b9c-80a7-b998-c837fe3faafb","A Gentle Introduction to the DCIN for Decentralized Inference","2025-03-26"),
 ("1c20edd2-4b9c-8080-9552-eca65a7b4d2a","Understanding Einstein's Notation and einsum Multiplication","2025-03-26"),
 ("1c20edd2-4b9c-807e-a794-ca2213927dc9","LLMOps — Serve a Llama-3 Model with BentoML","2025-03-26"),
 ("1c20edd2-4b9c-80d2-be80-e5db5f5c0b9a","Introduction to ETL Pipelines for Data Scientists","2025-03-26"),
 ("1c20edd2-4b9c-8036-9723-fcb9bf9c7f84","MLOps — Data Validation with PyTest","2025-03-26"),
 ("1c20edd2-4b9c-8039-aced-d557a84dbb40","MLOps — A Gentle Introduction to MLflow Pipelines","2025-03-26"),
 ("1c20edd2-4b9c-804c-af5b-e7d7931ab005","A Practical Approach to Algorithm Efficiency","2025-03-26"),
 ("1c20edd2-4b9c-802e-893d-c9fd339097bf","ONNX Unleashed: Training and Optimizing BERT Models for Streamlit Web Apps","2025-03-26"),
 ("1b80edd2-4b9c-8090-8e47-ef7feef706ec","Design Patterns with Python for ML Engineers: Abstract Factory","2025-03-16"),
 ("1b80edd2-4b9c-80d3-97cc-d6591d285c07","Convolutions in One Dimension using Python","2025-03-16"),
 ("1b80edd2-4b9c-8057-94fe-e074846a7070","Stop Using Print, and Start Debugging","2025-03-16"),
 ("1b80edd2-4b9c-80e4-b189-e1df68c8c136","Train YOLO for Object Detection on a Custom Dataset using Python","2025-03-16"),
 ("1b80edd2-4b9c-8067-8605-fb42e497536b","From Planetary Orbits to Relativity: A Tale of Data and Discovery","2025-03-16"),
 ("1b80edd2-4b9c-8049-98aa-f3155bcfd49b","Fine-Tuning for Domain Adaptation in NLP","2025-03-16"),
 ("1b80edd2-4b9c-80b1-be02-da0df86d303d","Visualized Linear Algebra to Get Started with Machine Learning: Part 2","2025-03-16"),
 ("1b80edd2-4b9c-8092-b785-c78972194c78","Visualized Linear Algebra to Get Started with Machine Learning: Part 1","2025-03-16"),
 ("1b80edd2-4b9c-80c9-a759-c84053c7315b","A Visual Explanation of Variance, Covariance, Correlation and Causation","2025-03-16"),
 ("1b80edd2-4b9c-801f-9855-d9a661780fbd","Clean Code in PyTorch: Best Practices for Readable ML","2025-03-16"),
 ("1b80edd2-4b9c-80ba-adea-e839a4111695","Hands-on Generative AI with GANs using Python: Autoencoders","2025-03-16"),
 ("1b80edd2-4b9c-801e-8da7-d33ed58d8524","Hands-on Generative AI with GANs using Python: Image Generation","2025-03-16"),
 ("1b80edd2-4b9c-80ef-9f74-ebcda0ac5995","Fine-tune a Large Language Model with Python","2025-03-16"),
 ("1b80edd2-4b9c-805f-92ce-f3f44ea4f830","Fast Prototyping with Hugging Face's Inference API","2025-03-16"),
 ("1b80edd2-4b9c-8046-8043-f343b9e01e56","LangChain: Develop Applications Powered by Language Models","2025-03-16"),
 ("1b80edd2-4b9c-8075-87ee-fed845318a62","Distilling Step-by-Step: Paper Review","2025-03-16"),
 ("1b80edd2-4b9c-80f1-99c9-c5b8ebeb4b19","How to Handle Label Scarcity: A Visual Explanation","2025-03-16"),
 ("1b80edd2-4b9c-80a4-bfa7-cbdea987d459","LangChain: Enhancing Performance with Memory Capacity","2025-03-16"),
 ("1b80edd2-4b9c-8078-a7f3-c2b8ccf4c2d7","LangChain: Allow LLMs to Interact with Your Code","2025-03-16"),
 ("1b80edd2-4b9c-8070-9143-d3ea4313004e","Keep Track of Your Experiments with Hydra","2025-03-16"),
 ("1b80edd2-4b9c-80cb-9b21-c5fa62b5f271","Gorilla — Enhancing LLMs' Ability to Use API Calls","2025-03-16"),
 ("1b80edd2-4b9c-80cd-87da-ca5db6c2a240","According to Aristotle, Would ChatGPT Be Able to Think?","2025-03-16"),
 ("1b80edd2-4b9c-8003-b089-e463c0ee6da4","Serving a PyTorch Model with FastAPI and Docker","2025-03-16"),
 ("1b80edd2-4b9c-809e-9c3c-ce11d79962c7","Design Patterns with Python for ML Engineers: Prototype","2025-03-16"),
 ("1b80edd2-4b9c-8072-8aad-cae0926aced9","A Simple CI/CD Setup for ML Projects","2025-03-16"),
 ("1b80edd2-4b9c-8071-812a-c4e22c62ca0b","Deploy Tiny-Llama on AWS EC2","2025-03-16"),
]

def slugify(name):
    s=name.lower()
    s=s.replace("&","and")
    s=re.sub(r"[’']", "", s)
    s=re.sub(r"[^a-z0-9]+","-", s).strip("-")
    return re.sub(r"-+","-",s)[:70]

# spread dates: strictly descending, >=9 days apart when duplicates
prev=None; recs=[]
for pid,name,created in ROWS:
    d=datetime.strptime(created,"%Y-%m-%d")
    if prev and d>=prev: d=prev - timedelta(days=9)
    prev=d
    recs.append((pid, slugify(name), name, d))

# articles.tsv
with open(os.path.join(os.path.dirname(__file__),"articles.tsv"),"w",encoding="utf-8") as f:
    for pid,slug,name,d in recs:
        f.write(f"{pid}\t{slug}\t{name}\t{d.strftime('%B %-d, %Y')}\n")

# home index.html
import html as H
rows_html="\n".join(
    f'      <li><a class="title" href="{slug}.html">{H.escape(name)}</a>'
    f'<span class="date">{d.strftime("%B %-d, %Y")}</span></li>'
    for pid,slug,name,d in recs)

HEAD='''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="tufte.css">
<link rel="stylesheet" href="custom.css">
<link href="https://fonts.googleapis.com/css?family=Lato:400,400italic" rel="stylesheet">
<link rel="icon" href="images/avatar.png">'''
home=f'''<!doctype html>
<html lang="en">
<head>
<title>Marcello Politi</title>
{HEAD}
</head>
<body class="layout-post">
  <header>
    <nav class="group">
      <a href="index.html">Home</a>
      <a href="#">About me</a>
      <a href="notebooks.html">Notebooks</a>
      <a href="lectures.html">Lectures</a>
      <a href="travels.html">Travels</a>
    </nav>
    <div>
      <p><a class="namelink" href="index.html" rel="me">Marcello Politi</a></p>
      <img class="headshot" src="images/photo.jpeg" alt="Marcello Politi">
      <p>I am a Research Scientist at the <a href="https://ai.ethereum.foundation/">Ethereum Foundation</a>,
        on the dAI team, where I work on decentralized AI: self-evolving multi-agent systems, on-chain LLM
        coordination, and decentralized inference for trustworthy AI economies.<span class="marginnote">Find me on
        <a href="https://www.linkedin.com/in/marcello-politi/">LinkedIn</a>,
        <a href="https://twitter.com/_March08_">X</a> and
        <a href="https://medium.com/@marcellopoliti">Medium</a>.</span> Before Ethereum I built deep-learning
        and space-tech systems with the <a href="https://www.esa.int/">European Space Agency</a> and
        <a href="https://mistral.ai/">Mistral AI</a>.</p>
    </div>
  </header>
  <article>
    <h2 class="writing-h">Writing</h2>
    <ul class="postlist">
{rows_html}
    </ul>
  </article>
<script src="site.js"></script>
</body>
</html>
'''
open(os.path.join(SITE,"index.html"),"w",encoding="utf-8").write(home)
print(f"generated index.html ({len(recs)} posts) and articles.tsv")
print("date range:", recs[0][3].strftime('%b %Y'), "→", recs[-1][3].strftime('%b %Y'))
