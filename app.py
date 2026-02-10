from flask import Flask, render_template, request, redirect, url_for, flash # Aggiunto flash
import csv
import datetime
import os # Importato os per controllare l'esistenza dei file

app = Flask(__name__)
app.secret_key = 'una_chiave_segreta_molto_segreta' # Necessario per i flash messages

# Definisci i nomi dei file CSV e le loro intestazioni
LIBRI_CSV = 'libri.csv'
PRESTITI_CSV = 'prestiti.csv'
LIBRI_HEADERS = ['codice', 'titolo', 'autore', 'disponibile']
PRESTITI_HEADERS = ['codice_libro', 'nome_utente', 'data_prestito', 'data_restituzione']

# Funzione per inizializzare i file CSV se non esistono
def initialize_csv_files():
    if not os.path.exists(LIBRI_CSV):
        with open(LIBRI_CSV, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=LIBRI_HEADERS)
            writer.writeheader()
    if not os.path.exists(PRESTITI_CSV):
        with open(PRESTITI_CSV, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=PRESTITI_HEADERS)
            writer.writeheader()

# Chiamata all'avvio dell'applicazione
initialize_csv_files()

# Funzione per aggiungere un libro
def aggiungi_libro(codice, titolo, autore):
    with open(LIBRI_CSV, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=LIBRI_HEADERS)
        writer.writerow({'codice': codice, 'titolo': titolo, 'autore': autore, 'disponibile': 'True'})
    flash(f'Libro "{titolo}" aggiunto con successo!', 'success') # Flash message di successo

