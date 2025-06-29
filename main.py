import os
import shutil
import time
from pathlib import Path
from datetime import datetime
from nudenet import NudeClassifier

def get_input_directory():
    """Chiede all'utente di specificare la directory da analizzare"""
    while True:
        dir_name = input("Inserisci il nome della directory da analizzare: ").strip()
        
        if not dir_name:
            print("Errore: Il nome della directory non può essere vuoto!")
            continue
            
        dir_path = Path(dir_name)
        
        if not dir_path.exists():
            print(f"Errore: La directory '{dir_name}' non esiste!")
            risposta = input("Vuoi riprovare? (s/n): ").strip().lower()
            if risposta != 's':
                return None
            continue
            
        if not dir_path.is_dir():
            print(f"Errore: '{dir_name}' non è una directory!")
            risposta = input("Vuoi riprovare? (s/n): ").strip().lower()
            if risposta != 's':
                return None
            continue
            
        return str(dir_path)

def setup_scan_directories(input_directory):
    """Crea la struttura di cartelle scan/nome_YYYYMMDD_HHMMSS/safe|unsafe"""
    # Crea la cartella scan principale
    scan_dir = Path("scan")
    scan_dir.mkdir(exist_ok=True)
    
    # Ottieni il nome della directory da analizzare
    dir_name = Path(input_directory).name
    
    # Crea una sottocartella con nome directory + timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_dir = scan_dir / f"{dir_name}_{timestamp}"
    session_dir.mkdir(exist_ok=True)
    
    # Crea le sottocartelle safe, unsafe
    safe_dir = session_dir / "safe"
    unsafe_dir = session_dir / "unsafe"
    logs_dir = session_dir
    
    safe_dir.mkdir(exist_ok=True)
    unsafe_dir.mkdir(exist_ok=True)
    
    return safe_dir, unsafe_dir, logs_dir, session_dir

