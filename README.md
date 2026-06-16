# MolinaCrypto Digital Monitor

**MolinaCrypto Digital Monitor** è una dashboard desktop open source collegata a https://www.molinacrypto.eu, pensata per aggregare in un'unica interfaccia dati e contenuti su criptovalute, Web3, cybersecurity, Bitcoin Network, news live e strumenti del Security LAB.

Il programma è sviluppato in Python con interfaccia grafica Tkinter ed è pensato per essere distribuito sia come sorgente Python sia, progressivamente, come pacchetto pronto all'uso per Linux e Windows.

---

## Funzioni principali

* Dashboard iniziale con sintesi dei principali indicatori.
* Sezione Articoli collegata all'archivio di molinacrypto.eu.
* Sezione News live con feed aggregati.
* Prezzi crypto live tramite API Kraken.
* Pannello grafico semplificato per asset crypto selezionati.
* Sezione Bitcoin Network con mempool, altezza blocco e fee consigliate.
* Sezione Cybersecurity con telemetria cyber e GitHub Security Advisories.
* Sezione Security LAB con collegamenti a Risk Score Checker online, MolinaCrypto Web3 Shield, Metodo Risk Score, checklist sicurezza crypto e glossario Crypto/Web3/Cybersecurity.

---

## Informativa dati live

All'avvio il programma mostra un'informativa prima di caricare i dati live.

La dashboard può interrogare servizi esterni per mostrare dati aggiornati, tra cui:

* endpoint pubblici di molinacrypto.eu;
* Kraken API;
* mempool.space API;
* Alternative.me Fear & Greed Index;
* GitHub Advisories API.

Se l'utente rifiuta, i dati live non vengono caricati automaticamente. È comunque possibile usare l'app come punto di accesso manuale ai link e alle sezioni del progetto.

Il programma desktop non carica direttamente banner pubblicitari, Google Analytics o cookie del sito. Tali servizi possono essere caricati solo quando l'utente apre manualmente le pagine web nel browser, secondo le informative e le impostazioni privacy dei rispettivi siti.

---

## Requisiti per l'esecuzione da sorgente

Per eseguire il programma direttamente dal file Python sono richiesti:

* Python 3;
* Tkinter;
* connessione internet per i dati live.

Non sono richieste librerie Python esterne installabili con pip.

---

## Linux

Su Linux Mint, Ubuntu o distribuzioni compatibili, se Tkinter non è presente, installare il pacchetto di sistema con il comando: sudo apt install python3-tk

Avvio da sorgente: python3 MolinaCryptoDigitalMonitor.py

Nel pacchetto Linux .tar.gz è previsto anche lo script: ./avvia.sh

Le istruzioni specifiche per Linux saranno incluse nel file README_LINUX.txt presente nel pacchetto Linux.

---

## Windows

Su Windows il programma può essere eseguito da sorgente installando Python 3 con supporto Tkinter.

In una release successiva è prevista anche la distribuzione come archivio .zip con eseguibile portable .exe.

Le istruzioni specifiche per Windows saranno incluse nel file README_WINDOWS.txt presente nel pacchetto Windows.

---

## Note importanti

MolinaCrypto Digital Monitor fornisce dati e contenuti a scopo informativo.

Non costituisce:

* consulenza finanziaria;
* consulenza fiscale;
* consulenza legale;
* consulenza professionale in cybersecurity;
* raccomandazione di investimento.

Prima di prendere decisioni operative, verificare sempre le fonti ufficiali.

---

## Progetto collegato

Sito web: https://www.molinacrypto.eu/

Security LAB: https://www.molinacrypto.eu/security-lab.html

Repository GitHub dell'autore: https://github.com/molpaolo3

---

## Licenza

Questo progetto è distribuito con licenza MIT. Vedere il file LICENSE.

