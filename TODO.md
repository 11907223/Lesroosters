# Lecturs & Lesroosters
On the TODO list:

## todo
- studenten class
- visualisatie
- maluspunten
    - kan worden doorgebouwd op originele schedule.py (deprecated)
- random algoritme (random vak in random tijdslot)

## heuristieken
- Avondslot dichtgooien
- Grootste vak in 1 zaal
- grootste vakken eerst
- studenten met meeste vakken eerst

## Assignment
1. [ ] Rooster alle vakken uit de onderstaande tabel in. Je mag E(studenten) nog even vergeten.
2. [ ] Hou nu wel rekening met E(studenten).
    > Voor iedere student die niet meer in de zaal past krijg je een maluspunt. Hoe minder maluspunten, hoe beter. De grootste zaal heeft ook een avondslot van 17:00-19:00, maar gebruik van het avondslot kost vijf maluspunten.
3. [ ] Werkcolleges en practica mogen in meerdere groepen gegeven worden. In tegenstelling tot een hoorcollege hoeven daarbij niet alle ingeschreven studenten in één sessie bedeeld te worden. Maak hiervan gebruik om het rooster te verbeteren.
4. [ ] Roostering wil bekijken of roosters rekening kunnen houden met individuele vakinschrijvingen. In plaats van de geschatte hoeveelheid studenten maak je hier gebruik van het daadwerkelijke aantal inschrijvingen per vak. Ieder vakconflict (meer dan één activiteit op hetzelfde moment) in het rooster van één student levert één maluspunt op.
5. [ ] Een tussenslot voor een student op een dag levert één maluspunt op. Twee tussensloten op één dag voor een student levert drie maluspunten op. Drie tussensloten op één dag is niet toegestaan.

    > De kans op verzuim bij meerdere tussensloten is aanzienlijk groter dan bij één tussenslot. Studenten zien het liefst aaneengesloten activiteiten en zo min mogelijk “tussensloten”. Dat zijn tijdsloten zonder ingeroosterde activiteiten voor de student, maar waarvoor en waarna wel een activiteit plaatsvindt. Naast de wens van de student is dit ook belangrijk voor het onderwijs, zo zal het verzuim bij de verschillende activiteiten lager zijn als activiteiten aaneengesloten worden geroosterd. Ook is dit belangrijk voor de drukte op de faculteit, want bij zulke tussensloten nemen studenten plaats op (zelf)studieplekken en studieplekken zijn er er maar beperkt. Daarom wil roostering kijken of tussenuren geminimaliseerd kunnen worden.

## Root directory

### README.md

- [ ] Write introduction
- [ ] Write overview
- [ ] Write requirements (or requirements.txt)
- [ ] Write installation
- [ ] Write usage
- [x] Write project structure
    - [ ] Update project structure
- [ ] Write project summary
- [ ] Write acknowledgements
- [ ] Write contact

## Code folder

### Structure
- [x] Discuss if classes go in subdirectory
- [ ] In timeslots door rooster stappen en kijken naar problemen
- [ ] Maluspunten bepalen is non-linear. Kijk naar wat er is veranderd

- [ ] Maluspunten calculator
    - [ ] elke student die vaker op één timeslot zit is een maluspunt
    - [ ] dictionary per timeslot bijhouden
        - [ ] die schrijft het rooster opnieuw maar dan in dicts
        - [ ] {timeslot: jimmy}
        - [ ] bijhouden per type maluspunt
            (dict voor maandag, di,wo, etc)

### Classes folder

- [ ] activity.py
    - [ ] typehint variables. Current function args unclear.
- [ ] Course.py
- [ ] Classroom.py