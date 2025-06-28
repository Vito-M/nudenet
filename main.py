import os
import shutil
import time
from pathlib import Path
from nudenet import NudeClassifier

def setup_directories():
    """Crea le cartelle safe e unsafe se non esistono"""
    safe_dir = Path("safe")
    unsafe_dir = Path("unsafe")
    
    safe_dir.mkdir(exist_ok=True)
    unsafe_dir.mkdir(exist_ok=True)
    
    return safe_dir, unsafe_dir

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
    safe_dir, unsafe_dir = setup_directories()
    
    # Ottieni tutte le immagini dalla cartella img
    image_files = get_image_files("img")
    
    if not image_files:
        print("Nessuna immagine trovata nella cartella 'img'")
        return
    
    print(f"Trovate {len(image_files)} immagini da classificare...\n")
    
    # Inizializza il classificatore
    print("Inizializzazione del classificatore NudeNet...")
    classifier = NudeClassifier()
    
    # Classifica le immagini
    print("Classificazione in corso...\n")
    
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
                    print(f"[{processed_files}/{total_files}] UNSAFE: {filename} (probabilità: {unsafe_probability:.3f}) -> copiata in 'unsafe/'")
                else:
                    # Immagine safe
                    destination = safe_dir / filename
                    shutil.copy2(str(source_path), str(destination))
                    safe_count += 1
                    print(f"[{processed_files}/{total_files}] SAFE: {filename} (probabilità unsafe: {unsafe_probability:.3f}) -> copiata in 'safe/'")
                    
            except Exception as e:
                print(f"[{processed_files}/{total_files}] Errore nel processare {image_path}: {str(e)}")
                error_count += 1
        
        batch_start = batch_end
    
    # Calcola il tempo trascorso
    elapsed_time = time.time() - start_time
    mins, secs = divmod(elapsed_time, 60)
    
    # Riepilogo finale
    print("\n" + "="*50)
    print("RIEPILOGO CLASSIFICAZIONE:")
    print(f"Immagini safe: {safe_count}")
    print(f"Immagini unsafe: {unsafe_count}")
    print(f"Errori: {error_count}")
    print(f"Totale processate: {safe_count + unsafe_count}")
    print(f"Tempo totale di esecuzione: {int(mins)} minuti e {secs:.2f} secondi")
    print("="*50)

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
