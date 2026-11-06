# Reguli pentru documente

Se aplică oricui scrie în `docs/`: oameni și agenți. Scopul este ca oricare dintre noi să găsească
repede o informație și să o poată verifica singur.

## O informație stă într-un singur loc

- Nu repeta o informație care există deja. Pune un link către fișierul în care stă.
- Dacă găsești aceeași informație în două locuri, păstreaz-o în fișierul al cărui titlu i se
  potrivește cel mai bine și șterge-o din celălalt.
- Nu copia ce are deja loc în `CONTEXT.md`, `AGENTS.md`, `README.md` sau `pitch/`. Pune un link.

## Când apare ceva nou

1. Caută în [README.md](README.md) fișierul potrivit.
2. Modifică textul existent, nu adăuga o versiune nouă lângă cea veche. Istoricul e în git.
3. Actualizează „Ultima verificare” din antetul fișierului.
4. Dacă noua informație contrazice una veche și nu știi care e corectă, păstrează-le pe amândouă
   cu sursa lor și adaug-o în [intrebari-deschise.md](intrebari-deschise.md). Când se lămurește,
   păstrează doar varianta corectă și scoate întrebarea.

Creează un fișier nou doar dacă niciun titlu existent nu se potrivește, și adaugă-l în același
commit în tabelul din [README.md](README.md).

## Titlurile spun ce conține fișierul

- Numele descrie conținutul: `ppc-proiecte-ai.md`, nu `note.md` sau `diverse.md`.
- Fișierul conține doar ce promite titlul. Dacă o parte nu se potrivește, mut-o.
- Numele sunt cu litere mici, cu cratime și fără diacritice.

## Fișierele se citesc ușor

Fiecare fișier începe cu un rând care spune ce conține, apoi cu sursa și data ultimei verificări:

```markdown
# Titlu

Ce găsești aici, într-o frază.

Surse: de unde vin informațiile. Ultima verificare: AAAA-LL-ZZ.
```

- Pune concluzia prima. Folosește titluri clare, tabele și liste scurte.
- Scrie în română, cu propoziții scurte. Lasă în engleză doar numele proprii și termenii tehnici.
- Separă clar ce știm de ce presupunem. Marchează presupunerile cu „ipoteză” și spune de unde vine
  fiecare cifră.
- Documentele originale stau în `surse/`, cu nume sugestive. Le rezumăm în fișierele Markdown.

## Ce nu intră aici

Repo-ul ajunge pe GitHub, iar juriul și organizatorii vor avea acces la proiectul predat. Nu pune
aici parole, chei, date personale sau date reale ale clienților.
