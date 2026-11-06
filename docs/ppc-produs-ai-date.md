# PPC: AI și date, din surse publice

Ce spun sursele publice despre echipele de AI și date ale PPC România, proiectele lor, joburile și
concursurile la care PPC a dat probleme. Completează [ppc-proiecte-ai.md](ppc-proiecte-ai.md) și
[ppc-companie-si-date.md](ppc-companie-si-date.md), care vin din prezentarea PPC.

Surse: anunțuri de angajare, presă și pagini de evenimente, cu URL și dată la fiecare fapt. Scris
de agentul lui Alex și verificat de agentul lui Dragoș; ce nu s-a putut confirma e marcat. Ultima
verificare: 2026-11-06.

## Pe scurt

- Stack-ul din prezentare se confirmă public: anunțurile de ML ale PPC cer AWS (SageMaker, EMR,
  Redshift, S3), Spark, Airflow și MLflow. Nimic despre LLM-uri în anunțuri.
- Sursele publice descriu doi agenți AI făcuți cu startup-uri, pentru clienți și juriști: un agent
  vocal pentru facturi (Wonderful) și RecovIA pentru dosarele de recuperare (3X7AI).
- La singurul hackathon public găsit cu probleme atribuite și PPC (CleanTech, mai 2025), temele au fost
  congestie, prosumatori, agenți AI, prognoză pe joasă tensiune, digital twin, drone și securitate.
- Bursele PPC Renewables din 2026 cer prognoză de consum, prognoză de producție, indicatori din
  date brute și simulare de tranzacționare. Asta e cea mai recentă listă de teme scrisă de PPC.

## Cine face AI și date la PPC România

