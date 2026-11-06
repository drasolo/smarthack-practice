# Teme posibile de la PPC

Ce temă ar putea propune PPC. Tot ce e aici sunt ipoteze: tema reală se anunță la start.

Surse: documentul de pregătire din 3 noiembrie (ipotezele principale, după ce am citit prezentarea)
și o conversație anterioară despre firmă (lista de 50). Ultima verificare: 2026-11-06.

## Ipotezele principale

Când cele două liste se contrazic, are prioritate aceasta, pentru că e mai nouă și se bazează pe
[prezentarea PPC](surse/prezentare-ppc-ai-awareness.pptx).

| # | Ipoteză | Semnal | Probabilitate |
| --- | --- | --- | --- |
| 1 | Anomalii și contoare defecte pe datele de smart metering | Slide 6, Energy Anomaly Detection, 192M rânduri pe zi | Mare |
| 2 | Dashboard asistat de AI: întrebi datele în limbaj natural | Slide 6, Redshift în stack | Mare |
| 3 | Prognoză de consum sau producție, cu costul erorii în lei | Slide 4, proiectele 05 și 08, exemplul de pe slide 13 | Medie-mare |
| 4 | Flexibilitate: cât consum mută clienții în orele ieftine sau gratuite | Pilotul „Zero Active Electricity” | Medie |
| 5 | Agent LLM peste text sau documente: sesizări, PDF-uri, chatbot intern | ReClassAI, LegalRoute, Inverter Extractor, AgentHub | Medie |
| 6 | Mobilitate electrică: ocupare și planificarea încărcărilor | PPC Blue | Mică |

## Lista largă de 50 de teme

Probabilitatea este o estimare. Zona arată ce direcție pregătită acoperă tema: **A** prognoză și
flexibilitate, **B** rețea, **C** client, iar **gol** înseamnă că nu e acoperită.

### Piață și tranzacționare (PPC Energie, PPC Renewables)

| # | Temă | Probabilitate | Zonă |
| --- | --- | --- | --- |
| 1 | Prognoza prețului pentru ziua următoare (PZU) | Mare | A |
| 2 | Prognoza prețului intraday sau de dezechilibru | Medie | A |
| 3 | Optimizarea dispecerizării bateriilor | Mare | A |
| 4 | Prognoza producției eoliene sau solare pentru un parc | Mare | A |
| 5 | Prognoza consumului pentru portofoliul furnizorului | Mare | A |
| 6 | Reducerea costului de dezechilibru al furnizorului | Medie | A |
| 7 | Prezicerea orelor cu preț negativ și decizia de limitare a producției | Medie | A |
| 8 | Strategie de ofertare pentru un parc hibrid PV + baterie | Medie | A |
| 9 | Consilier pentru cumpărare forward sau spot | Mică | A |
| 10 | Optimizarea certificatelor verzi sau a garanțiilor de origine | Mică | A |

### Clienți (PPC Energie)

| # | Temă | Probabilitate | Zonă |
| --- | --- | --- | --- |
| 11 | Asistent AI pentru facturi și contracte | Mare | C |
| 12 | Explicarea facturilor, detectarea anomaliilor din facturi | Mare | C |
| 13 | Predicția pierderii clienților și retenție | Medie | C |
| 14 | Recomandări personalizate de oferte | Medie | C |
| 15 | Consilier pentru tarife dinamice la gospodării | Mare | A/C |
| 16 | Demand response, implicare în programul de ore gratuite | Mare | A |
| 17 | Consilier pentru prosumatori: dimensionare PV + baterie și amortizare | Mare | A/C |
| 18 | Coach de eficiență energetică pe curbe de sarcină | Medie | A/C |
| 19 | Clasificarea și direcționarea tichetelor de call center | Medie | C |
| 20 | Predicția riscului de plată, prioritizarea recuperării | Mică-medie | C |
| 21 | Analiza sentimentului clienților | Mică | C |
| 22 | Lead scoring pentru B2B (PV, e-mobility) | Mică | C |

### Rețea (Rețele Electrice)

| # | Temă | Probabilitate | Zonă |
| --- | --- | --- | --- |
| 23 | Predicția întreruperilor în funcție de vreme | Mare | B |
| 24 | Localizarea defectelor, triaj din apeluri și contoare | Medie | B |
| 25 | Optimizarea echipelor din teren | Medie | B |
| 26 | Gestionarea congestiilor în rețeaua de distribuție | Mare | B/A |
| 27 | Capacitatea rețelei pentru prosumatori, evaluarea cererilor de racordare | Mare | B |
| 28 | Automatizarea actelor de racordare (LLM pe documente) | Medie | B/C |
| 29 | Mentenanță predictivă pentru transformatoare | Medie | B |
| 30 | Digital twin pentru un fider de distribuție | Medie | B |
| 31 | Detectarea pierderilor netehnice sau a furtului | Medie | B |
| 32 | Calitatea datelor de contor, completarea golurilor (nowcasting) | Medie | B |
| 33 | Prioritizarea investițiilor în rețea | Mică | B |
| 34 | Probleme de tensiune și calitate a energiei cauzate de PV | Mică-medie | B |
| 35 | Inspecția liniilor și a vegetației cu drone și computer vision | Mică-medie | gol |
| 36 | Planificarea rezilienței la furtuni | Mică | B |

### Mobilitate electrică (PPC Blue)

| # | Temă | Probabilitate | Zonă |
| --- | --- | --- | --- |
| 37 | Prognoza cererii de încărcare, alegerea locațiilor | Medie | A |
| 38 | Programe de încărcare pentru flote sau primării | Medie | A |
| 39 | Predicția defectelor la încărcătoare | Mică | B |
| 40 | Coordonarea încărcării EV cu capacitatea rețelei | Mică-medie | A/B |

### Operarea regenerabilelor

| # | Temă | Probabilitate | Zonă |
| --- | --- | --- | --- |
| 41 | Mentenanță predictivă pentru parcuri eoliene sau solare (SCADA) | Medie | B |
| 42 | Detectarea defectelor panourilor solare din imagini | Mică | gol |
| 43 | Alegerea locațiilor pentru regenerabile sau baterii | Mică | A/B |

### Transversal și corporate

| # | Temă | Probabilitate | Zonă |
| --- | --- | --- | --- |
| 44 | Asistent cu agenți pentru procese interne | Medie | C |
| 45 | RAG peste reglementările ANRE, asistent de conformitate | Medie | C |
| 46 | Detecția anomaliilor de securitate în sistemele de control ale rețelei | Mică-medie | aproape gol |
| 47 | Raportare ESG / CO₂, urmărirea intensității de carbon | Mică-medie | A |
| 48 | Consum și flexibilitate pentru centre de date | Mică | A |
| 49 | Comunități de energie, platformă de partajare | Medie | A/C |
| 50 | Economisire de energie prin gamificare | Mică-medie | C |

## Ce nu acoperim

Golurile reale sunt computer vision (#35, #42) și securitatea sistemelor de control (#46). Asigurarea
ieftină este o oră de citit despre un model pre-antrenat de detecție a obiectelor (YOLO). Pentru
#46, modulul de anomalii acoperă cea mai mare parte a încadrării.
