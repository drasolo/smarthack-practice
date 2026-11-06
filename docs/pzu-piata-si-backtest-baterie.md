# PZU: piața și backtest-ul cu baterie

Ce este PZU, cum funcționează și ce a arătat backtest-ul nostru pe prețuri reale.

Surse: o conversație anterioară pentru descrierea pieței, nereverificată pe site-ul OPCOM, și
`results_real/results.json` din proiectul local `ro-bess-forecast` de pe laptopul lui Dragoș. Ultima
verificare: 2026-11-06.

## Pe scurt

PZU (Piața Zilnică Unică) este piața din România pentru energia de a doua zi, operată de OPCOM. Pe
prețuri reale, modelul nostru a captat 72,7% din profitul maxim teoretic, dar un profil mediu simplu
a ajuns foarte aproape, la 72,0%.

## Cum funcționează

- Ofertele pentru ziua D se depun până la 12:00 CET în ziua D-1.
- Licitația stabilește un preț pentru fiecare interval de 15 minute, 96 pe zi, de la 1 octombrie 2025.
- România este cuplată prin SDAC, deci prețul depinde de cerere și ofertă în toată regiunea cuplată.
- După PZU urmează piața intraday și piețele de echilibrare. Costurile de dezechilibru apar când
  poziția din ziua precedentă este greșită.
- Forma zilei: vârf seara, scădere la prânz din cauza solarului, prețuri negative primăvara și vara.

Date: OPCOM și ENTSO-E publică prețurile, iar Energy-Charts le oferă prin API.

## Ce testează backtest-ul

Prognozăm cele 96 de prețuri de mâine, programăm o baterie pe baza prognozei, apoi calculăm profitul
la prețurile reale. Prognoza vede doar prețurile până în D-1 și prognozele meteo.

| Parametru | Valoare |
| --- | --- |
| Baterie | 4,47 MW / 8,94 MWh, dimensionată după stocarea PPC Renewables de la Colibași |
| Randament dus-întors | 88% |
| Stare de încărcare | 5-95% |
| Cost de uzură | 10 EUR/MWh |
| Curs folosit | 5 lei/EUR |
| Perioadă de test | 1 octombrie 2025 - 30 octombrie 2026 |
| Prețuri | Reale, din Energy-Charts |

## Rezultate pe prețuri reale

| Strategie | Lei pe an | % din maxim | MAE (EUR/MWh) |
| --- | --- | --- | --- |
| Previziune perfectă | 2.480.581 | 100% | n/a |
| LightGBM | 1.802.983 | 72,7% | 25,3 |
| Profil mediu pe 28 de zile | 1.786.356 | 72,0% | 35,1 |
| Baseline sezonier | 1.630.268 | 65,7% | 29,5 |

Sumele sunt anualizate. Modelul LightGBM face aproximativ 598 de cicluri pe an.

## Ce înseamnă

- LightGBM are cu 10,6% mai mult profit decât baseline-ul sezonier.
- Profilul mediu are o eroare mai mare, dar aproape același profit. Pentru o baterie de 2 ore, banii
  sunt în forma zilei, nu în eroarea medie.
- De aceea nu prezentăm „MAE mai mic”. Ținta este restul de 27,3% până la maxim: serile cu vârfuri,
  variațiile de la prânz și orele cu preț negativ.
- Prima versiune, pe prețuri sintetice, a dat 85,1%. Nu o cităm, pentru că prețurile reale sunt mai
  greu de prezis.

## Dacă tema este de piață

Nu pierde timp cu designul pieței. Învață regula de închidere și trecerea la 15 minute, apoi lucrează
la lanțul prognoză-decizie și la indicatorul „% din maxim”.
