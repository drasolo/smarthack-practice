# Planul celor 24 de ore

Fazele evenimentului, ce trebuie să fie gata la fiecare poartă și ce facem dacă rămânem în urmă.

Surse: documentul de pregătire din 3 noiembrie. Este planul nostru, nu programul oficial. Orele sunt
relative la start, iar cele exacte le anunță organizatorii. Ultima verificare: 2026-11-06.

## Regula principală

**La ora 10, demo-ul trebuie să meargă cap-coadă, oricât de urât.** Dacă nu merge, tăiem din idee
până merge. Tot ce urmează se construiește peste o variantă funcțională.

## Fazele

| Ore | Fază | Ce facem | Poartă la final |
| --- | --- | --- | --- |
| H0-H2 | Înțelegem problema | Tema și criteriile, deschidem datele, întrebăm mentorii, alegem o idee din 2-3 | Idee aleasă, problema într-o frază cu o cifră PPC |
| H2-H3 | Contractul | Repo, schema datelor, JSON-ul endpoint-urilor, mock-uri | Fiecare rulează partea lui pe mock-uri |
| H3-H10 | Prima felie cap-coadă | Date reale, baseline, API, un ecran. Sincronizare de 5 minute la H6 și H9 | **Demo cap-coadă pe date reale** |
| H10-H16 | Îmbunătățim | Model mai bun, explicație LLM, guardrails, tabel de evaluare. Somn pe rând, câte 2 ore, mereu cel puțin doi treji | Fără funcționalități noi |
| H16-H20 | Lustruim | Bug-uri, UI, 5 încercări de prompt injection, README cu ce am pregătit dinainte, video de rezervă | Fără cod nou, video înregistrat |
| H20-H24 | Pitch-ul | Slide-uri, două repetiții cronometrate, întrebări probabile și cine răspunde la fiecare | Gata de prezentat |

## În primele 2 ore, cu mentorii PPC

Întrebările sunt în [intrebari-deschise.md](intrebari-deschise.md). Trebuie să aflăm ce metrică
contează, ce înseamnă fiecare coloană, cine ar folosi soluția și dacă datele au voie să iasă spre un
API extern.

## Dacă datele nu au voie să iasă

Datele brute stau în afara repo-ului, iar agenții primesc doar schema și rânduri sintetice. Regulile
sunt în `AGENTS.md`. Pomenit în pitch, acest lucru răspunde direct cazului Samsung din
[ai-riscuri-evaluare-eu-ai-act.md](ai-riscuri-evaluare-eu-ai-act.md).
