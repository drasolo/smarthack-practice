# PPC: companie și date

Cine este PPC în România, ce companii are și cum arată platforma lui de date.

Surse: [prezentarea PPC](surse/prezentare-ppc-ai-awareness.pptx), slide-urile 2-6; pentru pilotul
de ore gratuite, Balkan Green Energy News (8 mai 2026), preluat din documentul de pregătire, fără
reverificare. Ultima verificare: 2026-11-06.

## Pe scurt

PPC face parte din PPC Group și acoperă în România tot lanțul energiei: producție regenerabilă,
distribuție, furnizare și mobilitate electrică. Cel mai mare activ de date este platforma de
contorizare inteligentă, cu aproximativ 192 de milioane de rânduri pe zi.

PPC Group este prezent în Grecia (de unde provine și unde are sediul), România și Macedonia de
Nord. Obiectivul declarat este să devină liderul energiei curate din Europa de Sud-Est.

## Companiile din România

| Companie | Rol | Cifre din prezentare |
| --- | --- | --- |
| PPC Renewables Romania | Produce energie din surse regenerabile | 1,6 GW+ instalați, cel mai mare producător privat de regenerabile din România |
| Rețele Electrice Romania | Operează rețeaua de distribuție în Muntenia (cu București), Banat și Dobrogea | 136.000 km de linii, 293 de stații de transformare, 26.000+ posturi de transformare |
| PPC Energy | Vinde energie: contracte, facturi, suport | ~3 milioane de clienți, ~80 de magazine |
| PPC Blue Romania | Construiește și operează stații de încărcare | 1.100+ puncte, peste jumătate rapide sau ultra-rapide |

## Platforma de date

Platforma de smart metering este construită intern de PPC Digital Solutions.

| Indicator | Valoare |
| --- | --- |
| Puncte de măsurare (POD) active cu contor inteligent | 2 milioane+ |
| Citiri pe POD | 96 pe zi, una la 15 minute |
| Rânduri ingerate | ~192 de milioane pe zi |

| Etapă | Tehnologie |
| --- | --- |
| Colectare | Contoare inteligente și colectoare de date |
| Ingestie | Apache NiFi (streaming), Airflow (batch) |
| Stocare | Amazon S3, straturile Bronze și Silver |
| Procesare | Spark / PySpark pe AWS EMR |
| Rezultate | Dashboard-uri în Redshift, fluxuri Kafka spre furnizori |

Rezultatul anunțat de PPC: datele de consum ajung la furnizori în minute, nu în zile, o premieră în
distribuția de energie din România.

## Ce vrea PPC să facă în continuare

Slide-ul 6 numește trei direcții AI pentru platformă:

- detecția de anomalii în comportamentul contoarelor;
- monitorizarea predictivă a contoarelor defecte;
- dashboard-uri asistate de AI.

Slide-ul 4 adaugă motivul economic: energia se cumpără înainte să fie folosită, deci fiecare eroare
de prognoză costă bani reali.

## Pilotul de ore gratuite

PPC Energie a rulat pilotul „Zero Active Electricity” în iunie-septembrie 2026: aproximativ 70 de
ore gratuite pe lună pentru 5.000 de clienți cu contor inteligent. Rezultatele urmau să fie evaluate
după septembrie.

Proiectele AI existente sunt în [ppc-proiecte-ai.md](ppc-proiecte-ai.md).
