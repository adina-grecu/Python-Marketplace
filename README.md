Nume: Adina Grecu
Grupă: 331CC

Tema 1 - Marketplace

Ca abordare generala, am urmat flow-ul descris in enuntul problemei si am 
implementat functiile definite in scheletul de cod. Marketplace-ul urmeaza 
modelul unui magazin real care are mai multe rafturi de aceeasi dimensiune 
queue_size_per_producer, ce apartin de fiecare producer. Fiecare producer isi
plaseaza produsele pe raftul sau prin metoda de publish. Cumparatorii sunt 
reprezentati de consumers. Ei iau de pe raft produsele dorite si, fiind foarte
civilizati, daca renunta la un produs, acestia il pun la loc pe raftul de unde 
l-au luat. Cand vor sa plaseze o comanda, acestia pun produsele pe banda pentru
a le plati (continutul cosului este mutat intr-o variabila order) si returneaza
cosul de cumparaturi (adica este sters din lista de cosuri existente). 
Implementarea este eficienta deoarece actiunile sunt realizate in paralel, fiind 
dependente de alte actiuni intr-o maniera minima. Ar putea fi totusi
imbunatatita deoarece programul retine si itereaza prin multe informatii inutile
care scad performanta, cum ar fi detaliile legate de produs care, in 
implementarea actuala, nu sunt folosite efectiv pentru nimic. Programul ar putea
fi scalat, de exemplu, pentru a lua in considerare pretul produselor si suma de 
bani pe care o au cumparatorii. 


Opțional:

De menționat cazuri speciale, nespecificate în enunț și cum au fost tratate.

Caz special:
Verificare daca un consumator incearca sa scoata din cos un produs care nu exista. Functionalitate implementata, dar nu este reflectata in teste.


Implementare

Am implementat intregul enunt al temei. 
Dacă există funcționalități extra, pe lângă cele din enunț - descriere succintă + motivarea lor
De specificat funcționalitățile lipsă din enunț (dacă există) și menționat dacă testele reflectă sau nu acest lucru
Dificultăți întâmpinate
Lucruri interesante descoperite pe parcurs

Implementare

Marketplace
Marketplace-ul este intermediar intre consumatori si producatori. 
Aceste contine intregul market in care sunt retinute rafturile si produsele 
existente pe acestea. Acesta este locul in care producatorii adauga produse si consumatorii le iau sau le pun la loc. Pentru a valida restrictiile impuse, Marketplace retine pentru fiecare producator gradul de ocupare al rafturilor (shelf_sizes) si cosurile de cumparaturi create de consumatori. 
In aceste cosuri de cumparaturi, fiecare produs are asociat raftul de pe care a fost luat, pentru a ajuta cumparatorii sa stie unde returneze produsul daca nu mai vor sa-l cumpere. Astfel, in cart, este adaugat un obiect cu 2 chei: product, care contine produsul in sine si shelf, care contine id-ul raftului de care apartine produsul. 
Dimensiunea raftului este standard, indicata de queue_size_per_producer. 
Producatorii pot adauga produse pe raft doar daca nu depasesc aceasta dimensiune. Ea este decrementata atunci cand producatorul plaseaza un produs pe raftul sau sau cand un consumator scoate din cos un produs si il pune la loc pe raft. De asemenea, este incrementata atunci cand un consumator ia de pe raft un produs si il pune in cosul sau de cumparaturi.

Marketplace-ul genereaza id-uri pentru cosuri de cumparaturi folosind o variabila cart_generator care este incrementata si initializeaza un cos lista de carts. Acelasi principiu il urmeaza si inregistrarea producatorilor: Marketplace-ul incrementeaza variabila producer_id_generator, o atribuie unui producator si initializeaza raftul in market si atribuie raftului dimensiunea standard in shelf_sizes.

Functia de publish verifica daca este loc pe raft pentru a aseza produsul, dupa care adauga in market, pe raftul producatorului, produsul respectiv si decrementeaza dimensiunea disponibila de pe reft. 

Functia de adaugare in cos verifica daca exista produsul in market,
scoate de pe raft produsul si adauga creeaza o intrare in carts, in cosul corespunzator, cu produsul, si retine raftul de pe care acesta a fost luat, dupa care actualizeaza dimensiunea raftului. 

Functia de stergere din cos cauta in cos produsul, il scoate din cosul corespunzator din carts si il pune la loc pe raftul de pe care a fost luat 
si actualizeaza dimensiunea raftului.

Pentru a plasa comanda, in variabila order se retine contentul cosului, care apoi este golit si sters, mimand comportamentul unui cumparator civilizat care isi pune produsele pe banda pentru a le plati si apoi returneaza cosul de cumparaturi.


Producător
Producatorul are lista de produse pe care le va pune pe raftul sau si timpul
pe care trebuie sa il astepte daca una din actiuni nu are succes. Pentru fiecare produs din lista, acesta incearca sa aseze pe raft (publish) produsul corespunzator in cantitatea specifificata. Pentru a ma asigura ca toate produsele sunt publicate, am folosit un while care urmareste cantitatea, aceasta fiind actualizata doar daca actiunea de publish este finalizata cu succes. (Iterarea cu un for nu este adecvata deoarece pot fi 
mai multe incercari de publish decat iteratii prin for).

Consumator
Consumatorul (in cazul nostru, cumparatorul) are lista proprie de cosuri de cumparaturi. Pentru fiecare cos din lista, cere de la marketplace un id de cos (ca si cum ar lua un cos cand isi incepe cumparaturile) prin metoda de init_cart. Pentru fiecare produs din cos verifica mai intai tipul actiunii si retine cantitatea specificata. Consumatorul incearca sa adauge in cos produsul si cantitatea ramasa este actualizata doar atunci cand actiunea este finalizata cu succes, la fel si pentru remove. Am avut aceeasi motivatie ca in cazul producatorului, folosind 2 while-uri. 
In final, cand sunt realizate toate actiunile pentru un cos, este plasata comanda apeland functia de place_order.

Logger

Am folosit loggerul pentru a semnaliza diferite actiuni precum adaugarea si scoaterea din cos, plasarea comenzii, crearea unui cos nou, publicarea produselor, inregistrarea producatorului si cazurile in care aceste actiuni nu au succes.

Testare
Am implementat unit tests care verifica apelarea corecta a functiilor din marketplace si rezultatele corecte ale acestor apeluri in functie de limitarile programului (de exemplu, daca queue-size-ul producatorului este 2, apelul funcriei publish a treia oara va intoarce False.)


Resurse utilizate

Logger: 
https://stackoverflow.com/questions/40088496/how-to-use-pythons-rotatingfilehandler
https://docs.python.org/3/howto/logging.html

Unit testing: 
https://docs.python.org/3/library/unittest.html

Multiple Producer Multiple Consumer:
https://ocw.cs.pub.ro/courses/asc/laboratoare/03
https://superfastpython.com/thread-producer-consumer-pattern-in-python/
https://stackoverflow.com/questions/28349302/single-producer-multiple-consumer

Style:
https://peps.python.org/pep-0008/


Git

https://github.com/grecuadina/Python_Marketplace

Ce să NU


Detalii de implementare despre fiecare funcție/fișier în parte
Fraze lungi care să ocolească subiectul în cauză
Răspunsuri și idei neargumentate
Comentarii (din cod) și TODO-uri


////////////////////////////////////////////////////////////////////////////////////////



