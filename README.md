Nume: Adina Grecu
Grupă: 331CC


Tema 1 - Marketplace

Ca abordare generală, am urmat flow-ul descris în enunțul problemei și am 
implementat funcțiile definite în scheletul de cod. Am implementat întregul 
enunț al temei. Marketplace-ul urmează modelul unui magazin real cu rafturi pe
care sunt puse produse de către produceri. Cumpărătorii sunt reprezentați de 
consumeri. 

Implementarea este eficientă deoarece acțiunile sunt realizate în paralel și
depind cât mai puțin posibil unele de altele. Ar putea fi îmbunătățită deoarece
programul reține și iterează prin multe informații inutile care scad 
performanța. De exemplu, detaliile legate de produs nu sunt folosite în niciun
fel in implementarea actuală. Programul ar putea fi dezvoltat pentru a lua în 
considerare prețul produselor și bugetul cumpărătorilor la plasarea comenzii. 


Implementare

Marketplace
Marketplace-ul este intermediar între consumatori și producători și în el am
salvat întregul magazin (market), structurat în rafturi (ale producătorilor),
care au produse. Acțiunile de publish, add_to_cart și remove_from_cart au loc
între market și carts, unde sunt salvate coșurile de cumpărături ale 
consumatorilor.

Dimensiunea raftului este standard (queue_size_per_producer), iar producătorii
pot adăuga produse pe raft doar dacă nu este depășită această dimensiune.
Pentru a valida această restricție, gradul de ocupare al rafturilor este
reținut în shelf_sizes. Spațiul disponibil pe un raft este decrementat în 
cadrul funcțiilor de publish și de remove și incrementat în add_to_cart.

O problemă pe care am întâmpinat-o în timpul implementării a fost în cadrul 
funcției de remove. Pentru a actualiza consistent gradul de ocupare al 
rafturilor, produsul trebuie să se întoarcă pe raftul de pe care a fost luat
dacă este scos din coș. Am luat decizia să rețin o asociere între produs și 
raft pentru fiecare produs adăugat în coș.


Producător
Producătorul încearcă să așeze pe raft, folosind metoda de publish, toate 
produsele din lista sa, pe rând, în cantitatea specificată. Pentru a mă 
asigura că toate produsele sunt publicate, am folosit un while care urmărește
cantitatea, aceasta fiind actualizată doar dacă acțiunea de publish a fost 
finalizată cu succes. (Iterarea cu un for nu este adecvată deoarece pot fi 
mai multe încercări de publish decât iterații prin for).

Consumator
Consumatorul (în cazul nostru, cumpărătorul) cere de la marketplace un coș
pentru a își începe cumpărăturile prin metoda de init_cart. Pentru a asigura 
corectitudinea datelor, și anume că produsele au fost adăugate și șterse în
modul cerut, am urmat aceeași logică ca în cazul producătorului, folosind un 
while în care cantitatea este actualizata atunci când acțiunea de add este 
finalizată cu succes (la fel si pentru remove). În final, când sunt realizate
toate acțiunile pentru un coș, este plasată comanda apelând funcția de 
place_order și se continuă cu următorul coș din listă, până la finalul acesteia.

Comanda este plasată după ce conținutul coșului este dus la casa de marcat și
coșul este returnat, acest aspect fiindilustrat în program prin mutarea 
conținutului într-o variabilă "order" și ștergerea coșului din carts.

Un caz special la care m-am gândit este acela în care un consumator încearcă să 
scoață din coș un produs care nu există. Am implementat o verificare pentru 
acest lucru, dar situația aceasta nu este reflectată în teste.


Resurse utilizate

Logger: 
https://stackoverflow.com/questions/40088496/how-to-ușe-pythons-rotatingfilehandler
https://docs.python.org/3/howto/logging.html

Unit testing: 
https://docs.python.org/3/library/unittest.html

Threads:
https://ocw.cs.pub.ro/courses/asc/laboratoare/03

Gît:
https://github.com/grecuadina/Python_Marketplace