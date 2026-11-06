# Rețele Electrice: produse, date și teme probabile

Ce face distribuitorul din grupul PPC, ce date are și ce temă ar putea veni de aici.

Surse: comunicate și pagini Rețele Electrice, ANRE prin presă, articole din presa economică. Fiecare
fapt are linkul și data lui. Ultima verificare: 2026-11-06.

## Pe scurt

- Rețele Electrice are cel mai mare parc de contoare inteligente din România (2 milioane) și o
  platformă care trimite zilnic furnizorilor curbele de sarcină. Cifrele platformei sunt deja în
  [ppc-companie-si-date.md](ppc-companie-si-date.md).
- Construiește acum sistemele în care ar intra un model AI: AADMS (SCADA, DMS, OMS) și WFM din
  noiembrie 2025, apoi un GIS nou din aprilie 2026. Directorul general vorbește explicit de
  „algoritmi de inteligență artificială” pentru reziliența rețelei.
- Are trei dureri publice: furtul de energie (circa 700 de cazuri în două luni din 2026), prosumatorii
  pe care nu îi vede (bateriile despre care „habar n-avem”) și întreruperile (SAIDI național a crescut
  în 2025 pentru prima dată în ultimii ani).
- Cele mai probabile teme din zona asta: anomalii și pierderi pe datele de contor, vizibilitatea
  prosumatorilor, întreruperi. Detalii la final.

## Compania, în cifre noi

Cifrele din prezentarea PPC (136.000 km, 293 de stații, 26.000+ posturi) sunt în
[ppc-companie-si-date.md](ppc-companie-si-date.md). Aici sunt doar cele care lipsesc acolo.

