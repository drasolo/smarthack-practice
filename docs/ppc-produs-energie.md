# PPC Energie: oferte, myPPC, tarife dinamice și pilotul de ore gratuite

Ce produse are PPC Energie pentru clienții cu contor inteligent, ce date produc ele și ce ar putea
cere PPC pe baza lor. Cifrele companiei sunt în [ppc-companie-si-date.md](ppc-companie-si-date.md).

Surse: comunicate PPC Energie, pagina ofertei PPC MaxControl și presă economică, cu URL și dată la
fiecare fapt. Scris de agentul lui Alex și verificat de agentul lui Dragoș. Ultima verificare:
2026-11-06.

## Pe scurt

- PPC Energie vinde deja energie cu preț pe interval orar: Ore Smart (august 2025), Ore Smart+
  (martie 2026), Ore Smart PRO pentru firme mici (septembrie 2026) și PPC MaxControl pentru
  prosumatori, cu preț PZU pe fiecare 15 minute (2026).
- Pilotul se numește oficial „Energie Electrică Activă Zero”. După primele șase intervale, 83% din
  locuri și-au schimbat consumul, iar consumul în orele gratuite a crescut cu 28,6%. Nu am găsit
  un bilanț final după septembrie.
- Toate aceste produse au nevoie de contor inteligent integrat în sistemul de contorizare. Asta
  leagă produsele de vânzare de platforma de date de la Rețele Electrice.
- myPPC are deja un modul de recomandări de eficiență („myEnergy Coach”), alerte și raport lunar
  pentru prosumatori. Un asistent AI peste factură și consum ar avea unde să intre.

## Tarife dinamice

