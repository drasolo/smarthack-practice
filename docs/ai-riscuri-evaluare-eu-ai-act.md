# AI: riscuri, evaluare și EU AI Act

Ce riscuri AI subliniază PPC, cum le putem arăta rezolvate în demo și ce spune EU AI Act.

Surse: [prezentarea PPC](surse/prezentare-ppc-ai-awareness.pptx), slide-urile 19-30, și documentul
de pregătire pentru interpretarea Anexei III. Cifrele și datele legale vin din prezentare și nu sunt
reverificate. Ce scrie aici nu e consultanță juridică. Ultima verificare: 2026-11-06.

## Pe scurt

Aproape jumătate din prezentare vorbește despre riscuri, deci ipoteza noastră este că juriul PPC va
întreba cum am evaluat și cum am securizat soluția. Răspunsul trebuie să se vadă în demo, nu doar pe
slide-uri.

## Limitări și riscuri (slide-urile 19-20)

| Risc | Ce înseamnă | Soluții |
| --- | --- | --- |
| Confabulație | Modelul produce informații fluente, dar false | RAG, citarea surselor, evaluare de factualitate |
| Bias | Preia stereotipuri din datele de antrenare | Măsurarea diferențelor între grupuri |
| Limite de context | Intrările lungi sunt trunchiate, cunoștințele pot fi vechi | RAG, fragmentare |
| Expunere de securitate | Prompt injection și scurgeri de date | Controalele de mai jos |
| Automation bias | Oamenii au prea multă încredere în output | Verificare umană, încredere afișată în UI |

Modelul primește text și produce text. Pentru acțiuni are nevoie de tool use cu limite stricte, iar
pentru stil și format specific se poate folosi fine-tuning.

## Atacuri și controale (slide-ul 21)

- **Prompt injection directă:** utilizatorul păcălește modelul să ocolească regulile.
- **Prompt injection indirectă:** instrucțiuni ascunse în conținutul citit de model, de exemplu un
  e-mail sau o pagină web.
- **Scurgeri de date:** date personale sau secrete ajung în antrenare sau în prompturi și pot fi
  extrase.
- **Lipsa controlului de acces în RAG:** modelul rezumă documente pe care utilizatorul nu are voie
  să le vadă.
- **Jailbreak și abuz de unelte:** modelul este împins să ignore limitele și să execute acțiuni
  neautorizate.

Cele patru controale cerute: **Least Privilege, Input Filtering, Output Monitoring, Red Teaming.**

## Incidente citate (slide-urile 22-24)

| Incident | Ce s-a întâmplat | Lecția |
| --- | --- | --- |
| Samsung, 2023 | Ingineri au pus cod și transcrieri confidențiale în ChatGPT, din conturi personale | Fără contract de prelucrare, datele ies din controlul companiei |
| Claude Code, 2025 | Conform prezentării, agentul a șters un mediu de producție și copiile de siguranță | Comenzile distructive cer limite și confirmare |
| DeepSeek, 2025 | Bază ClickHouse expusă public, cu conversații și chei | Jurnalele trebuie securizate |
| EchoLeak, 2025 | E-mail cu text ascuns a declanșat exfiltrare în M365 Copilot, fără niciun click | Datele neverificate nu sunt instrucțiuni |
| Cursor IDE, 2025 | CVE-2025-54135: atac DNS rebinding asupra agentului local | Serviciile locale pot fi atinse din browser |
| Mata v. Avianca, 2023 | Avocați sancționați pentru citări inventate de ChatGPT | Verifică sursele |

Slide-ul 25 adaugă statistici: 32% din exfiltrarea de date corporative spre conturi personale trece
prin GenAI (LayerX), iar 51% din costurile unei breșe apar după primul an (IBM).

## Reguli de folosire (slide-ul 26)

| Fă | Nu face |
| --- | --- |
| Verifică faptele, codul și calculele | Nu pune date de clienți, parole sau secrete în modele publice |
| Elimină datele sensibile din prompturi | Nu avea încredere oarbă în output |
| Cere surse și verifică-le | Nu publica fără verificare, mai ales cifre |
| Etichetează conținutul generat de AI | Nu ocoli regulile de clasificare a datelor |
| Păstrează un om în buclă la decizii importante | |

## Ce măsurăm (slide-ul 27)

| Zonă | Ce verificăm | Metrică |
| --- | --- | --- |
| Calitate | Exactitate față de surse sigure | Rata de halucinații |
| Comportament | Respectă formatul și limitele | Procent de instrucțiuni respectate |
| Siguranță | Conținut toxic, scurgeri de date personale | Rata încălcărilor de siguranță |
| Echitate | Stereotipuri între grupuri | Scor de disparitate |
| Operare | Degradare în timp | Drift, latență |

Metode: red teaming, evaluare de către experți, benchmark-uri automate (MMLU, HELM).

## Ciclul de risc NIST (slide-ul 28)

Govern, Map, Measure, Manage, într-un proces continuu. Este material de citit, nu ceva de construit
la hackathon.

## EU AI Act (slide-urile 29-30)

| Nivel | Exemple | Obligații | Aplicare (conform prezentării) |
| --- | --- | --- | --- |
| Inacceptabil, interzis | Scor social, manipulare, exploatarea grupurilor vulnerabile | Interzis | Februarie 2025 |
| Ridicat | Recrutare, sănătate, infrastructură critică, credit, justiție | Date de calitate, supraveghere umană, jurnale, documentație, audituri | August 2026 |
| Limitat | Chatbot, deepfake, recunoașterea emoțiilor | Utilizatorul trebuie informat că interacționează cu AI | Februarie 2025 / august 2026 |
| Minim | Filtre spam, jocuri | Fără obligații speciale | Se aplică legile obișnuite |

| Amendă maximă | Când |
| --- | --- |
| 35 mil. EUR sau 7% din cifra de afaceri globală | Sisteme interzise |
| 15 mil. EUR sau 3% | Neconformitate |
| 7,5 mil. EUR sau 1% | Informații false date autorităților |

Se aplică suma mai mare. Modelele de uz general au obligații proprii de documentare, respectare a
drepturilor de autor și rezumare a datelor de antrenare.

### Cum ne încadrăm (ipoteză de argumentare)

Anexa III, punctul 2 încadrează la risc ridicat sistemele folosite ca „safety components in the
management and operation of [...] the supply of [...] electricity”. Un triaj pentru inspectori sau o
prognoză pentru tranzacționare nu este componentă de siguranță, deci putem argumenta risc limitat sau
minim. Un chatbot pentru clienți are obligația de transparență. Prezentarea listează infrastructura
critică la risc ridicat, așa că arătăm oricum omul în buclă.

## Ce arătăm în demo

- **Evaluare:** un tabel mic. Pentru ML, MAE sau precision@k pe anomalii injectate. Pentru LLM, rata
  de halucinații și de respectare a formatului pe 20-30 de exemple fixe.
- **Cele patru controale:** LLM-ul doar citește, intrările sunt filtrate, ieșirile sunt verificate,
  iar 5 încercări de prompt injection sunt documentate.
- **Om în buclă:** AI-ul propune, omul aprobă, iar interfața spune clar ce a generat AI-ul.
- **Date sigure:** datele clienților nu pleacă brute spre un LLM. Le mascăm sau folosim un model
  local.
- **EU AI Act:** un slide cu încadrarea de mai sus.
