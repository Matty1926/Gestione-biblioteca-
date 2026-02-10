# Gestione biblioteca scolastica
Questo è un progetto web sviluppato con il framework Flask di Python. 
In questo progetto per la gestione di una biblioteca scolastica sviluppato da **Manuel Catone**, **Gennaro Bonanno** e **Mattia Piccolo**  sono mostrati i concetti base di Flask, la gestione dei form HTML, la persistenza su file CSV e l'interazione tra diverse pagine web.







## Caratteristiche:
- ***Aggiunta dei libri***: Aggiunge i libri nella biblioteca inserendo i campi titolo, autore, codice 
- ***Registra prestiti/restituzione***: Registra i vari prestiti dei libri / Registra un' eventuale restituzione di un libro in prestito
- ***Storico dei prestiti***: Restituisce uno storico dei libri in prestito e dei libri che sono stati restituiti
- ***Elenco dei libri disponibili o in prestito***: Restituisce uno storico dei libri attualmente disponibili
- ***Accumulo e Salvataggio su CSV***: Il salvataggio dei libri aggiunti viene affettuato su un file csv




### Prerequisiti


#### Installazione delle Dipendenze
Per installare le librerie Python necessarie per questo progetto (principalmente Flask), apri il tuo terminale o prompt dei comandi e esegui questo comando:


````
pip install Flask
````




#### Struttura del Progetto

Il nostro progetto è organizzato come segue:
````
App_Flask_BibliotecaScolastica/
├── app.py                           # Il codice principale dell'applicazione Flask
└── templates/                       # Cartella per i template HTML
    ├── index.html                   # Pagina html principale della biblioteca
    ├── aggiungi_libro.html          # Pagina html per aggiungere libri alla biblioteca
    ├── registra_prestito.html       # Pagina html per registrare il prestito di un libro dispobile in biblioteca
    ├── registra_restituzione.html   # Pagina html per registrare la restituzione di un libro preso in prestito
    ├── libri.html                   # Pagina html per visualizzare i libri della biblioteca
    ├── prestiti.html                # Pagina html per visualizzare lo storico dei prestiti
 
````

Quando avvierai l'applicazione e completerai i campi, verranno creati i seguenti file CSV nella cartella principale del progetto:

``
libri.csv
``
``
prestiti.csv
``







### Come Avviare l'Applicazione
Segui questi passaggi per avviare l'applicazione web:

##### Naviga nella cartella del progetto:
Apri il terminale o il prompt dei comandi e spostati nella directory App_Flask_BibliotecaScolastica 


##### Avvia l'applicazione Flask:
Apri il terminale ed esegui il seguente comando:

````
python app.py
````
##### Accedi all'applicazione:
Dopo aver avviato il server, vedrai un messaggio nel terminale simile a questo:

 * Running on http://127.0.0.1:5000


Apri il tuo browser web preferito (Chrome, Firefox, Edge, Safari, ecc.) e vai all'indirizzo:
http://127.0.0.1:5000

L'applicazione è ora in esecuzione e pronta per l'uso!