| Ofertă | Când e ieftin | Preț activ (fără taxe) ieftin / restul | Final București, cu taxe | Sursă și dată |
| --- | --- | --- | --- | --- |
| PPC Ore Smart | 11:00-14:59, martie-octombrie | 0,313 / 0,767 lei/kWh (−59%) | 0,89 / 1,44 lei/kWh | [Economedia](https://economedia.ro/ppc-lanseaza-prima-oferta-dinamica-din-romania-prin-care-consumatorii-pot-plati-un-pret-cu-59-mai-mic-daca-consuma-in-momentele-de-varf-ale-productiei-regenerabile.html), 2025-08-06 |
| PPC Ore Smart+ | Nopțile de luni până vineri 00:00-05:59, tot weekendul, 11:00-14:59 în martie-octombrie | 0,348 / 0,823 lei/kWh | 0,98 / 1,56 lei/kWh | [Știri Craiova](https://stiricraiova.ro/2026/03/19/ppc-energie-lanseaza-o-oferta-cu-tarif-dinamic-ppc-ore-smart-cu-preturi-reduse-la-energie-in-week-end-si-pe-timp-de-noapte/), 2026-03-19; [comunicat PPC](https://www.ppcenergy.ro/wp-content/uploads/Comunicat-de-presa-PPC-Energie-lanseaza-noua-oferta-PPC-Ore-Smart-.pdf) |
| PPC Ore Smart PRO | Firme cu consum sub 200.000 kWh pe an și contor inteligent, fără prosumatori. Tot weekendul; în zilele lucrătoare din martie-octombrie, 00:00-05:59 și 11:00-14:59 | nepublicat în sursă | 1,00-1,09 / 1,65-1,73 lei/kWh, după zona de distribuție | [Economedia](https://economedia.ro/?p=370922), 2026-09-10 |

Exemplul PPC pentru Ore Smart+: o gospodărie cu 300 kWh pe lună care mută 75 kWh în intervalele
ieftine economisește cam 580 lei pe an.

Singura cifră publică despre comportament, raportată de PPC: în august 2026, aproximativ 22% din
clienții casnici Ore Smart+ și-au redus ponderea consumului între 20:00 și 23:00, față de alte două luni de vară și o lună de
iarnă ([Economedia](https://economedia.ro/?p=370922), 2026-09-10). Numărul de clienți pe aceste
oferte nu e public.

Ipoteză: PPC folosește deja curbele la 15 minute ale clienților Ore Smart ca să măsoare cât consum
se mută. Asta e exact întrebarea din tema 4 din [teme-posibile-ppc.md](teme-posibile-ppc.md).

## Pilotul „Energie Electrică Activă Zero”

| Fapt | Valoare | Sursă și dată |
| --- | --- | --- |
| Înscriere | Primii 5.000 de clienți eligibili, 7-20 mai 2026 | [Forbes România](https://www.forbes.ro/?p=500324); [comunicat PPC](https://www.ppcenergy.ro/wp-content/uploads/Comunicat-de-presa-PPC-Energie-lanseaza-intervale-de-consum-cu-energie-activa-la-cost-zero.pdf) |
| Perioadă | Iunie-septembrie 2026, circa 70 de ore pe lună | Aceleași |
| Anunțarea intervalelor | Cu cel puțin 12 ore înainte, prin e-mail și myPPC | [Economica.net](https://www.economica.net/anunt-de-la-ppc-ce-s-a-intamplat-cu-clientii-care-au-primit-energie-activa-la-zero-lei-kwh_952038.html/amp), 2026-06-19 |
| Primele șase intervale (iunie) | ~71 MWh consumați la 0 lei | Același |
| Câți au reacționat | ~4.193 de locuri de consum, peste 83%, și-au schimbat obiceiurile | Același |
| Cât au crescut consumul | +28,6% în intervalele gratuite, față de aceleași intervale și zile din mai | Același |
| Câți au deschis notificările | ~78% | Același |
| Valoarea bonusului | ~61.000 lei pentru prima jumătate a lui iunie, pe factură ca „Bonus Campanie Energie Activă Zero” | Același |
| Exemplu de interval | 19 iunie 2026, 11:00-17:00 | Același |

Nu am găsit un bilanț după încheierea pilotului. Comparația cu luna mai e o bază simplă: nu ține
cont de vreme sau de sezon. Ipoteză: PPC ar vrea o măsurare mai bună a efectului (grup de control,
bază pe vreme), iar asta e o problemă bună pentru un hackathon.

## Oferte pentru prosumatori

| Produs | Ce face | Sursă și dată |
| --- | --- | --- |
| PPC MaxControl | Consumul și energia livrată în rețea se plătesc la prețul PZU pe fiecare interval de 15 minute, minus componenta TG. Soldul se plătește la 30 de zile, nu la 24 de luni. Prețul la injecție nu scade sub 0 lei/kWh, iar consumul nu se facturează peste 0,999 lei/kWh. Raport lunar cu recomandări și fișier Excel cu consum, injecție și preț la 15 minute, notificare săptămânală cu prețuri. Cere contor inteligent și cel mult 200 kW | [ppcenergy.ro](https://www.ppcenergy.ro/prosumatori/clienti-rezidentiali/ppc-maxcontrol/), ofertă valabilă până la 2026-11-30; lansare raportată pe 2026-07-15 de [Știri Craiova](https://stiricraiova.ro/2026/07/15/ppc-energie-lanseaza-ppc-maxcontrol-oferta-pentru-prosumatori-cu-plata-soldului-la-30-de-zile-si-protectie-impotriva-preturilor-negative/) |
| Baterii pentru prosumatori | 5, 10 sau 15 kWh, pentru invertoare hibride Huawei și Deye, de la 299 lei pe lună | [The Diplomat](https://www.thediplomat.ro/2026/05/13/ppc-energy-expands-its-portfolio-of-solutions-for-prosumers-with-storage-systems/), 2026-05-13 |
| PPC Solar Upgrade | Pentru sisteme fără invertor hibrid; de la 599 lei pe lună, cel mult 36 de rate pe factură | Același |

Pagina MaxControl spune că o baterie crește autoconsumul la 55-65%, față de 15-25% fără. La
contoarele orare, consumul se împarte egal pe cele patru intervale de 15 minute, deci o curbă la 15
minute poate fi de fapt orară. Pagina are și o eroare: dă media PZU 2025 ca „545,17 lei/kWh”, foarte probabil lei/MWh.

## myPPC

Noua versiune a apărut în iulie 2026, pe web și mobil
([Capital](https://www.capital.ro/un-anunt-important-pentru-clientii-ppc-aplicatia-folosita-pentru-facturi-si-index-va-fi-schimbata.html),
2026-07-16).

- Facturi, plată cu confirmare imediată, index, consum, documente de contract.
- Mai multe locuri de consum într-un cont, separat pentru casă și firmă.
- Alerte pentru facturi, scadențe și perioade de citire, pe e-mail sau în aplicație.
- Formular de contact cu tipuri de cerere predefinite.
- PPC myRewards (reduceri) și PPC myEnergy Coach (recomandări personalizate de eficiență).

Pentru întrebări despre facturi, PPC are și un agent vocal, descris în
[ppc-produs-ai-date.md](ppc-produs-ai-date.md).

## Ce date ar putea da PPC

Ipoteze, din produsele de mai sus:

| Date | Din ce produs |
| --- | --- |
| Curbe de consum la 15 minute pentru clienți cu tarif dinamic, cu eticheta ofertei | Ore Smart, Ore Smart+, Ore Smart PRO |
| Intervalele gratuite anunțate, cine a deschis notificarea și consumul înainte și după | Pilotul Energie Electrică Activă Zero |
| Consum și injecție la 15 minute pentru prosumatori, cu prețul PZU pe interval | PPC MaxControl |
| Linii de factură, tipuri de cerere din formularul de contact, recomandări myEnergy Coach | myPPC |

## Trei teme probabile

1. **Cât consum mută clienții și cât valorează.** PPC a rulat un pilot cu 5.000 de clienți și are
   trei oferte cu preț pe interval, dar publică doar o comparație simplă cu luna anterioară. O
   măsurare corectă a efectului, cu grup de control și ajustare pentru vreme, se poate face într-o
   zi pe curbe la 15 minute.
2. **Recomandări personale de tarif și de program de consum.** Fiecare ofertă are un exemplu de
   economie, MaxControl promite recomandări lunare, iar myEnergy Coach există deja. Un model care
   spune fiecărui client ce ofertă i se potrivește și când să consume se poate arăta live.
3. **Prosumatorul cu baterie la preț PZU.** MaxControl, bateriile și PPC Solar Upgrade sunt
   lansate toate în 2026. Când să încarci și să descarci bateria la preț pe 15 minute leagă
   produsul de [pzu-piata-si-backtest-baterie.md](pzu-piata-si-backtest-baterie.md).