def create_log_file(logs_dir, input_dir):
    """Crea il file di log con timestamp nel nome"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"classification_log_{timestamp}.txt"
    log_path = logs_dir / log_filename
    
    # Crea l'intestazione del log
    with open(log_path, 'w', encoding='utf-8') as log_file:
        log_file.write(f"LOG CLASSIFICAZIONE IMMAGINI - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        log_file.write("="*80 + "\n")
        log_file.write(f"Directory analizzata: {input_dir}\n")
        log_file.write("="*80 + "\n\n")
    
    return log_path

def log_message(log_path, message, print_to_console=True):
    """Scrive un messaggio sia nel log che nel terminale"""
    if print_to_console:
        print(message)
    
    with open(log_path, 'a', encoding='utf-8') as log_file:
        log_file.write(message + "\n")

def get_image_files(img_dir):
    """Ottiene tutti i file immagine dalla cartella specificata"""
    img_path = Path(img_dir)
    
    if not img_path.exists():
        print(f"Errore: La cartella '{img_dir}' non esiste!")
        return []
    
    # Estensioni immagine supportate
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}
    
    image_files = []
    
    # Scansione ricorsiva di tutte le sottocartelle
    for file_path in img_path.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
            image_files.append(str(file_path))
    
    return image_files

def classify_and_organize_images(input_directory, batch_size, threshold):
    """
    Classifica le immagini e le sposta nelle cartelle appropriate
    
    Args:
        input_directory (str): Directory da analizzare
        batch_size (int): Dimensione del batch per la classificazione
        threshold (float): Soglia per considerare un'immagine come unsafe (default: 0.5)
    """
    start_time = time.time()
    
    # Setup delle cartelle nella struttura scan/nome_timestamp/
    safe_dir, unsafe_dir, logs_dir, session_dir = setup_scan_directories(input_directory)
    
    # Crea il file di log
    log_path = create_log_file(logs_dir, input_directory)
    
    # Ottieni tutte le immagini dalla cartella specificata
    image_files = get_image_files(input_directory)
    
    if not image_files:
        log_message(log_path, f"Nessuna immagine trovata nella directory '{input_directory}'")
        return
    
    log_message(log_path, f"Trovate {len(image_files)} immagini da classificare...")
    log_message(log_path, f"Directory di input: {input_directory}")
    log_message(log_path, f"Directory di output: {session_dir}")
    log_message(log_path, f"Batch size: {batch_size}")
    log_message(log_path, f"Soglia unsafe: {threshold}")
    log_message(log_path, "")
    
    # Inizializza il classificatore
    log_message(log_path, "Inizializzazione del classificatore NudeNet...")
    classifier = NudeClassifier()
    
    # Classifica le immagini
    log_message(log_path, "Classificazione in corso...")
    log_message(log_path, "")
    
    # Processa i file in batch ma mostra progresso per ogni file
    total_files = len(image_files)
    processed_files = 0
    batch_start = 0
    
    # Contatori per il riepilogo
    safe_count = 0
    unsafe_count = 0
    error_count = 0
    
    while batch_start < total_files:
        batch_end = min(batch_start + batch_size, total_files)
        current_batch = image_files[batch_start:batch_end]
        
        # Classifica il batch corrente
        results = classifier.classify(current_batch)
        
        # Processa i risultati del batch
        for image_path, classification in results.items():
            processed_files += 1
            try:
                source_path = Path(image_path)
                filename = source_path.name
                
                # Per evitare conflitti di nomi, aggiungi un prefisso se necessario
                counter = 1
                original_filename = filename
                while (safe_dir / filename).exists() or (unsafe_dir / filename).exists():
                    name_parts = original_filename.rsplit('.', 1)
                    if len(name_parts) == 2:
                        filename = f"{name_parts[0]}_{counter}.{name_parts[1]}"
                    else:
                        filename = f"{original_filename}_{counter}"
                    counter += 1
                
                # Determina se l'immagine è safe o unsafe
                unsafe_probability = classification.get('unsafe', 0)
                
                if unsafe_probability > threshold:
                    # Immagine unsafe
                    destination = unsafe_dir / filename
                    shutil.copy2(str(source_path), str(destination))
                    unsafe_count += 1
                    message = f"[{processed_files}/{total_files}] UNSAFE: {source_path.name} -> {filename} (probabilità: {unsafe_probability:.3f})"
                    log_message(log_path, message)
                else:
                    # Immagine safe
                    destination = safe_dir / filename
                    shutil.copy2(str(source_path), str(destination))
                    safe_count += 1
                    message = f"[{processed_files}/{total_files}] SAFE: {source_path.name} -> {filename} (probabilità unsafe: {unsafe_probability:.3f})"
                    log_message(log_path, message)
                    
            except Exception as e:
                error_message = f"[{processed_files}/{total_files}] Errore nel processare {image_path}: {str(e)}"
                log_message(log_path, error_message)
                error_count += 1
        
        batch_start = batch_end
    
    # Calcola il tempo trascorso
    elapsed_time = time.time() - start_time
    mins, secs = divmod(elapsed_time, 60)
    
    # Riepilogo finale
    log_message(log_path, "")
    log_message(log_path, "="*60)
    log_message(log_path, "RIEPILOGO CLASSIFICAZIONE:")
    log_message(log_path, f"Directory analizzata: {input_directory}")
    log_message(log_path, f"Directory risultati: {session_dir}")
    log_message(log_path, f"Immagini safe: {safe_count}")
    log_message(log_path, f"Immagini unsafe: {unsafe_count}")
    log_message(log_path, f"Errori: {error_count}")
    log_message(log_path, f"Totale processate: {safe_count + unsafe_count}")
    log_message(log_path, f"Tempo totale di esecuzione: {int(mins)} minuti e {secs:.2f} secondi")
    log_message(log_path, "="*60)
    log_message(log_path, f"Log salvato in: {log_path}")
    
    print(f"\n" + "="*60)
    print(f"SCANSIONE COMPLETATA!")
    print(f"Risultati salvati in: {session_dir}")
    print(f"Log completo in: {log_path}")
    print("="*60)

def main():
    """Funzione principale"""
    print("="*60)
    print("CLASSIFICATORE IMMAGINI CON NUDENET")
    print("="*60)
    
    # Chiedi all'utente quale directory analizzare
    input_directory = get_input_directory()
    
    if input_directory is None:
        print("Operazione annullata.")
        return
    
    # Parametri configurabili
    BATCH_SIZE = 4  # Modifica secondo le tue esigenze
    THRESHOLD = 0.4  # Soglia per considerare unsafe (0.0 - 1.0)
    
    print(f"\nDirectory da analizzare: {input_directory}")
    print(f"Batch size: {BATCH_SIZE}")
    print(f"Soglia unsafe: {THRESHOLD}")
    
    # Conferma prima di procedere
    conferma = input(f"\nProcedere con la scansione? (s/n): ").strip().lower()
    if conferma != 's':
        print("Operazione annullata.")
        return
    
    print("-" * 60)
    
    try:
        classify_and_organize_images(
            input_directory=input_directory,
            batch_size=BATCH_SIZE, 
            threshold=THRESHOLD
        )
    except Exception as e:
        print(f"Errore durante l'esecuzione: {str(e)}")

if __name__ == "__main__":
    main()
