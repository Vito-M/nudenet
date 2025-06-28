# 🔍 Sistema di Rilevamento Automatico Contenuti Illeciti

## 📖 Panoramica del Progetto

Questo sistema di rilevamento automatico utilizza il modulo **NudeNet**, una rete neurale avanzata basata su **YOLOv8** (You Only Look Once version 8) per l'identificazione e classificazione di contenuti inappropriati nelle immagini.

### 🧠 Caratteristiche Tecniche
- **Modello:** YOLOv8 ottimizzato per il rilevamento di contenuti sensibili
- **Dataset di Training:** Oltre **160.000 immagini** completamente auto-etichettate utilizzando:
  - Heat maps di classificazione
  - Tecniche ibride avanzate di labeling automatico
  - Contenuti reali fotografici
  - Illustrazioni e contenuti cartoon/anime
  - Diverse tipologie di pose e situazioni
- **Metodologia di Training:** La versione attuale di NudeNet è stata addestrata su 160.000 immagini interamente auto-etichettate utilizzando heat maps di classificazione e varie altre tecniche ibride
- **Accuratezza:** Elevata precisione nel rilevamento grazie al vasto dataset di addestramento automatizzato
- **Performance:** Processamento rapido delle immagini grazie all'architettura YOLO

### 🎯 Funzionalità
- Rilevamento automatico di contenuti inappropriati
- Supporto per formati immagine comuni (JPEG, PNG, etc.)

---

