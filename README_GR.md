[🇬🇧 English version](README.md)

# IoT Traffic Generator

Συνθετικός generator δικτυακής κίνησης IoT που αναπτύχθηκε στο πλαίσιο πτυχιακής εργασίας.

Το σύστημα δημιουργεί τόσο κανονική όσο και κακόβουλη IoT δικτυακή κίνηση και παράγει labeled datasets για χρήση σε έρευνα και πειραματισμό στον χώρο της κυβερνοασφάλειας.

## Βασικές Λειτουργίες

- Δημιουργία συνθετικής κανονικής IoT κίνησης:
  - DNS
  - HTTP
  - MQTT

- Προσομοίωση επιθετικών σεναρίων:
  - Port Scan
  - MQTT Flood
  - DNS Exfiltration
  - Mirai-like Scanning

- Παραμετροποίηση της αναλογίας normal / attack traffic
- Παραμετροποίηση της αναλογίας των διαφορετικών attack types
- IoT device profiles
- Προσομοίωση attack bursts
- Επαναληψιμότητα μέσω random seed
- Δημιουργία PCAP μέσω Scapy
- Flow analysis μέσω Zeek
- Δημιουργία CSV datasets
- Αυτόματο labeling των flows
- Dataset validation
- Στατιστική ανάλυση
- Αυτόματη παραγωγή plots

## Τεχνολογίες

- Python 3
- Scapy
- Pandas
- Matplotlib
- TShark
- Wireshark
- Zeek
- WSL / Ubuntu

## Δομή Project

```text
iot_traffic_generator/
├── generators/
│   ├── attack_generator.py
│   ├── dns_generator.py
│   ├── http_generator.py
│   └── mqtt_generator.py
├── processing/
│   ├── dataset_pipeline.py
│   ├── plots.py
│   ├── statistics.py
│   ├── traffic_pipeline.py
│   ├── validation.py
│   ├── zeek_processor.py
│   ├── tshark_processor.py
│   ├── dataset_builder.py
│   └── feature_extractor.py
├── output/
│   ├── csv/
│   ├── logs/
│   ├── pcap/
│   └── plots/
├── config.py
├── main.py
├── requirements.txt
└── README.md
```

## Εγκατάσταση

Δημιουργία Python virtual environment:

```bash
python -m venv .venv
```

Ενεργοποίηση του virtual environment στα Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Εγκατάσταση των απαιτούμενων Python packages:

```bash
pip install -r requirements.txt
```

Τα Zeek και TShark πρέπει να εγκατασταθούν ξεχωριστά.

Η τρέχουσα υλοποίηση εκτελεί το Zeek μέσω WSL / Ubuntu.

## Παραμετροποίηση

Οι βασικές παράμετροι της δικτυακής κίνησης ορίζονται στο:

```text
config.py
```

Παράδειγμα:

```python
TOTAL_FLOWS = 10000
ATTACK_RATIO = 0.20
RANDOM_SEED = 42
```

Μέσω του `config.py` μπορούν επίσης να παραμετροποιηθούν:

- οι αναλογίες των normal protocols,
- οι αναλογίες των attack types,
- τα IoT device profiles,
- τα attack burst sizes,
- τα timing parameters.

## Εκτέλεση

Για την εκτέλεση του generator:

```bash
python main.py
```

Η βασική ροή του συστήματος είναι:

```text
Config Validation
        ↓
Traffic Generation
        ↓
Normal / Attack Mixing
        ↓
Timing και Attack Bursts
        ↓
PCAP Generation
        ↓
Zeek Flow Extraction
        ↓
Automatic Labeling
        ↓
CSV Dataset Generation
        ↓
Statistics και Plots
        ↓
Dataset Validation
```

## Παραγόμενα Αρχεία

### PCAP

```text
output/pcap/final_mixed_traffic.pcap
```

### Labeled Flow Dataset

```text
output/csv/final_flow_dataset.csv
```

### Attack Burst Statistics

```text
output/csv/attack_burst_statistics.csv
```

### Plots

```text
output/plots/
```

Παράγονται plots για:

- Flow distribution ανά label
- Protocol distribution
- Destination port distribution
- Average inter-arrival time ανά attack type

## Labels του Dataset

Το dataset περιλαμβάνει τα παρακάτω labels:

```text
normal
port_scan
mqtt_flood
dns_exfiltration
mirai_like
```

Σε ένα ενδεικτικό experiment με 10.000 flows χρησιμοποιήθηκε η ακόλουθη κατανομή:

```text
8000 normal flows
500 port scan flows
500 MQTT flood flows
500 DNS exfiltration flows
500 Mirai-like flows
```

## Επαναληψιμότητα

Χρησιμοποιείται configurable random seed ώστε τα experiments να μπορούν να αναπαραχθούν.

Παράδειγμα:

```python
RANDOM_SEED = 42
```

Με το ίδιο configuration και το ίδιο random seed μπορεί να παραχθεί το ίδιο synthetic experiment.

Η αλλαγή του random seed οδηγεί σε διαφορετικές τυχαίες επιλογές, όπως διαφορετική σειρά traffic events, ports, device selections και attack bursts.

## IoT Device Profiles

Ο generator χρησιμοποιεί διαφορετικά IoT device profiles με ξεχωριστές IP διευθύνσεις και διαφορετική πιθανότητα χρήσης των διαθέσιμων protocols.

Τα profiles περιλαμβάνουν ενδεικτικά:

- Temperature Sensor
- Smart Camera
- Thermostat
- Gateway

Με αυτόν τον τρόπο η normal κίνηση δεν προέρχεται από μία μόνο συσκευή, αλλά προσομοιώνεται ένα μικρό IoT δίκτυο με διαφορετικά patterns χρήσης.

## Attack Bursts

Τα attack events ομαδοποιούνται σε bursts τυχαίου μεγέθους.

Κάθε attack type διαθέτει διαφορετικό timing profile, ώστε να δημιουργούνται διαφορετικά χρονικά patterns.

Ενδεικτικά:

- MQTT Flood: πολύ μικρά inter-arrival times
- Mirai-like: γρήγορη σάρωση πολλών targets
- Port Scan: γρήγορη σάρωση διαφορετικών ports
- DNS Exfiltration: πιο αραιή και stealthy δραστηριότητα

## Flow Extraction και Labeling

Το παραγόμενο PCAP αναλύεται μέσω Zeek.

Από το `conn.log` εξάγονται flow-level χαρακτηριστικά όπως:

- Source IP
- Source Port
- Destination IP
- Destination Port
- Protocol
- Service
- Duration
- Original Bytes
- Response Bytes
- Original Packets
- Response Packets

Τα flows αντιστοιχίζονται αυτόματα στα metadata του generator και λαμβάνουν το κατάλληλο label.

## Στατιστική Ανάλυση

Μετά την παραγωγή του dataset υπολογίζονται αυτόματα στατιστικά όπως:

- συνολικός αριθμός flows,
- κατανομή των labels,
- κατανομή TCP / UDP,
- μέση διάρκεια flow,
- μέσος αριθμός packets ανά flow,
- μέσος αριθμός bytes,
- συχνότερα destination ports,
- στατιστικά ανά label,
- attack burst duration,
- average inter-arrival time.

## Validation

Το pipeline πραγματοποιεί αυτόματα ελέγχους για:

- τον αναμενόμενο αριθμό flows,
- missing labels,
- ορθότητα labeling,
- απαιτούμενες στήλες του dataset,
- εγκυρότητα των traffic ratios.

Ένα επιτυχημένο run ολοκληρώνεται με αποτελέσματα όπως:

```text
Flow count: OK
Missing labels: OK
Labeling: OK
Required columns: OK
```

## Ενδεικτικό Dataset

Στο τελικό experiment δημιουργήθηκαν:

```text
10.000 traffic events
27.600 raw packets
10.000 labeled Zeek flows
```

με κατανομή:

```text
80% normal traffic
20% attack traffic
```

Το attack traffic κατανέμεται ισόποσα μεταξύ των τεσσάρων attack scenarios.

## Σημειώσεις

Η παραγόμενη δικτυακή κίνηση είναι συνθετική και προορίζεται για ερευνητική και εκπαιδευτική χρήση.

Τα attack scenarios προσομοιώνουν χαρακτηριστικά μοτίβα κακόβουλης δικτυακής συμπεριφοράς χωρίς να υλοποιούν ή να εκτελούν πραγματικό malware ή πραγματικές επιθέσεις σε δίκτυα.
