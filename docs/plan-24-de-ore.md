# Planul celor 24 de ore

Fazele evenimentului, ce trebuie să fie gata la fiecare poartă și ce facem dacă rămânem în urmă.

Surse: documentul de pregătire din 3 noiembrie. Este planul nostru, nu programul oficial, care e în
[eveniment-si-regulament.md](eveniment-si-regulament.md). H0 este start coding, sâmbătă la 12:00.
Ultima verificare: 2026-11-06.

## Regula principală

**La H10 (sâmbătă, 22:00), demo-ul trebuie să meargă cap-coadă, oricât de urât.** Dacă nu merge, tăiem din idee
până merge. Tot ce urmează se construiește peste o variantă funcțională.

## Fazele

| Ore | Când | Fază | Ce facem | Poartă la final |
| --- | --- | --- | --- | --- |
| H0-H2 | Sâm 12:00-14:00 | Înțelegem problema | Tema și criteriile, deschidem datele, întrebăm mentorii, alegem o idee din 2-3 | Idee aleasă, problema într-o frază cu o cifră PPC |
| H2-H3 | Sâm 14:00-15:00 | Contractul | Repo, schema datelor, JSON-ul endpoint-urilor, mock-uri | Fiecare rulează partea lui pe mock-uri |
| H3-H10 | Sâm 15:00-22:00 | Prima felie cap-coadă | Date reale, baseline, API, un ecran. Sincronizare de 5 minute la H6 și H9 | **Demo cap-coadă pe date reale** |
| H10-H16 | Sâm 22:00 - Dum 4:00 | Îmbunătățim | Model mai bun, explicație LLM, guardrails, tabel de evaluare. Somn pe rând, câte 2 ore, mereu cel puțin doi treji | Fără funcționalități noi |
| H16-H20 | Dum 4:00-8:00 | Lustruim | Bug-uri, UI, 5 încercări de prompt injection, README cu ce am pregătit dinainte, video de rezervă | Fără cod nou, video înregistrat |
| H20-H24 | Dum 8:00-12:00 | Pitch-ul | Slide-uri, două repetiții cronometrate, întrebări probabile și cine răspunde la fiecare | Gata de prezentat |

## În primele 2 ore, cu mentorii PPC

Întrebările sunt în [intrebari-deschise.md](intrebari-deschise.md). Trebuie să aflăm ce metrică
contează, ce înseamnă fiecare coloană, cine ar folosi soluția și dacă datele au voie să iasă spre un
API extern.

## Dacă datele nu au voie să iasă

Datele brute stau în afara repo-ului, iar agenții primesc doar schema și rânduri sintetice. Regulile
sunt în `AGENTS.md`. Pomenit în pitch, acest lucru răspunde direct cazului Samsung din
[ai-riscuri-evaluare-eu-ai-act.md](ai-riscuri-evaluare-eu-ai-act.md).
