import os
import shutil
import time
from pathlib import Path
from datetime import datetime
from nudenet import NudeClassifier

def setup_directories():
    """Crea le cartelle safe, unsafe e logs se non esistono"""
    safe_dir = Path("safe")
    unsafe_dir = Path("unsafe")
    logs_dir = Path("logs")
    
    safe_dir.mkdir(exist_ok=True)
    unsafe_dir.mkdir(exist_ok=True)
    logs_dir.mkdir(exist_ok=True)
    
    return safe_dir, unsafe_dir, logs_dir

def create_log_file(logs_dir):
    """Crea il file di log con timestamp nel nome"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"classification_log_{timestamp}.txt"
    log_path = logs_dir / log_filename
    
    # Crea l'intestazione del log
    with open(log_path, 'w', encoding='utf-8') as log_file:
        log_file.write(f"LOG CLASSIFICAZIONE IMMAGINI - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        log_file.write("="*80 + "\n\n")
    
    return log_path

def log_message(log_path, message, print_to_console=True):
    """Scrive un messaggio sia nel log che nel terminale"""
    if print_to_console:
        print(message)
    
    with open(log_path, 'a', encoding='utf-8') as log_file:
        log_file.write(message + "\n")

def get_image_files(img_dir):
    """Ottiene tutti i file immagine dalla cartella img"""
    img_path = Path(img_dir)
    
    if not img_path.exists():
        print(f"Errore: La cartella '{img_dir}' non esiste!")
        return []
    
    # Estensioni immagine supportate
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}
    
    image_files = []
    for file_path in img_path.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
            image_files.append(str(file_path))
    
    return image_files

def classify_and_organize_images(batch_size, threshold):
    """
    Classifica le immagini e le sposta nelle cartelle appropriate
    
    Args:
        batch_size (int): Dimensione del batch per la classificazione
        threshold (float): Soglia per considerare un'immagine come unsafe (default: 0.5)
    """
    start_time = time.time()
    
    # Setup delle cartelle
    safe_dir, unsafe_dir, logs_dir = setup_directories()
    
    # Crea il file di log
    log_path = create_log_file(logs_dir)
    
    # Ottieni tutte le immagini dalla cartella img
    image_files = get_image_files("img")
    
    if not image_files:
        log_message(log_path, "Nessuna immagine trovata nella cartella 'img'")
        return
    
    log_message(log_path, f"Trovate {len(image_files)} immagini da classificare...")
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
                
                # Determina se l'immagine è safe o unsafe
                unsafe_probability = classification.get('unsafe', 0)
                
                if unsafe_probability > threshold:
                    # Immagine unsafe
                    destination = unsafe_dir / filename
                    shutil.copy2(str(source_path), str(destination))
                    unsafe_count += 1
                    message = f"[{processed_files}/{total_files}] UNSAFE: {filename} (probabilità: {unsafe_probability:.3f}) -> copiata in 'unsafe/'"
                    log_message(log_path, message)
                else:
                    # Immagine safe
                    destination = safe_dir / filename
                    shutil.copy2(str(source_path), str(destination))
                    safe_count += 1
                    message = f"[{processed_files}/{total_files}] SAFE: {filename} (probabilità unsafe: {unsafe_probability:.3f}) -> copiata in 'safe/'"
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
    log_message(log_path, "="*50)
    log_message(log_path, "RIEPILOGO CLASSIFICAZIONE:")
    log_message(log_path, f"Immagini safe: {safe_count}")
    log_message(log_path, f"Immagini unsafe: {unsafe_count}")
    log_message(log_path, f"Errori: {error_count}")
    log_message(log_path, f"Totale processate: {safe_count + unsafe_count}")
    log_message(log_path, f"Tempo totale di esecuzione: {int(mins)} minuti e {secs:.2f} secondi")
    log_message(log_path, "="*50)
    log_message(log_path, f"Log salvato in: {log_path}")
    
    print(f"\nLog completo salvato in: {log_path}")

def main():
    """Funzione principale"""
    # Parametri configurabili
    BATCH_SIZE = 32  # Modifica secondo le tue esigenze
    THRESHOLD = 0.5  # Soglia per considerare unsafe (0.0 - 1.0)
    
    print("Avvio classificazione immagini con NudeNet")
    print(f"Batch size: {BATCH_SIZE}")
    print(f"Soglia unsafe: {THRESHOLD}")
    print("-" * 50)
    
    try:
        classify_and_organize_images(batch_size=BATCH_SIZE, threshold=THRESHOLD)
    except Exception as e:
        print(f"Errore durante l'esecuzione: {str(e)}")

if __name__ == "__main__":
    main()
