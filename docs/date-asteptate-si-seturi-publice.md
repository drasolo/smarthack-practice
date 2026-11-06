# Date așteptate și seturi publice

Ce date am putea primi de la PPC, ce capcane verificăm în prima oră și ce seturi publice folosim
pentru exercițiu sau ca rezervă.

Surse: documentul de pregătire din 3 noiembrie. Coloanele sunt ipoteze: PPC nu a publicat datele.
Ultima verificare: 2026-11-06.

## Pe scurt (ipoteză)

Cel mai probabil primim un eșantion anonimizat de serii de timp la 15 minute, câteva mii de POD-uri,
nu 2 milioane, în CSV sau Parquet, plus meteo și calendar. Consumul unei gospodării este dată
personală, deci datele pot fi și sintetice.

Schema internă a repo-ului și regulile de acces la date sunt în `CONTEXT.md` și `AGENTS.md`.

## Ce am putea primi și ce verificăm

| Set de date | Coloane probabile | Capcane |
| --- | --- | --- |
| Citiri smart meter | POD anonim, timestamp, kWh activ (import, export la prosumatori), poate reactiv, regiune, tip client | Zile cu 92 sau 100 de intervale; UTC sau Europe/Bucharest; registru cumulativ sau consum pe interval; lipsă sau zero; duplicate; contor înlocuit |
| Etichete de fraudă sau defect | POD, data inspecției, rezultat | Foarte dezechilibrate; există doar pentru ce s-a inspectat |
| Producție eoliană sau solară | Parc, timestamp, MW, capacitate, disponibilitate, vânt, iradianță | Producția limitată arată ca vânt slab; pentru ziua următoare folosim prognoza meteo, nu vremea reală |
| Prețuri de piață | PZU, prețuri de dezechilibru | Trecerea PZU la 15 minute, vezi [pzu-piata-si-backtest-baterie.md](pzu-piata-si-backtest-baterie.md) |
| Meteo și calendar | Temperatură, vânt, iradianță, sărbători, vacanțe | Paștele ortodox se mută; 30 noiembrie și 1 decembrie |
| Sesizări (text) | Text în română, categoria aleasă, categoria corectă, dată, SLA | Fără diacritice, abrevieri, date personale în text |
| Documente | PDF-uri scanate | Calitatea OCR, tabele pe mai multe pagini |
| Încărcări EV | Stație, conector, kW, start, stop, kWh, locație | Sesiuni abandonate, stații offline |
| Facturi și plăți | Client, sumă, scadență, data plății | Date financiare personale, nu ies în API-uri externe |

## Seturi publice

| Set | Ce conține | Când îl folosim |
| --- | --- | --- |
| Smart meters in London (Kaggle) | Consum la 30 de minute pentru ~5.500 de gospodării, cu meteo | Anomalii, exercițiu de practică |
| ElectricityLoadDiagrams20112014 (UCI) | 370 de clienți la 15 minute, același pas ca la PPC | Prognoză de consum |
| SGCC electricity theft (State Grid, China) | Consum zilnic cu etichete de fraudă | Fraudă cu etichete |
| Wind Turbine SCADA (Kaggle) | Putere, vânt, curba teoretică | Prognoză sau defecte la parcuri eoliene |
| Open-Meteo | Meteo istoric, gratuit, fără cheie | Variabile meteo |
| Energy-Charts API (`bzn=RO`) | Prețuri PZU și producție pe surse; dă HTTP 429 după ~5 apeluri rapide | Prețuri, vezi backtest-ul |
