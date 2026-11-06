# Idei de proiect

Ce am putea construi la eveniment și ce rămâne la fel oricare ar fi tema.

Surse: documentul de pregătire din 3 noiembrie și o conversație anterioară despre focalizare.
Ultima verificare: 2026-11-06.

## Starea deciziei

**Nu am ales încă proiectul final, pentru că tema se anunță la start.** Alegem la eveniment o idee
din 2-3 candidate. Brief-ul de practică din `CONTEXT.md` folosește triajul de contoare, dar el este
un exercițiu, nu alegerea finală.

Ideile care au șanse mari combină un model clasic care face munca grea cu un LLM care explică
rezultatul în română unui om care decide.

## Ideile

| Idee | Se leagă de | Partea ML | Partea LLM | Ce arătăm în demo |
| --- | --- | --- | --- | --- |
| Triaj contoare suspecte | Energy Anomaly Detection, slide 6 | Isolation Forest sau abateri de la profilul propriu; scor în kWh recuperabili | Fișă pentru inspector: ce e ciudat, de când, ce să verifice | Coadă ordonată după lei recuperabili; inspectorul aprobă sau respinge |
| Întreabă datele | „AI-assisted dashboards”, Redshift | Agregări în DuckDB | Text în SQL, doar citire, doar pe view-uri permise, cu SQL vizibil | Întrebare în română, grafic, SQL vizibil, refuz pe date nepermise |
| Costul erorii de prognoză | Proiectele 05 și 08, slide 4 | LightGBM cu meteo, calendar și valori anterioare; baseline sezonier | Explică de ce prognoza de mâine e mai mare | Eroarea transformată în lei cu prețuri PZU, comparată cu baseline-ul |
| Ore gratuite: cine se mută | Pilotul de ore gratuite | Participanți comparați cu clienți similari; scor de flexibilitate | Sfaturi personalizate | Cine merită invitat în faza 2 și cât consum s-a mutat |
| Triaj sesizări | ReClassAI | Baseline TF-IDF + regresie logistică | Clasifică, extrage adresa și urgența, propune un răspuns | Matrice de confuzie LLM vs baseline, coadă cu timer de SLA |
| Documente în tabel | LegalRoute, Inverter Extractor | Reguli de validare pe câmpuri | OCR și extragere în JSON după o schemă fixă | Fiecare câmp cu sursa și încrederea lui; omul corectează |

Tema se potrivește cu ideile astfel: [teme-posibile-ppc.md](teme-posibile-ppc.md). Partea comună de
evaluare și siguranță este în
[ai-riscuri-evaluare-eu-ai-act.md](ai-riscuri-evaluare-eu-ai-act.md).

## Motorul de decizie (variantă de rezervă)

O conversație anterioară propunea un singur proiect, adaptabil la temă: prognoză pentru mâine,
optimizator care alege acțiunile, explicație în limbaj simplu și un demo pe un singur ecran.

- **De ce e bună:** acoperă temele #1, #3, #4, #15-17 și #37-38 și are o cifră clară de prezentat:
  X lei pe an, Y% din maximul teoretic. Baza există în
  [backtest-ul PZU](pzu-piata-si-backtest-baterie.md).
- **Când o folosim:** dacă tema e de prognoză sau flexibilitate. Schimbăm datele de intrare și
  obiectivul optimizatorului, nu arhitectura.
- **Când renunțăm:** dacă tema nu se potrivește, de exemplu computer vision. Păstrăm doar obiceiurile:
  întâi baseline-ul, metrica în lei, un ecran clar.

Propunerea a fost făcută înainte de citirea prezentării PPC. Prezentarea a ridicat anomaliile pe
primul loc, de aceea aici apare ca rezervă. Nu există o decizie de echipă care să o excludă.

## Ce nu construim

Conversația a exclus RAG peste reglementările ANRE, digital twin, predicția pierderii clienților,
securitatea cibernetică, aplicația mobilă și fine-tuning-ul, pentru că fiecare costă mult și nu
schimbă scorul, dacă tema nu le cere explicit.