# Funzione per registrare un prestito
def registra_prestito(codice_libro, nome_utente, data_prestito):
    # Verifica se il libro esiste e se è disponibile
    libro_trovato = False
    libri = []
    with open(LIBRI_CSV, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            libri.append(row)
            if row['codice'] == codice_libro:
                libro_trovato = True
                if row['disponibile'] == 'False':
                    flash(f'Errore: Il libro "{codice_libro}" è già in prestito.', 'danger')
                    return False # Libro già in prestito
    
    if not libro_trovato:
        flash(f'Errore: Il libro con codice "{codice_libro}" non esiste.', 'danger')
        return False # Libro non trovato

    with open(PRESTITI_CSV, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=PRESTITI_HEADERS)
        writer.writerow({'codice_libro': codice_libro, 'nome_utente': nome_utente, 'data_prestito': data_prestito, 'data_restituzione': ''})
    
    # Aggiorna disponibilità libro
    aggiorna_disponibilita_libro(codice_libro, False)
    flash(f'Prestito del libro "{codice_libro}" registrato con successo!', 'success')
    return True

# Funzione per registrare la restituzione di un libro
def registra_restituzione(codice_libro):
    prestiti_aggiornati = []
    prestito_trovato = False
    libro_da_rendere_disponibile = False

    with open(PRESTITI_CSV, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['codice_libro'] == codice_libro and row['data_restituzione'] == '':
                # Trovato il prestito attivo per questo libro
                row['data_restituzione'] = datetime.date.today().isoformat()
                prestito_trovato = True
                libro_da_rendere_disponibile = True
            prestiti_aggiornati.append(row)
    
    if not prestito_trovato:
        flash(f'Errore: Nessun prestito attivo trovato per il libro con codice "{codice_libro}".', 'danger')
        return False

    with open(PRESTITI_CSV, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=PRESTITI_HEADERS)
        writer.writeheader()
        writer.writerows(prestiti_aggiornati)
    
    if libro_da_rendere_disponibile:
        aggiorna_disponibilita_libro(codice_libro, True)
        flash(f'Restituzione del libro "{codice_libro}" registrata con successo!', 'success')
        return True
    
    return False

# Funzione per aggiornare la disponibilità di un libro
def aggiorna_disponibilita_libro(codice_libro, disponibile):
    libri = []
    libro_trovato = False
    with open(LIBRI_CSV, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['codice'] == codice_libro:
                row['disponibile'] = 'True' if disponibile else 'False'
                libro_trovato = True
            libri.append(row)
    
    if not libro_trovato:
        # Questo caso non dovrebbe accadere se la validazione è corretta, ma è una buona pratica
        print(f"Attenzione: Libro con codice {codice_libro} non trovato durante l'aggiornamento della disponibilità.")

    with open(LIBRI_CSV, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=LIBRI_HEADERS)
        writer.writeheader()
        writer.writerows(libri)

# Funzione per ottenere l'elenco dei libri
def elenco_libri(solo_disponibili=None): # Modificato per supportare tutti i libri
    libri_list = []
    with open(LIBRI_CSV, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Converte la stringa 'True'/'False' in booleano
            row['disponibile'] = (row['disponibile'] == 'True') 
            libri_list.append(row)

    if solo_disponibili is True:
        return [libro for libro in libri_list if libro['disponibile']]
    elif solo_disponibili is False:
        return [libro for libro in libri_list if not libro['disponibile']]
    else: # Restituisce tutti i libri se solo_disponibili è None
        return libri_list

# Funzione per ottenere lo storico dei prestiti
def storico_prestiti():
    with open(PRESTITI_CSV, mode='r') as file:
        reader = csv.DictReader(file)
        return list(reader)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/aggiungi_libro', methods=['GET', 'POST'])
def aggiungi_libro_route():
    if request.method == 'POST':
        codice = request.form['codice'].strip()
        titolo = request.form['titolo'].strip()
        autore = request.form['autore'].strip()

        # Controllo del codice
        if not codice:
            flash("Il codice non può essere vuoto.", 'danger')
            return render_template('aggiungi_libro.html')
        
        # Controllo se il codice esiste già
        with open(LIBRI_CSV, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['codice'] == codice:
                    flash(f"Un libro con codice '{codice}' esiste già.", 'danger')
                    return render_template('aggiungi_libro.html')

        # Controllo del titolo
        if not titolo:
            flash("Il titolo non può essere vuoto.", 'danger')
            return render_template('aggiungi_libro.html')

        # Controllo dell'autore
        if not autore:
            flash("L'autore non può essere vuoto.", 'danger')
            return render_template('aggiungi_libro.html')

        # Se tutti i controlli passano, aggiungi il libro
        aggiungi_libro(codice, titolo, autore)
        return redirect(url_for('index'))

    return render_template('aggiungi_libro.html')

@app.route('/registra_prestito', methods=['GET', 'POST'])
def registra_prestito_route():
    if request.method == 'POST':
        codice_libro = request.form['codice_libro'].strip()
        nome_utente = request.form['nome_utente'].strip()
        data_prestito = datetime.date.today().isoformat()

        if not codice_libro:
            flash("Il codice del libro non può essere vuoto.", 'danger')
            return render_template('registra_prestito.html')
        if not nome_utente:
            flash("Il nome utente non può essere vuoto.", 'danger')
            return render_template('registra_prestito.html')

        if registra_prestito(codice_libro, nome_utente, data_prestito):
            return redirect(url_for('index'))
        else:
            # Se registra_prestito ritorna False (errore), rimane sulla stessa pagina con il flash message
            return render_template('registra_prestito.html')
            
    return render_template('registra_prestito.html')

# Nuova rotta per la restituzione
@app.route('/registra_restituzione', methods=['GET', 'POST'])
def registra_restituzione_route():
    if request.method == 'POST':
        codice_libro = request.form['codice_libro'].strip()

        if not codice_libro:
            flash("Il codice del libro non può essere vuoto.", 'danger')
            return render_template('registra_restituzione.html')
        
        if registra_restituzione(codice_libro):
            return redirect(url_for('index'))
        else:
            return render_template('registra_restituzione.html')

    return render_template('registra_restituzione.html')


@app.route('/libri')
def libri():
    libri_disponibili = elenco_libri(solo_disponibili=True) # Mostra solo i disponibili per questa pagina
    return render_template('libri.html', libri=libri_disponibili)

@app.route('/tutti_i_libri') # Nuova rotta per vedere tutti i libri
def tutti_i_libri():
    tutti_i_libri = elenco_libri(solo_disponibili=None) # Mostra tutti i libri
    return render_template('libri.html', libri=tutti_i_libri) # Potresti usare un template diverso se vuoi

@app.route('/prestiti')
def prestiti():
    storico = storico_prestiti()
    return render_template('prestiti.html', prestiti=storico)

if __name__ == '__main__':
    app.run(debug=True)