| Fapt | Valoare | Sursă, dată |
| --- | --- | --- |
| Clienți deserviți | peste 3 milioane | [Our activity](https://www.reteleelectrice.ro/en/?p=18659), pagină fără dată, citită 2026-11-06 |
| Energie distribuită | peste 15 TWh pe an | aceeași pagină |
| Cotă din piața de distribuție | aproximativ o treime | [Business Forum](https://businessforum.ro/energy/20260403/retele-electrice-romania-to-invest-eur260-million-in-grid-modernisation-this-year-3062), 2026-04-03 |
| Investiții 2025 | ~1,4 mld. lei (~280 mil. euro) | Business Forum, 2026-04-03 |
| Plan de investiții 2026 | 1,3 mld. lei (~260 mil. euro), din care 821,3 mil. lei fonduri proprii | Business Forum, 2026-04-03 |
| Lucrări 2025 | ~1.000 de posturi de transformare noi, 440 modernizate, 303 km de linii MT noi | Business Forum, 2026-04-03 |

## Contorizare inteligentă

Sursa principală: [comunicatul din 17 martie 2025](https://reteleelectrice.ro/wp-content/uploads/comunicat-rer-program-smart-meter-2025.pdf).

| Fapt | Valoare |
| --- | --- |
| Contoare inteligente la final de 2025 | ~2 milioane (țintă în martie 2025; confirmat ca atins în [Business Forum, 2026-04-03](https://businessforum.ro/energy/20260403/retele-electrice-romania-to-invest-eur260-million-in-grid-modernisation-this-year-3062)) |
| Instalări planificate în 2025 | peste 174.000 |
| Acoperire la final de 2025 | 60% București, Ilfov, Giurgiu; peste 50% Banat; peste 60% Dobrogea |
| Citiri de la distanță în 2024 | ~1,5 milioane pe lună, în medie |
| Platforma pentru furnizori | lansată la finalul lui 2024, date de la peste 1,6 milioane de contoare, puse „zilnic” la dispoziția furnizorilor, cu curbe de sarcină |
| Calendarul de instalare | stabilit de ANRE din 2015 |

Directorul general, în același comunicat: contoarele permit „flexibilitatea și agregarea”,
integrarea producției descentralizate și a stocării, schimbarea furnizorului și reconectarea fără
deplasare.

## Calitatea serviciului: întreruperi

SAIDI este durata medie de întrerupere pe client, în minute pe an. SAIFI este numărul mediu de
întreruperi pe client. Valori pentru 2024, din [Our activity](https://www.reteleelectrice.ro/en/?p=18659):

| Regiune | SAIDI planificat | SAIDI neplanificat | SAIFI planificat | SAIFI neplanificat |
| --- | --- | --- | --- | --- |
| Muntenia | 36,6 | 74,62 | 0,18 | 2,29 |
| Banat | 183,55 | 95,14 | 0,72 | 2,3 |
| Dobrogea | 206,39 | 79,9 | 0,81 | 2,55 |

- Întreruperile neplanificate scad constant din 2019 în toate cele trei regiuni (Muntenia: de la
  142,8 la 74,62 minute).
- Întreruperile planificate sunt mari în Banat și Dobrogea, de 5-6 ori peste Muntenia.
- La nivel național, SAIDI a fost 236 de minute în 2025, față de 229 în 2024: prima creștere din
  ultimii ani. 145 de minute planificate, 91 neplanificate. Date ANRE, prin
  [Economica.net](https://www.economica.net/?p=961648), 2026-07-22. Valorile pe operator pentru
  Rețele Electrice nu apar în text.
- Întreruperile planificate se publică săptămânal, ca PDF, pe
  [reteleelectrice.ro](https://www.reteleelectrice.ro/en/outages/planned). Nu am găsit o hartă a
  avariilor sau o aplicație mobilă.

## Digitalizarea rețelei

| Proiect | Ce face | Valoare și durată | Sursă, dată |
| --- | --- | --- | --- |
| AADMS | Platformă integrată: SCADA, DMS/EMS (analiza și modelarea rețelei), OMS (gestiunea întreruperilor) | împreună cu WFM, peste 135 mil. lei; 2 ani; DMS/EMS din fonduri UE | [comunicat](https://www.reteleelectrice.ro/en/?p=24193), 2025-11-21 |
| WFM | Planificarea echipelor de operare și mentenanță | inclus mai sus | același comunicat |
| GIS & Topology | Topologia rețelei, date de teren prin aplicație mobilă, simulare, „starea de sănătate” a rețelei, schimb de date cu AADMS și cu sistemul de contorizare | până la 45 mil. lei; 17 luni de implementare | [comunicat](https://www.reteleelectrice.ro/en/?p=25728), 2026-04-06 |

Beneficii declarate pentru AADMS și WFM: intervenții mai rapide la întreruperi, durate mai mici ale
întreruperilor, integrarea regenerabilelor. Directorul general: sistemele vor permite folosirea
„algoritmilor de inteligență artificială” pentru o rețea rezilientă. Comunicatul nu vorbește de
prognoză.

## Prosumatori

| Fapt | Valoare | Sursă, dată |
| --- | --- | --- |
| Prosumatori în România, 30 iunie 2026 | 359.378 (324.535 persoane fizice, 34.843 juridice) | ANRE, prin [StartupCafe](https://startupcafe.ro/romani-panouri-solare-cati-prosumatori-racordare-retelele-electrice-romania-105065), 2026-08-13 |
| Putere instalată | 4.019 MW | aceeași sursă |
| Prosumatori cu baterii | 127.084 | aceeași sursă |
| Prosumatori noi la Rețele Electrice în 2024 | ~30.000; ~60.000 estimați pentru 2025 | Mihai Pește, director general, prin [Economica.net](https://www.economica.net/prosumatori-retea-date-control_809199.html), 2025-02-09 |

Ce a spus directorul general la aceeași conferință (2025-02-09):

- Distribuitorul are nevoie de „datele de invertor, datele de producție, datele de măsură” ca să
  vadă congestiile și să prognozeze.
- Despre multe baterii deja instalate „habar n-avem”. Le observă doar din forma curbelor de
  producție.
- Agregarea și flexibilitatea nu se pot dezvolta „fără aceste date”.
- Asociația prosumatorilor a numit propunerea „un control abuziv”.

Nu am găsit numărul de prosumatori din aria Rețele Electrice pentru 2026.

## Pierderi și furt de energie

- Rețele Electrice a găsit circa 700 de cazuri de furt în primele două luni din 2026. Sesizările
  vin și printr-un formular online. Sursa: [Financiarul](https://financiarul.ro/economie/peste-8-000-de-cazuri-de-furt-de-energie-in-2025-cu-prejudicii-de-zeci-de-milioane-lei/), 2026-03-25.
- În reglementarea ANRE, consumul fraudulos intră la pierderi în rețea, deci în tarif, și îl plătesc
  toți clienții (aceeași sursă).
- La concurență, DEER detectează furtul cu analiza consumului și cu contorizarea inteligentă, iar
  Distribuție Oltenia a făcut peste 21.000 de verificări în 2025 (aceeași sursă). Ipoteză:
  Rețele Electrice face ceva asemănător, dar nu am găsit o sursă.
- Nu am găsit procentul oficial de pierderi (CPT) pentru Rețele Electrice.

## Sesizări de la clienți

ReClassAI, modelul care reclasifică sesizările de pe site, este deja descris în
[ppc-proiecte-ai.md](ppc-proiecte-ai.md).

## Ce se contrazice

- Lungimea rețelei: 134.000 km pe [Our activity](https://www.reteleelectrice.ro/en/?p=18659) și în
  [Economica.net](https://www.economica.net/prosumatori-retea-date-control_809199.html)
  (2025-02-09), 136.000 km în prezentarea PPC și în Business Forum (2026-04-03). Probabil cifra
  nouă e 136.000.
- Viteza datelor către furnizori: „în minute” în prezentarea PPC, „zilnic” în comunicatul din martie
  2025. Ipoteză: s-a trecut la streaming (Kafka) după martie 2025.

## Ce date ar putea da PPC din zona asta

Ipoteze, deduse din sistemele de mai sus. Schema citirilor de contor e în
[date-asteptate-si-seturi-publice.md](date-asteptate-si-seturi-publice.md).

| Date | De unde | La ce folosesc |
| --- | --- | --- |
| Curbe de sarcină la 15 minute, import și export la prosumatori | platforma de contorizare | anomalii, furt, prosumatori nedeclarați |
| Evenimente de contor: citiri lipsă, alarme, deconectări | sistemul de contorizare | contoare defecte, calitatea datelor |
| Legătura contor, post de transformare, fider | GIS | bilanț pe post, deci pierderi; congestii |
| Întreruperi cu cauză, durată și clienți afectați | OMS | prognoza întreruperilor, SAIDI |
| Cazuri de furt confirmate la inspecție | inspecții | etichete pentru un model supervizat |
| Sesizări text de la clienți | site, ReClassAI | triaj, rezumate |
| Meteo | public | întreruperi, producție PV |

## Trei teme probabile

1. **Anomalii și pierderi netehnice pe datele de contor.** Este exact direcția de pe slide-ul 6
   (anomalii, contoare defecte). Furtul ajunge în tarif și generează sute de cazuri pe lună. Pot
   exista etichete din inspecții. Se potrivește cu ce construim deja.
2. **Prosumatorii pe care rețeaua nu îi vede.** Detectarea PV și a bateriilor din curbele de
   contor, prognoza injecției pe post de transformare, avertizare de congestie. Motiv: directorul
   general a spus public că nu are aceste date, iar prosumatorii au 4 GW și 127.000 de baterii la
   nivel național.
3. **Întreruperi: prognoză și triaj.** Risc de întrerupere din meteo și istoricul OMS, localizarea
   defectului din contoarele care tac, prioritizarea echipelor. Motiv: AADMS, OMS și WFM sunt în
   implementare și menționează AI, iar SAIDI național a crescut în 2025.