## 📋 Indice
- [⚙️ Requisiti](#️-requisiti)
- [🚀 Funzionamento del Sistema](#-funzionamento-del-sistema)
- [🪟 Windows](#-windows)
- [🐧 Linux](#-linux)
- [🔧 Istruzioni di Installazione](#-istruzioni-di-installazione)
- [✅ Note Finali](#-note-finali)

---

### ⚙️ Requisiti

- [Python 3.10+](https://www.python.org)
- Git
- Sistema operativo: Windows 10/11 o Linux (Ubuntu 18.04+, Debian 10+, CentOS 7+)

---

## 🚀 Funzionamento del Sistema

### 📁 Struttura delle Cartelle

Il sistema utilizza una struttura di cartelle specifica per organizzare le immagini durante il processo di analisi:

```
nudenet/
├── img/           # Cartella dove inserire le immagini da analizzare
├── safe/          # Immagini classificate come sicure (generate automaticamente)
├── unsafe/        # Immagini classificate come inappropriate (generate automaticamente)
├── main.py
├── requirements.txt
└── ...
```

### 🔄 Processo di Analisi

1. **Preparazione:** Inserire tutte le immagini da analizzare nella cartella `img/` del progetto
2. **Esecuzione:** Avviare il programma con `python main.py`
3. **Elaborazione:** Il sistema analizza automaticamente tutte le immagini presenti nella cartella `img/`
4. **Classificazione:** Le immagini vengono automaticamente copiate in:
   - `safe/` - Immagini classificate come appropriate e sicure
   - `unsafe/` - Immagini classificate come inappropriate o contenenti contenuti sensibili

### 📋 Formati Supportati
- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff, .tif)
- Altri formati immagine comuni

---

## 🪟 Windows

Questa guida illustra come configurare e avviare correttamente il progetto su **Windows** utilizzando **Python** (versione più recente).

### 🔧 Istruzioni di Installazione

#### 1. Installare Python

Scaricare e installare Python dal sito ufficiale: 
👉 [https://www.python.org](https://www.python.org)

Durante l'installazione:
- Spuntare l'opzione **"Add Python to PATH"**
- Verificare l'installazione eseguendo:
    ```bash
    py --version
    ```

#### 2. Scaricare il progetto

Posizionarsi in una cartella del sistema ed eseguire il seguente comando nel terminale:
```bash
git clone https://github.com/Vito-M/nudenet.git
```

#### 3. Creare un ambiente virtuale

Nel terminale, posizionarsi nella cartella principale del progetto e creare un ambiente virtuale:
```bash
cd nudenet
py -m venv myenv
```
È possibile denominare la cartella `myenv` con qualsiasi nome.

> 🔒 **Nota:** Assicurarsi che la cartella dell'ambiente virtuale sia presente nel file `.gitignore`:
```gitignore
myenv/
```

#### 4. Attivare l'ambiente virtuale

Nel terminale:
```bash
myenv\Scripts\activate
```
In questo modo, qualsiasi operazione verrà eseguita in un ambiente Python isolato, evitando problemi sul sistema principale.

#### 5. Aggiornare `pip`

PIP è il gestore di pacchetti Python e verrà utilizzato per installare tutte le librerie necessarie per far funzionare il progetto. Nel terminale:
```bash
python -m pip install --upgrade pip
```

#### 6. Installare le dipendenze necessarie

Nel file `requirements.txt` sono elencate tutte le librerie che installeremo utilizzando PIP. Nel terminale:
```bash
pip install -r requirements.txt
```

#### 7. Avviare il programma

Una volta completata la configurazione, è possibile avviare il programma. Nel terminale:
```bash
python main.py
```

---

## 🐧 Linux

Questa sezione illustra come configurare e avviare il progetto su sistemi **Linux** (Ubuntu, Debian, CentOS, etc.).

### 🔧 Istruzioni di Installazione

#### 1. Aggiornare il sistema

Prima di iniziare, aggiornare i pacchetti del sistema:

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt upgrade -y
```

**CentOS/RHEL/Fedora:**
```bash
sudo yum update -y
# o per Fedora/RHEL 8+
sudo dnf update -y
```

#### 2. Installare Python e dipendenze

**Ubuntu/Debian:**
```bash
sudo apt install python python3-venv python3-dev python3-pip git -y
```

**CentOS/RHEL:**
```bash
sudo yum install python3 python3-venv python3-devel python3-pip git -y
# o per versioni più recenti
sudo dnf install python3 python3-venv python3-devel python3-pip git -y
```

#### 3. Verificare l'installazione di Python

```bash
python3 --version
```

#### 4. Scaricare il progetto

Posizionarsi in una directory di lavoro ed eseguire:
```bash
git clone https://github.com/Vito-M/nudenet.git
cd nudenet
```

#### 5. Creare un ambiente virtuale

```bash
python3 -m venv myenv
```

#### 6. Attivare l'ambiente virtuale

```bash
source myenv/bin/activate
```

Dovrebbe apparire `(myenv)` all'inizio del prompt, indicando che l'ambiente virtuale è attivo.

#### 7. Aggiornare pip

```bash
python -m pip install --upgrade pip
```

#### 8. Installare le dipendenze

```bash
pip install -r requirements.txt
```

#### 9. Avviare il programma

```bash
python main.py
```

### 🔄 Comandi utili per Linux

**Disattivare l'ambiente virtuale:**
```bash
deactivate
```

**Riattivare l'ambiente virtuale (dalla directory del progetto):**
```bash
source myenv/bin/activate
```

**Verificare i pacchetti installati:**
```bash
pip list
```

---

## ✅ Note Finali

- **Importante:** Verificare sempre che l'ambiente virtuale sia attivato prima di installare dipendenze o eseguire il programma
- **Troubleshooting:** In caso di errori durante l'installazione delle dipendenze, assicurarsi di avere tutti i prerequisiti di sistema installati
- **Performance:** Per migliori performance su Linux, considerare l'installazione di CUDA se si dispone di una GPU NVIDIA compatibile

### 🔧 Risoluzione Problemi Comuni

**Errore di permessi su Linux:**
```bash
sudo chown -R $USER:$USER nudenet/
```

**Problemi con pip su sistemi più vecchi:**
```bash
python -m pip install --upgrade pip setuptools wheel
```

---

## 👨‍🎓 Profilo Sviluppatore

**Studente:** Vito Marchionna  
**Università:** Università degli Studi di Bari Aldo Moro  
**Corso di Laurea:** ITPS  
**Anno Accademico:** 2025  

**Competenze tecniche:**
- Python
- YOLOv8 Implementation
- Git Version Control