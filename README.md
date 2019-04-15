# ppoit
Záverečné zadanie ku skúške
Cieľom zadania je implementovať inteligentné riadenie fyzikálneho modelu automobilu prostredníctvom webovej aplikácie, pričom miera inteligencie bude daná senzormi, ktorými bude automobil vybavený.

K dispozícii bude nasledovný hardvér: fyzikálny model automobilu  ECX BARRAGE 1/24 4WD SCALE CRAWLER, Raspberry Pi 3 Model B, infračervené snímače, ultrazvukové snímače, fotoodpory, A/D prevodníky, Web kamera, USB káble, LED diódy, odpory, tranzistory, univerzálne dosky, prepojovacie kábliky. Napájanie je riešené z powerbank-u.

Vašou úlohou je vytvoriť webovú aplikáciu v jazyku Python na platforme Raspberry Pi, ktorá bude realizovať nasledovné funkcie:

1.       spustenie aplikácie tlačidlom Start, ktoré bude slúžiť na inicializáciu systému, nadviazanie spojenia a aktiváciu senzorov a akčných členov

2.       zastavenie aplikácie tlačidlom Stop, ktoré bude slúžiť na deaktiváciu systému a ukončenie spojenia

3.       ovládanie zatáčania automobilu posuvníkom

4.       ovládanie rýchlosti automobilu posuvníkom

5.       pohyb automobilu sledovaním trajektórie vymedzenej čiarou na podlahe (lane assistant)

6.       plynulé spomaľovanie až zastavenie a plynulý rozbeh v závislosti na vzdialenosti od prekážky (adaptívny tempomat)

7.       rozsvietenie resp. vypnutie svetiel na základe zistenej intenzity okolitého svetla (inteligentné svetlá)

8.       snímanie obrazu z Web kamery (predná kamera)

9.        archiváciu snímaných a akčných signálov a údajov prostredníctvom súboru (aj s možnosťou ich výpisu a vykreslenia)

Ku každému bodu je potrebné vytvoriť serverovú aj klientskú časť, pričom úlohou serverovej časti je zvyčajne riadenie a hardvérová realizácia a úlohou klientskej časti je ovládanie a vizualizácia (numericky, graficky - grafy, cíferníky, posuvníky...).

K vytvorenému dielu je potrebné napísať technickú dokumentáciu v rozsahu min. 10 strán formátu A4. Technická dokumentácia bude obsahovať vývojársku a používateľskú príručku. Technickú dokumentáciu (vo formáte DOC alebo PDF) spolu s vytvorenou aplikáciou odovzdáva vedúci tímu elektronicky prostredníctvom systému Moodle ako jeden zozipovaný súbor.

Pri vývoji aplikácie je potrebné používať verzionovací systém GitHub (prípadne Bitbucket), pričom jednotlivé príspevky musia byť vhodne komentované a v technickej dokumentácii musí byť uvedená adresa úložiska (prípadne ďalšie prístupové údaje).

Zadanie sa vypracováva v tímoch, do ktorých budete zadelení na cvičeniach. Každý tím si zvolí vedúceho tímu, ktorý bude riadiť práce a na záver percentuálne hodnotiť členov tímu (vrátane seba). V prípade nesúhlasu ktoréhokoľvek člena s hodnotením vykoná prerozdelenie hodnotenia skúšajúca komisia. Skúšajúca komisia ohodnotí vypracované zadanie na základe vytvoreného diela, napísanej dokumentácie a obhajoby zadania v deň skúšky absolútnym počtom bodov (max. 140 bodov pre 5-členný tím), ktorý bude rozrátaný medzi členov tímu podľa ich percentuálneho hodnotenia.

Približný rozpis bodovania je nasledovný: zdokumentovaný návrh architektúry celej aplikácie 10b, návrh a realizácia komunikačného protokolu 10b, návrh a realizácia serverovej časti 10b, návrh a realizácia klientskej časti 10b, body 1. a 2. spolu 20b, každý z bodov 3. - 9. cca 10b, technická dokumetácia 10b. 6-členné tímy budú mať navyše za úlohu aj archiváciu prostredníctvom databázy, za ktorú bude možné získať navyše 28 bodov.

Na jednotlivých úlohách môžu participovať aj viacerí členovia tímu.

Upozornenie: Vypracované zadanie je potrebné odovzdať do určeného termínu (viď. údaj "Termín odovzdania" nižšie - môže sa ešte zmeniť, ak sa zmení termín skúšky). Penalizácia za každý deň omeškania je 1 bod na každého člena tímu.