| Fapt | Sursă și dată |
| --- | --- |
| Echipa de ML se numește „Digital Solutions” sau „Global Digital Solutions” și angajează sub PPC Energy Services, București, hibrid | [Middle ML Engineer](https://www.undelucram.ro/ro/locuri-de-munca/middle-machine-learning-engineer/100199), publicat 2026-09-09; [Junior ML Engineer](https://www.undelucram.ro/ro/locuri-de-munca/junior-machine-learning-engineer/100358), publicat 2026-09-15 |
| Stack ML: Python, TensorFlow, PyTorch, scikit-learn, SageMaker, Spark pe EMR, Redshift, S3, Airflow, MLflow, CI/CD | Aceleași anunțuri |
| Juniorul trebuie să înțeleagă și „generative AI”; middle-ul nu are nimic despre LLM | Aceleași anunțuri |
| Platforma unică de date de contorizare pentru RER, prezentată la DevTalks de un BI Developer și un Data Engineer PPC: date din surse eterogene, standardizate în AVRO, validare automată și recuperare a istoricului, citiri aproape în timp real pentru toți furnizorii | [DevTalks 2026](https://www.devtalks.ro/speakers/765-anda-spataru), talk pe 2026-06-03 |
| PPC mai angajează Data Engineer (1-5 ani) în București | [hipo.ro](https://www.hipo.ro/locuri-de-munca/locuri_de_munca/273559/), dată neafișată în rezultat |

Ipoteză: talkul DevTalks descrie aceeași platformă ca slide-ul 6 din prezentare. Ce aduce nou:
datele vin din mai multe surse care nu se potrivesc, iar calitatea se repară automat. Asta susține
tema „calitatea datelor de contor” (#32 din [teme-posibile-ppc.md](teme-posibile-ppc.md)).

## Proiecte AI care nu sunt în prezentare

| Proiect | Ce face | Cifre | Sursă și dată |
| --- | --- | --- | --- |
| Agent vocal PPC Energie (cu Wonderful) | Răspunde la întrebări despre facturi și modalități de plată, înregistrează dovezi de plată; legat de sistemele de facturare, contracte și IVR | Titlul spune -75% la timpul de apel, în 4 săptămâni. Un angajat Wonderful dă pe LinkedIn: de la 6 min la 90 s, 77% „containment”, 91% feedback pozitiv | [Wonderful, studiu de caz](https://www.wonderful.ai/blog-articles/ppc-energie), datat 2026-05-15 în pagină. La verificare am putut citi doar titlul; cifrele sunt de la vânzător și nu le cităm ca fapte |
| RecovIA (cu startup-ul 3X7AI) | Pregătește un dosar de recuperare a creanțelor: verifică actele, alege instanța, generează cererile. Autorul notează „sub 2 minute”; nu am putut confirma | Locul 2 la FT Innovative Lawyers Awards Europe 2026, categoria In-house, Digital Solutions, 24 din 27 de puncte, ceremonie pe 2026-09-24 | [Profit.ro](https://profit.ro/legal/ppc-romania-locul-2-la-financial-times-innovative-lawyers-awards-europe-2026-recovia-solutia-ai-care-duce-inovatia-juridica-romaneasca-pe-scena-europeana-22789183), 2026. Premiul e confirmat prin rezumate de căutare, nu prin pagina completă sau de FT |

Ipoteze:

- Agentul vocal Wonderful e fie proiectul 06 „AI Claims Agent” din prezentare, fie un proiect
  vecin. Prezentarea îl dă în DEV și pentru restanțe; Wonderful descrie un agent în producție pentru
  întrebări despre facturi. Nu știm care e relația.
- RecovIA e pe același flux ca LegalRoute (documente juridice), dar face altceva: generează actele,
  nu doar le clasifică.
- Ambele arată un tipar: PPC cumpără sau co-dezvoltă agenți LLM cu startup-uri și îi măsoară pe
  timp economisit. Un proiect de hackathon cu LLM ar trebui să arate același tip de cifră.

## Concursuri și programe pentru studenți

### CleanTech Hackathon 2025

Organizat de Techcelerator la Energy Expo, 23-24 mai 2025, cu sprijinul Ministerului Energiei și
al PPC România. Pentru startup-uri, nu pentru studenți. StartupCafe numește PPC doar ca susținător,
iar altă publicație de startup-uri atribuie problemele și PPC, Delgaz și Romgaz. Nicio sursă nu spune
care problemă e a cui.
Surse: [StartupCafe, anunț](https://startupcafe.ro/inscrieri-2025-cele-9-provocari-ale-competitiei-cleantech-hackathon-cu-premii-totale-de-22-000-eur-pentru-startup-uri-romanesti-de-solutii-ai-pentru-energie-81133)
(2025-05-15), [StartupCafe, câștigători](https://startupcafe.ro/castigatori-competitie-startup-solutii-sector-energie-sustenabila-cleantech-hackathon-2025-81716)
(2025-05-29).

| # | Problemă |
| --- | --- |
| 1 | Managementul inteligent al congestiei în rețelele de distribuție |
| 2 | Platforme care integrează datele din fluxurile de energie ale prosumatorilor |
| 3 | Platforme prin care clienții co-investesc în regenerabile |
| 4 | Optimizarea rețelelor urbane de stații de încărcare prin modelare predictivă |
| 5 | Digital twin pentru mentenanță predictivă și securitate cibernetică |
| 6 | AI și agentic AI cu platforme integrate de management (guvernanța datelor, documente, acțiuni corective, acces) |
| 7 | Drone și software pentru automatizarea inspecțiilor |
| 8 | Estimarea consumului și a producției pe joasă tensiune cu AI |
| 9 | SecOps cu AI pentru infrastructura energetică, OT și IT |

Câștigători: YellowGrid (locul 1, managementul energiei pentru prosumatori, cu vânzarea surplusului
la preț de piață), WiseWatts (copilot AI pentru optimizarea consumului), Procesio (automatizare de
procese și extragere de date din documente cu LLM). 130 de înscriși, 30 de soluții, 14 echipe
finaliste. Ordinea locurilor 2 și 3 diferă între surse; StartupCafe dă WiseWatts pe 2 și Procesio pe 3.

### Burse PPC Renewables

| Program | Teme | Sursă și dată |
| --- | --- | --- |
| Burse pentru licență la ASE CSIE, 4 × 1.000 lei pe lună, noiembrie 2026 - iulie 2027 | Prognoza consumului; prognoza producției; „GreenGrid Insights” (indicatori de performanță verde din date brute); „PowerTrade Analytics” (analiză și simulare pentru tranzacționare) | [Economedia](https://economedia.ro/?p=366566), 2026-08-14 |
| Laborator IoT la Automatică și Calculatoare (UPB) și 8 burse pe an | Proiecte de digitalizare în energie | [Comunicat PPC Renewables](https://www.ppcenergy.ro/wp-content/uploads/comunicat-presa-ppc-renewables-romania-laborator-politehnica.pdf), 2026 după Economedia |

Nu am găsit niciun hackathon pentru studenți organizat de PPC România înainte de SmartHack 2026.

## Ce date ar putea da PPC

Ipoteze, din ce apare public:

| Date | De ce credem asta |
| --- | --- |
| Curbe de consum la 15 minute, eventual cu goluri și surse care nu se potrivesc | Platforma de contorizare e produsul de date despre care PPC vorbește cel mai mult (prezentare, DevTalks) |
| Serii de producție eoliană sau solară cu meteo | Temele de bursă PPC Renewables și proiectul 08 |
| Transcrieri de apeluri sau texte de facturi și contracte | Agentul vocal și RecovIA arată că PPC are fluxuri de text și voce etichetate pe intenții |
| Prețuri PZU și volume de tranzacționare | Tema de bursă „PowerTrade Analytics” |

Toate ar fi probabil sintetice sau anonimizate, pentru că anunțurile și talkurile nu arată nicio
deschidere publică a datelor.

## Trei teme probabile

1. **Prognoză de consum sau producție pe 15 minute, cu costul erorii.** PPC a scris-o explicit
   în bursele din august 2026, e problema 8 de la CleanTech și are două proiecte în prezentare.
   Echipa de ML lucrează exact pe stack-ul pentru asta.
2. **Calitatea și anomaliile datelor de contorizare.** Platforma de contorizare e mândria echipei
   de date (talk DevTalks, slide-ul 6), iar validarea automată e deja o problemă recunoscută.
3. **Agent LLM care economisește timp de operator sau de jurist.** Sursele publice descriu doi
   astfel de agenți, prezentați cu cifre de timp economisit. Un agent peste facturi,
   sesizări sau documente ar continua tiparul. Probabilitate mai mică decât primele două, pentru că
   anunțurile de ML nu cer LLM-uri.
