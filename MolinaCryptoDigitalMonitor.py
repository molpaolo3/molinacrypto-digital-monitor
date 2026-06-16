# -*- coding: utf-8 -*-
"""
MolinaCrypto Digital Monitor v0.8 UI + Privacy Notice
Dashboard desktop open source per molinacrypto.eu.

Obiettivo versione:
- UI/UX più moderna e leggibile su Linux Mint/Windows.
- Fix consenso: dopo un rifiuto iniziale, un consenso successivo da Aggiorna tutto avvia correttamente il refresh live.
- Pulizia warning Thonny/Pylint/Mypy principali: annotazioni, root non ombreggiato, lambda nav sostituita con partial.
- Avvio massimizzato su Linux Mint/Windows, senza taglio dei pulsanti principali.
- Sezione "Risorse" trasformata in "Security LAB".
- Disclaimer iniziale con accettazione/rifiuto prima delle chiamate live a servizi esterni.
- Navigazione laterale, dashboard operativa, card sintetiche e link rapidi.
- Nessuna dipendenza esterna: solo standard library + Tkinter.
"""

import json
import threading
import time
import urllib.request
import webbrowser
from functools import partial
from typing import Any, Callable, Dict, List, Optional, Tuple
import tkinter as tk
from tkinter import ttk, messagebox


APP_TITLE = "MolinaCrypto Digital Monitor · Security Dashboard"
APP_VERSION = "v0.8"
USER_AGENT = "MolinaCryptoDigitalMonitor/0.8 (+https://www.molinacrypto.eu)"

URLS = {
    "site": "https://www.molinacrypto.eu/",
    "archive": "https://www.molinacrypto.eu/archivio.html",
    "security_lab": "https://www.molinacrypto.eu/security-lab.html",
    "risk_checker": "https://www.molinacrypto.eu/security-lab/risk-score-checker.html",
    "risk_method": "https://www.molinacrypto.eu/security-lab/metodologia-risk-score.html",
    "about": "https://www.molinacrypto.eu/aboutme.html",
    "contacts": "https://www.molinacrypto.eu/contatti.html",
    "donations": "https://www.molinacrypto.eu/donazioni.html",
    "articles": "https://www.molinacrypto.eu/data/approfondimenti-list.php",
    "home_feeds": "https://www.molinacrypto.eu/data/home-feeds.php",
    "extra_feeds": "https://www.molinacrypto.eu/data/home-feeds-extra.php",
    "world_news": "https://www.molinacrypto.eu/data/world-news.php",
    "cyber_globe_cache": "https://www.molinacrypto.eu/data/cache/cyber-globe-cache.json",
    "kraken": "https://api.kraken.com/0/public/Ticker?pair=xbteur,bcheur,etheur,soleur,xrpeur,adaeur,doteur,linkeur,avaxeur,xdgeur,bnbeur",
    "github_advisories": "https://api.github.com/advisories?per_page=15&sort=updated&direction=desc",
    "fear_greed": "https://api.alternative.me/fng/?limit=7&format=json",
    "mempool_stats": "https://mempool.space/api/mempool",
    "mempool_fees": "https://mempool.space/api/v1/fees/recommended",
    "mempool_height": "https://mempool.space/api/blocks/tip/height",
    "github_checklist": "https://github.com/molpaolo3/crypto-security-checklist-it",
    "github_glossario": "https://github.com/molpaolo3/glossario-crypto-web3-cybersecurity-it",
    "github_web3_shield": "https://github.com/molpaolo3/molinacrypto-web3-shield",
    "github_digital_monitor": "https://github.com/molpaolo3/molinacrypto-digital-monitor",
}


# ---------------------------------------------------------------------------
# Network helpers
# ---------------------------------------------------------------------------

def fetch_text(url: str, timeout: int = 15) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def fetch_json(url: str, timeout: int = 15) -> Any:
    return json.loads(fetch_text(url, timeout=timeout))


def safe(value: Any, default: str = "") -> str:
    if value is None:
        return default
    return str(value)


def shorten(value: Any, limit: int = 120) -> str:
    text = safe(value).strip().replace("\n", " ")
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 1)].rstrip() + "…"


def format_int(value: Any) -> str:
    try:
        return f"{int(value):,}".replace(",", ".")
    except Exception:
        return "—"


def format_float(value: Any, decimals: int = 2) -> str:
    try:
        return f"{float(value):,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "—"


def format_eur(value: Any) -> str:
    try:
        n = float(value)
        if n >= 1000:
            return "€ " + format_float(n, 2)
        if n >= 1:
            return "€ " + format_float(n, 4)
        return "€ " + format_float(n, 6)
    except Exception:
        return "€ —"


# ---------------------------------------------------------------------------
# UI widgets
# ---------------------------------------------------------------------------

class MetricCard(tk.Frame):
    def __init__(self, parent: tk.Widget, title: str, value: str = "—", subtitle: str = "", accent: str = "#00d4ff", **kwargs: Any) -> None:
        super().__init__(parent, bg="#0b1220", highlightthickness=1, highlightbackground="#18324f", **kwargs)
        self.accent = accent

        self.header = tk.Frame(self, bg="#0b1220")
        self.header.pack(fill="x", padx=14, pady=(12, 2))

        self.dot = tk.Label(self.header, text="●", bg="#0b1220", fg=accent, font=("DejaVu Sans", 9, "bold"))
        self.dot.pack(side="left")

        self.title_label = tk.Label(
            self.header,
            text=title,
            bg="#0b1220",
            fg="#90a8c7",
            font=("DejaVu Sans", 9, "bold"),
            anchor="w",
        )
        self.title_label.pack(side="left", padx=(6, 0), fill="x", expand=True)

        self.value_label = tk.Label(
            self,
            text=value,
            bg="#0b1220",
            fg="#eef8ff",
            font=("DejaVu Sans", 18, "bold"),
            anchor="w",
        )
        self.value_label.pack(fill="x", padx=14, pady=(2, 0))

        self.subtitle_label = tk.Label(
            self,
            text=subtitle,
            bg="#0b1220",
            fg="#6f87aa",
            font=("DejaVu Sans", 9),
            anchor="nw",
            justify="left",
            wraplength=310,
        )
        self.subtitle_label.pack(fill="both", expand=True, padx=14, pady=(4, 12))

    def set(self, value: str, subtitle: Optional[str] = None, accent: Optional[str] = None) -> None:
        self.value_label.config(text=value)
        if subtitle is not None:
            self.subtitle_label.config(text=subtitle)
        if accent:
            self.accent = accent
            self.dot.config(fg=accent)
            self.configure(highlightbackground=accent)


class MolinaCryptoApp:
    def __init__(self, root_window: tk.Tk) -> None:
        self.root = root_window
        self.root.title(APP_TITLE)
        self.root.geometry("1440x900")
        self.root.minsize(1180, 760)

        self.colors = {
            "bg": "#050b18",
            "panel": "#0b1220",
            "panel2": "#101a2e",
            "panel3": "#071021",
            "line": "#17314f",
            "text": "#dcecff",
            "muted": "#7d94b6",
            "muted2": "#566b8f",
            "accent": "#27d7ff",
            "accent2": "#1e90ff",
            "green": "#00d4a0",
            "yellow": "#ffbd4a",
            "red": "#ff4d6d",
            "purple": "#a78bfa",
            "orange": "#ff8a3d",
        }

        self.data: Dict[str, Any] = {
            "articles": [],
            "home_feeds": [],
            "extra_feeds": [],
            "world_news": [],
            "crypto": [],
            "advisories": [],
            "fng": {},
            "mempool": {},
            "globe": {},
            "loaded_at": "",
        }
        self.errors: List[str] = []
        self.pages: Dict[str, tk.Frame] = {}
        self.nav_buttons: Dict[str, tk.Button] = {}
        self.current_page: str = "dashboard"
        self.pulse_state: int = 0
        self.live_data_consent: bool = False
        self.refresh_in_progress: bool = False

        self.setup_style()
        self.build_ui()
        self.show_page("dashboard")

        # Evita la finestra ridotta su Linux Mint e lascia comunque un fallback
        # per ambienti dove lo stato "zoomed" non è supportato.
        self.root.after(80, self.maximize_window)
        # Nessuna chiamata live parte prima dell'informativa iniziale.
        self.root.after(350, self.first_startup_notice)

    # ------------------------------------------------------------------
    # Window / privacy startup notice
    # ------------------------------------------------------------------
    def maximize_window(self) -> None:
        """Avvia la finestra massimizzata, senza usare fullscreen esclusivo."""
        try:
            self.root.state("zoomed")
        except Exception:
            pass
        try:
            self.root.attributes("-zoomed", True)
        except Exception:
            pass

    def first_startup_notice(self) -> None:
        accepted = self.show_live_data_notice()
        if accepted:
            # Avvio differito per uscire puliti dalla finestra modale.
            self.root.after(50, self.refresh_all)
        else:
            self.status.config(text="Dati live non caricati: consenso non fornito. Puoi usare i link manuali e riattivare con 'Aggiorna tutto'.")
            self.status_dot.config(fg=self.colors["yellow"])

    def show_live_data_notice(self) -> bool:
        """Mostra informativa prima di qualunque interrogazione live esterna."""
        if self.live_data_consent:
            return True

        c = self.colors
        dialog = tk.Toplevel(self.root)
        dialog.title("Informativa dati live · MolinaCrypto Digital Monitor")
        dialog.configure(bg=c["bg"])
        dialog.geometry("900x650")
        dialog.minsize(780, 560)
        dialog.transient(self.root)
        dialog.grab_set()

        result: Dict[str, bool] = {"accepted": False}

        outer = tk.Frame(dialog, bg=c["bg"], padx=18, pady=16)
        outer.pack(fill="both", expand=True)

        tk.Label(
            outer,
            text="Prima di caricare i dati live",
            bg=c["bg"],
            fg=c["accent"],
            font=("DejaVu Sans", 18, "bold"),
            anchor="w",
        ).pack(fill="x")

        tk.Label(
            outer,
            text="Il programma può interrogare siti e API esterne per mostrare informazioni aggiornate. Nessuna chiamata live viene eseguita prima della tua scelta.",
            bg=c["bg"],
            fg=c["muted"],
            font=("DejaVu Sans", 10),
            anchor="w",
            justify="left",
            wraplength=840,
        ).pack(fill="x", pady=(6, 12))

        text_frame = tk.Frame(outer, bg=c["panel"], highlightthickness=1, highlightbackground=c["line"])
        text_frame.pack(fill="both", expand=True)

        notice = tk.Text(
            text_frame,
            bg=c["panel"],
            fg=c["text"],
            insertbackground=c["text"],
            relief="flat",
            wrap="word",
            font=("DejaVu Sans", 10),
            padx=14,
            pady=14,
            height=18,
        )
        scroll = ttk.Scrollbar(text_frame, orient="vertical", command=notice.yview)
        notice.configure(yscrollcommand=scroll.set)
        notice.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        notice_text = """MolinaCrypto Digital Monitor è una dashboard informativa: per funzionare in modalità live effettua richieste HTTPS verso endpoint del sito molinacrypto.eu e verso alcuni fornitori esterni.

Servizi interrogati automaticamente solo dopo accettazione:

1) molinacrypto.eu / endpoint dati del sito
- Articoli, feed news, cache cyber e dati pubblici esposti dal sito.
- Possibili dati tecnici trattati dal server/hosting: indirizzo IP, data/ora della richiesta, user-agent dell'applicazione e log tecnici necessari all'erogazione del servizio.
- L'app desktop non carica direttamente banner pubblicitari, script Google Analytics o cookie del sito: questi possono entrare in gioco solo quando apri pagine web nel browser.

2) Kraken API / Payward
- Usata per mostrare prezzi crypto e dati OHLC aggiornati.
- Possibili dati tecnici: indirizzo IP, user-agent/applicazione, data/ora della richiesta e log tecnici del servizio.
- Privacy policy: https://www.kraken.com/legal/privacy

3) mempool.space API
- Usata per mostrare dati pubblici della rete Bitcoin: mempool, altezza blocco e fee consigliate.
- Possibili dati tecnici: indirizzo IP, user-agent/applicazione, data/ora della richiesta e log tecnici del servizio.
- Privacy policy: https://mempool.space/privacy-policy

4) Alternative.me Fear & Greed Index
- Usato per mostrare indicatore e storico recente del sentiment crypto.
- Possibili dati tecnici: indirizzo IP, user-agent/applicazione, data/ora della richiesta e log tecnici del servizio.
- Privacy policy: https://alternative.me/privacy/

5) GitHub Advisories API
- Usata per mostrare advisory e vulnerabilità recenti.
- Possibili dati tecnici: indirizzo IP, user-agent/applicazione, data/ora della richiesta e log tecnici del servizio GitHub.
- Privacy statement: https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement

Link aperti manualmente dall'utente:
- I pulsanti verso Security LAB, sito, archivio, GitHub repository, checklist e glossario aprono pagine nel browser. In quel caso si applicano le informative, i cookie banner e le impostazioni privacy dei rispettivi siti visitati.
- Google Analytics, Iubenda, Altervista Ads o altri script non vengono eseguiti dentro questa app desktop; possono essere caricati solo dalle pagine web aperte nel browser, secondo il consenso espresso sul sito.

Finalità:
- visualizzazione di dati pubblici aggiornati su crypto, Bitcoin Network, cybersecurity, contenuti editoriali e news.

Nota:
- i dati sono informativi e non costituiscono consulenza finanziaria, legale, fiscale o di cybersecurity professionale.

Scegli "Accetta e carica dati live" per abilitare le chiamate esterne in questa sessione. Scegli "Rifiuta" per usare l'app senza caricare dati live automatici."""
        notice.insert("end", notice_text)
        notice.configure(state="disabled")

        button_row = tk.Frame(outer, bg=c["bg"])
        button_row.pack(fill="x", pady=(14, 0))

        def accept():
            result["accepted"] = True
            self.live_data_consent = True
            dialog.destroy()

        def reject():
            result["accepted"] = False
            self.live_data_consent = False
            dialog.destroy()

        dialog.protocol("WM_DELETE_WINDOW", reject)

        reject_btn = tk.Button(
            button_row,
            text="Rifiuta dati live",
            command=reject,
            bg=c["panel"],
            fg=c["text"],
            activebackground=c["panel2"],
            activeforeground=c["accent"],
            relief="flat",
            cursor="hand2",
            font=("DejaVu Sans", 10, "bold"),
            padx=14,
            pady=9,
        )
        reject_btn.pack(side="right", padx=(8, 0))

        accept_btn = tk.Button(
            button_row,
            text="Accetta e carica dati live",
            command=accept,
            bg=c["accent2"],
            fg="white",
            activebackground="#38bdf8",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            font=("DejaVu Sans", 10, "bold"),
            padx=14,
            pady=9,
        )
        accept_btn.pack(side="right")

        tk.Label(
            button_row,
            text="La scelta vale per questa sessione dell'app.",
            bg=c["bg"],
            fg=c["muted2"],
            font=("DejaVu Sans", 8),
            anchor="w",
        ).pack(side="left")

        dialog.update_idletasks()
        try:
            x = self.root.winfo_x() + max(0, (self.root.winfo_width() - dialog.winfo_width()) // 2)
            y = self.root.winfo_y() + max(0, (self.root.winfo_height() - dialog.winfo_height()) // 2)
            dialog.geometry(f"+{x}+{y}")
        except Exception:
            pass

        dialog.wait_window()
        return result["accepted"]

    # ------------------------------------------------------------------
    # Styling
    # ------------------------------------------------------------------
    def setup_style(self) -> None:
        c = self.colors
        self.root.configure(bg=c["bg"])
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=c["panel"],
            foreground=c["text"],
            fieldbackground=c["panel"],
            bordercolor=c["line"],
            rowheight=34,
            font=("DejaVu Sans", 9),
        )
        style.configure(
            "Treeview.Heading",
            background=c["panel2"],
            foreground=c["accent"],
            bordercolor=c["line"],
            font=("DejaVu Sans", 9, "bold"),
        )
        style.map(
            "Treeview",
            background=[("selected", c["accent2"])],
            foreground=[("selected", "white")],
        )

        style.configure(
            "Vertical.TScrollbar",
            background=c["panel2"],
            troughcolor=c["panel"],
            bordercolor=c["line"],
            arrowcolor=c["accent"],
        )
        style.configure(
            "TCombobox",
            fieldbackground=c["panel"],
            background=c["panel2"],
            foreground=c["text"],
            arrowcolor=c["accent"],
        )

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------
    def build_ui(self) -> None:
        c = self.colors
        self.shell = tk.Frame(self.root, bg=c["bg"])
        self.shell.pack(fill="both", expand=True)

        self.sidebar = tk.Frame(self.shell, bg="#071021", width=235, highlightthickness=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.main = tk.Frame(self.shell, bg=c["bg"])
        self.main.pack(side="right", fill="both", expand=True)

        self.build_sidebar()
        self.build_topbar()
        self.build_pages()
        self.build_statusbar()

    def build_sidebar(self) -> None:
        c = self.colors
        brand = tk.Frame(self.sidebar, bg="#071021")
        brand.pack(fill="x", padx=16, pady=(18, 16))

        logo_row = tk.Frame(brand, bg="#071021")
        logo_row.pack(fill="x")

        logo = tk.Label(
            logo_row,
            text="M",
            bg="#0b3d91",
            fg="#ffffff",
            font=("DejaVu Sans", 24, "bold"),
            width=2,
            height=1,
        )
        logo.pack(side="left")

        brand_text = tk.Frame(logo_row, bg="#071021")
        brand_text.pack(side="left", padx=(10, 0), fill="x", expand=True)

        tk.Label(
            brand_text,
            text="molinacrypto",
            bg="#071021",
            fg=c["text"],
            font=("DejaVu Sans", 13, "bold"),
            anchor="w",
        ).pack(fill="x")
        tk.Label(
            brand_text,
            text="Digital Monitor",
            bg="#071021",
            fg=c["accent"],
            font=("DejaVu Sans", 9, "bold"),
            anchor="w",
        ).pack(fill="x")

        tk.Label(
            brand,
            text="Crypto · Web3 · Cyber intelligence",
            bg="#071021",
            fg=c["muted2"],
            font=("DejaVu Sans", 8),
            anchor="w",
        ).pack(fill="x", pady=(9, 0))

        sep = tk.Frame(self.sidebar, bg="#102342", height=1)
        sep.pack(fill="x", padx=16, pady=(0, 12))

        nav_items = [
            ("dashboard", "Dashboard", "●"),
            ("articles", "Articoli", "◆"),
            ("news", "News live", "◌"),
            ("crypto", "Crypto live", "₿"),
            ("security", "Security LAB", "⚡"),
            ("cyber", "Cybersecurity", "▣"),
            ("bitcoin", "Bitcoin Network", "▤"),
        ]

        for page, text, icon in nav_items:
            btn = self.nav_button(page, text, icon)
            btn.pack(fill="x", padx=12, pady=4)
            self.nav_buttons[page] = btn

        bottom = tk.Frame(self.sidebar, bg="#071021")
        bottom.pack(side="bottom", fill="x", padx=12, pady=14)

        self.security_lab_button = tk.Button(
            bottom,
            text="⚡ Apri Security LAB",
            command=lambda: webbrowser.open(URLS["security_lab"]),
            bg="#0f766e",
            fg="white",
            activebackground="#14b8a6",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            font=("DejaVu Sans", 10, "bold"),
            padx=10,
            pady=9,
        )
        self.security_lab_button.pack(fill="x", pady=(0, 8))

        self.small_button(bottom, "Risk Checker", lambda: webbrowser.open(URLS["risk_checker"])).pack(fill="x", pady=3)
        self.small_button(bottom, "GitHub repo", lambda: webbrowser.open(URLS["github_digital_monitor"])).pack(fill="x", pady=3)
        self.animate_security_button()

    def nav_button(self, page: str, text: str, icon: str) -> tk.Button:
        c = self.colors
        return tk.Button(
            self.sidebar,
            text=f" {icon}  {text}",
            command=partial(self.show_page, page),
            anchor="w",
            bg="#071021",
            fg=c["muted"],
            activebackground="#102342",
            activeforeground=c["text"],
            relief="flat",
            cursor="hand2",
            font=("DejaVu Sans", 10, "bold"),
            padx=12,
            pady=10,
        )

    def animate_security_button(self) -> None:
        palette = ["#0f766e", "#0891b2", "#1e90ff", "#14b8a6"]
        self.pulse_state = (self.pulse_state + 1) % len(palette)
        try:
            self.security_lab_button.config(bg=palette[self.pulse_state], activebackground=palette[(self.pulse_state + 1) % len(palette)])
        except Exception:
            return
        self.root.after(900, self.animate_security_button)

    def build_topbar(self) -> None:
        c = self.colors
        self.topbar = tk.Frame(self.main, bg=c["bg"])
        self.topbar.pack(fill="x", padx=22, pady=(18, 12))

        left = tk.Frame(self.topbar, bg=c["bg"])
        left.pack(side="left", fill="x", expand=True)

        self.page_title = tk.Label(
            left,
            text="Dashboard operativa",
            bg=c["bg"],
            fg=c["text"],
            font=("DejaVu Sans", 22, "bold"),
            anchor="w",
        )
        self.page_title.pack(fill="x")

        self.page_subtitle = tk.Label(
            left,
            text="Vista rapida su sito, crypto, cyber risk, Bitcoin network e contenuti live.",
            bg=c["bg"],
            fg=c["muted"],
            font=("DejaVu Sans", 10),
            anchor="w",
        )
        self.page_subtitle.pack(fill="x", pady=(3, 0))

        right = tk.Frame(self.topbar, bg=c["bg"])
        right.pack(side="right", padx=(12, 0))

        self.primary_button(right, "Aggiorna tutto", self.refresh_all).pack(side="right", padx=(8, 0))
        self.ghost_button(right, "Apri sito", lambda: webbrowser.open(URLS["site"])).pack(side="right", padx=(8, 0))
        self.ghost_button(right, "Archivio", lambda: webbrowser.open(URLS["archive"])).pack(side="right", padx=(8, 0))

    def build_pages(self) -> None:
        self.page_container = tk.Frame(self.main, bg=self.colors["bg"])
        self.page_container.pack(fill="both", expand=True, padx=22, pady=(0, 10))

        for name in ["dashboard", "articles", "news", "crypto", "security", "cyber", "bitcoin"]:
            frame = tk.Frame(self.page_container, bg=self.colors["bg"])
            self.pages[name] = frame

        self.build_dashboard_page(self.pages["dashboard"])
        self.build_articles_page(self.pages["articles"])
        self.build_news_page(self.pages["news"])
        self.build_crypto_page(self.pages["crypto"])
        self.build_security_page(self.pages["security"])
        self.build_cyber_page(self.pages["cyber"])
        self.build_bitcoin_page(self.pages["bitcoin"])

    def build_statusbar(self) -> None:
        c = self.colors
        self.statusbar = tk.Frame(self.main, bg=c["panel3"], height=28)
        self.statusbar.pack(fill="x", side="bottom")
        self.statusbar.pack_propagate(False)

        self.status_dot = tk.Label(self.statusbar, text="●", bg=c["panel3"], fg=c["yellow"], font=("DejaVu Sans", 8, "bold"))
        self.status_dot.pack(side="left", padx=(22, 6))

        self.status = tk.Label(
            self.statusbar,
            text="Pronto.",
            bg=c["panel3"],
            fg=c["muted"],
            font=("DejaVu Sans", 8),
            anchor="w",
        )
        self.status.pack(side="left", fill="x", expand=True)

        self.version_label = tk.Label(
            self.statusbar,
            text=f"{APP_VERSION} · dati informativi, non consulenza",
            bg=c["panel3"],
            fg=c["muted2"],
            font=("DejaVu Sans", 8),
            anchor="e",
        )
        self.version_label.pack(side="right", padx=22)

    def show_page(self, name: str) -> None:
        for page in self.pages.values():
            page.pack_forget()
        self.pages[name].pack(fill="both", expand=True)
        self.current_page = name

        titles = {
            "dashboard": ("Dashboard operativa", "Sintesi rapida dei segnali principali: contenuti, mercato, rischio digitale e network Bitcoin."),
            "articles": ("Articoli molinacrypto.eu", "Archivio locale dei contenuti caricati dal sito, con filtri e ricerca rapida."),
            "news": ("News live", "Feed esterni aggregati in una vista unica: crypto, Web3, cybersecurity e AI."),
            "crypto": ("Crypto live", "Prezzi Kraken, variazioni 24h e pannello grafico OHLC semplificato."),
            "security": ("Security LAB", "Centro operativo: Risk Checker, Web3 Shield, metodo, checklist e glossario."),
            "cyber": ("Cybersecurity", "Telemetria cyber e advisory recenti per leggere il rischio digitale."),
            "bitcoin": ("Bitcoin Network", "Mempool, fee rate e stato operativo della rete Bitcoin."),
        }
        title, subtitle = titles.get(name, ("MolinaCrypto", ""))
        self.page_title.config(text=title)
        self.page_subtitle.config(text=subtitle)

        for key, btn in self.nav_buttons.items():
            if key == name:
                btn.config(bg="#102342", fg=self.colors["accent"], activebackground="#102342")
            else:
                btn.config(bg="#071021", fg=self.colors["muted"], activebackground="#102342")

    # ------------------------------------------------------------------
    # Buttons / components
    # ------------------------------------------------------------------
    def primary_button(self, parent: tk.Widget, text: str, command: Callable[[], Any]) -> tk.Button:
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=self.colors["accent2"],
            fg="white",
            activebackground="#38bdf8",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            font=("DejaVu Sans", 9, "bold"),
            padx=13,
            pady=8,
        )

    def ghost_button(self, parent: tk.Widget, text: str, command: Callable[[], Any]) -> tk.Button:
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=self.colors["panel"],
            fg=self.colors["text"],
            activebackground=self.colors["panel2"],
            activeforeground=self.colors["accent"],
            relief="flat",
            cursor="hand2",
            font=("DejaVu Sans", 9, "bold"),
            padx=13,
            pady=8,
        )

    def small_button(self, parent: tk.Widget, text: str, command: Callable[[], Any]) -> tk.Button:
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg="#0b1220",
            fg=self.colors["text"],
            activebackground="#102342",
            activeforeground=self.colors["accent"],
            relief="flat",
            cursor="hand2",
            font=("DejaVu Sans", 8, "bold"),
            padx=9,
            pady=7,
        )

    def section_label(self, parent, title, subtitle=None):
        c = self.colors
        box = tk.Frame(parent, bg=c["bg"])
        box.pack(fill="x", pady=(0, 10))
        tk.Label(
            box,
            text=title,
            bg=c["bg"],
            fg=c["accent"],
            font=("DejaVu Sans", 13, "bold"),
            anchor="w",
        ).pack(fill="x")
        if subtitle:
            tk.Label(
                box,
                text=subtitle,
                bg=c["bg"],
                fg=c["muted"],
                font=("DejaVu Sans", 9),
                anchor="w",
            ).pack(fill="x", pady=(2, 0))
        return box

    def panel(self, parent, bg=None, padx=12, pady=12):
        c = self.colors
        return tk.Frame(parent, bg=bg or c["panel"], highlightthickness=1, highlightbackground=c["line"], padx=padx, pady=pady)

    def make_table(self, parent, columns, height=None):
        outer = tk.Frame(parent, bg=self.colors["bg"])
        outer.pack(fill="both", expand=True)
        tree = ttk.Treeview(outer, columns=[c[0] for c in columns], show="headings", height=height)
        for key, label, width, *extra in columns:
            anchor = extra[0] if extra else "w"
            stretch = extra[1] if len(extra) > 1 else True
            tree.heading(key, text=label)
            tree.column(key, width=width, anchor=anchor, stretch=stretch)

        scroll_y = ttk.Scrollbar(outer, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll_y.set)
        tree.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

        tree.tag_configure("positive", foreground=self.colors["green"])
        tree.tag_configure("negative", foreground=self.colors["red"])
        tree.tag_configure("warning", foreground=self.colors["yellow"])
        tree.tag_configure("muted", foreground=self.colors["muted"])
        return tree

    def clear_table(self, tree):
        for item in tree.get_children():
            tree.delete(item)

    def open_from_tree(self, tree, url_index):
        selected = tree.selection()
        if not selected:
            return
        values = tree.item(selected[0], "values")
        if len(values) > url_index and values[url_index]:
            webbrowser.open(values[url_index])

    # ------------------------------------------------------------------
    # Pages
    # ------------------------------------------------------------------
    def build_dashboard_page(self, parent):
        c = self.colors
        hero = self.panel(parent, bg="#081225", padx=18, pady=16)
        hero.pack(fill="x", pady=(0, 14))

        tk.Label(
            hero,
            text="Controlla il contesto prima di cliccare, firmare o collegare il wallet.",
            bg="#081225",
            fg=c["text"],
            font=("DejaVu Sans", 17, "bold"),
            anchor="w",
            justify="left",
            wraplength=1000,
        ).pack(fill="x")
        tk.Label(
            hero,
            text="Dashboard desktop per unire sito, dati live, threat intelligence e strumenti del Security LAB.",
            bg="#081225",
            fg=c["muted"],
            font=("DejaVu Sans", 10),
            anchor="w",
            justify="left",
            wraplength=1000,
        ).pack(fill="x", pady=(6, 0))

        actions = tk.Frame(hero, bg="#081225")
        actions.pack(fill="x", pady=(12, 0))
        self.primary_button(actions, "Risk Checker online", lambda: webbrowser.open(URLS["risk_checker"])).pack(side="left", padx=(0, 8), pady=3)
        self.ghost_button(actions, "Security LAB", lambda: webbrowser.open(URLS["security_lab"])).pack(side="left", padx=(0, 8), pady=3)
        self.ghost_button(actions, "Metodo Risk Score", lambda: webbrowser.open(URLS["risk_method"])).pack(side="left", padx=(0, 8), pady=3)

        cards = tk.Frame(parent, bg=c["bg"])
        cards.pack(fill="x", pady=(0, 14))
        for col in range(3):
            cards.grid_columnconfigure(col, weight=1)

        self.card_articles = MetricCard(cards, "ULTIMI ARTICOLI", accent=c["accent"])
        self.card_crypto = MetricCard(cards, "CRYPTO LIVE", accent=c["green"])
        self.card_fng = MetricCard(cards, "FEAR & GREED", accent=c["yellow"])
        self.card_btc = MetricCard(cards, "BITCOIN NETWORK", accent=c["orange"])
        self.card_cyber = MetricCard(cards, "CYBER RISK", accent=c["red"])
        self.card_news = MetricCard(cards, "NEWS LIVE", accent=c["purple"])

        for i, card in enumerate([self.card_articles, self.card_crypto, self.card_fng, self.card_btc, self.card_cyber, self.card_news]):
            card.grid(row=i // 3, column=i % 3, sticky="nsew", padx=6, pady=6)

        bottom = tk.Frame(parent, bg=c["bg"])
        bottom.pack(fill="both", expand=True)
        bottom.grid_columnconfigure(0, weight=2)
        bottom.grid_columnconfigure(1, weight=1)
        bottom.grid_rowconfigure(0, weight=1)

        feed_panel = self.panel(bottom, padx=12, pady=12)
        feed_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        tk.Label(feed_panel, text="Radar operativo", bg=c["panel"], fg=c["accent"], font=("DejaVu Sans", 12, "bold"), anchor="w").pack(fill="x")
        tk.Label(feed_panel, text="Ultimi contenuti e segnali caricati", bg=c["panel"], fg=c["muted"], font=("DejaVu Sans", 9), anchor="w").pack(fill="x", pady=(2, 8))
        self.dashboard_feed = tk.Text(
            feed_panel,
            bg="#071021",
            fg=c["text"],
            insertbackground=c["text"],
            relief="flat",
            wrap="word",
            font=("DejaVu Sans", 9),
            padx=10,
            pady=10,
            height=7,
        )
        self.dashboard_feed.pack(fill="both", expand=True)
        self.dashboard_feed.configure(state="disabled")

        protocol_panel = self.panel(bottom, padx=12, pady=12)
        protocol_panel.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        tk.Label(protocol_panel, text="Protocollo Security LAB", bg=c["panel"], fg=c["accent"], font=("DejaVu Sans", 12, "bold"), anchor="w").pack(fill="x")
        for number, title, text in [
            ("1", "Osserva", "URL, mittente, wallet, firma, contesto."),
            ("2", "Verifica", "Fonte ufficiale, dominio, canale, urgenza."),
            ("3", "Decidi", "Se restano dubbi, non procedere."),
            ("4", "Fermati", "Mai seed phrase, private key, OTP o 2FA."),
        ]:
            row = tk.Frame(protocol_panel, bg=c["panel"])
            row.pack(fill="x", pady=6)
            badge = tk.Label(row, text=number, bg=c["accent2"], fg="white", width=2, font=("DejaVu Sans", 9, "bold"))
            badge.pack(side="left", padx=(0, 9))
            tk.Label(row, text=f"{title}: {text}", bg=c["panel"], fg=c["text"], font=("DejaVu Sans", 9), anchor="w", wraplength=280, justify="left").pack(side="left", fill="x", expand=True)

    def build_articles_page(self, parent):
        c = self.colors
        top = tk.Frame(parent, bg=c["bg"])
        top.pack(fill="x", pady=(0, 10))
        self.section_label(top, "Archivio contenuti", "Doppio click su una riga per aprire l'articolo nel browser.")

        controls = tk.Frame(top, bg=c["bg"])
        controls.pack(fill="x")
        tk.Label(controls, text="Categoria", bg=c["bg"], fg=c["muted"], font=("DejaVu Sans", 9, "bold")).pack(side="left")
        self.article_filter = tk.StringVar(value="tutti")
        combo = ttk.Combobox(controls, textvariable=self.article_filter, values=["tutti", "crypto", "cybersecurity", "digital", "web3"], state="readonly", width=18)
        combo.pack(side="left", padx=(8, 16))
        combo.bind("<<ComboboxSelected>>", lambda _event: self.populate_articles())

        tk.Label(controls, text="Cerca", bg=c["bg"], fg=c["muted"], font=("DejaVu Sans", 9, "bold")).pack(side="left")
        self.article_search = tk.StringVar(value="")
        entry = tk.Entry(controls, textvariable=self.article_search, bg=c["panel"], fg=c["text"], insertbackground=c["text"], relief="flat", font=("DejaVu Sans", 9), width=34)
        entry.pack(side="left", padx=(8, 0), ipady=6)
        entry.bind("<KeyRelease>", lambda _event: self.populate_articles())

        self.articles_tree = self.make_table(
            parent,
            [
                ("date", "Data", 120),
                ("label", "Categoria", 130),
                ("title", "Titolo", 610),
                ("url", "URL", 300),
            ],
        )
        self.articles_tree.bind("<Double-1>", lambda _event: self.open_from_tree(self.articles_tree, 3))

    def build_news_page(self, parent):
        self.section_label(parent, "Feed news", "Main, Extra e World news in una tabella unica.")
        self.news_tree = self.make_table(
            parent,
            [
                ("type", "Tipo", 90),
                ("date", "Data", 105),
                ("source", "Fonte", 140),
                ("category", "Categoria", 130),
                ("title", "Titolo", 600),
                ("url", "URL", 320),
            ],
        )
        self.news_tree.bind("<Double-1>", lambda _event: self.open_from_tree(self.news_tree, 5))

    def build_crypto_page(self, parent):
        c = self.colors
        top = tk.Frame(parent, bg=c["bg"])
        top.pack(fill="x", pady=(0, 10))
        self.section_label(top, "Crypto Live", "Prezzi live da Kraken. Doppio click su un asset per aprire il pannello grafico.")
        row = tk.Frame(top, bg=c["bg"])
        row.pack(fill="x")
        self.primary_button(row, "Apri pannello asset / grafici", self.open_crypto_panel).pack(side="right")

        self.crypto_tree = self.make_table(
            parent,
            [
                ("asset", "Asset", 80),
                ("label", "Nome", 145),
                ("price", "Prezzo EUR", 150),
                ("change", "Var. 24h", 115),
                ("high", "Max 24h", 145),
                ("low", "Min 24h", 145),
                ("volume", "Volume", 140),
            ],
        )
        self.crypto_tree.bind("<Double-1>", self.open_selected_crypto_from_main_table)

    def build_security_page(self, parent):
        c = self.colors
        self.section_label(parent, "Security LAB", "Checker online, tool desktop, metodo, repository, checklist e knowledge base.")

        grid = tk.Frame(parent, bg=c["bg"])
        grid.pack(fill="both", expand=True)
        for col in range(3):
            grid.grid_columnconfigure(col, weight=1)
        for row in range(2):
            grid.grid_rowconfigure(row, weight=1)

        cards = [
            ("Risk Score Checker", "Analizza SMS, email, URL, wallet, contract e richieste di firma sospette direttamente dal browser.", "Apri checker", URLS["risk_checker"], c["accent"]),
            ("MolinaCrypto Web3 Shield", "Tool desktop per controlli preliminari su link, wallet pubblici, smart contract EVM, firme e pattern phishing Web3.", "Repository", URLS["github_web3_shield"], c["green"]),
            ("Digital Monitor", "Dashboard desktop per crypto, Web3, cybersecurity, Bitcoin network e news live in un unico ambiente operativo.", "Repository", URLS["github_digital_monitor"], c["purple"]),
            ("Metodo Risk Score", "Scala 100/100 basso rischio e 0/100 alto rischio, con fattori osservati e motivazioni leggibili.", "Leggi metodo", URLS["risk_method"], c["yellow"]),
            ("Glossario Crypto/Web3/Cyber", "Knowledge base italiana per orientarsi tra blockchain, wallet, smart contract, phishing, AI e sicurezza digitale.", "Apri glossario", URLS["github_glossario"], c["orange"]),
            ("Crypto Security Checklist", "Checklist pratica per evitare errori impulsivi prima di cliccare, firmare, scaricare o collegare il wallet.", "Apri checklist", URLS["github_checklist"], c["red"]),
        ]

        for index, (title, text, btn_text, url, accent) in enumerate(cards):
            card = self.panel(grid, padx=14, pady=14)
            card.grid(row=index // 3, column=index % 3, sticky="nsew", padx=6, pady=6)
            tk.Label(card, text="●", bg=c["panel"], fg=accent, font=("DejaVu Sans", 10, "bold")).pack(anchor="w")
            tk.Label(card, text=title, bg=c["panel"], fg=c["text"], font=("DejaVu Sans", 13, "bold"), anchor="w", justify="left", wraplength=280).pack(fill="x", pady=(4, 6))
            tk.Label(card, text=text, bg=c["panel"], fg=c["muted"], font=("DejaVu Sans", 9), anchor="nw", justify="left", wraplength=300).pack(fill="both", expand=True)
            self.primary_button(card, btn_text, lambda u=url: webbrowser.open(u)).pack(anchor="w", pady=(12, 0))

    def build_cyber_page(self, parent):
        c = self.colors
        self.section_label(parent, "Cyber Threat Intelligence", "Telemetria aggregata dal sito e ultime vulnerabilità GitHub Advisory.")
        self.globe_summary = tk.Label(
            parent,
            text="Cyber globe: in attesa dati…",
            bg=c["panel"],
            fg=c["text"],
            font=("DejaVu Sans", 10),
            justify="left",
            anchor="w",
            padx=12,
            pady=10,
            highlightthickness=1,
            highlightbackground=c["line"],
        )
        self.globe_summary.pack(fill="x", pady=(0, 10))

        panes = tk.PanedWindow(parent, bg=c["bg"], sashwidth=6, sashrelief="flat", orient="vertical")
        panes.pack(fill="both", expand=True)

        telemetry_box = tk.Frame(panes, bg=c["bg"])
        adv_box = tk.Frame(panes, bg=c["bg"])
        panes.add(telemetry_box, minsize=180)
        panes.add(adv_box, minsize=180)

        tk.Label(telemetry_box, text="Telemetria cyber recente", bg=c["bg"], fg=c["accent"], font=("DejaVu Sans", 11, "bold"), anchor="w").pack(fill="x", pady=(0, 6))
        self.telemetry_tree = self.make_table(
            telemetry_box,
            [
                ("source", "Sorgente", 150),
                ("target", "Target", 150),
                ("category", "Categoria", 130),
                ("severity", "Severità", 100),
                ("description", "Evento", 600),
            ],
        )

        tk.Label(adv_box, text="Ultime vulnerabilità GitHub Advisory", bg=c["bg"], fg=c["accent"], font=("DejaVu Sans", 11, "bold"), anchor="w").pack(fill="x", pady=(8, 6))
        self.cyber_tree = self.make_table(
            adv_box,
            [
                ("severity", "Severity", 105),
                ("id", "ID", 185),
                ("date", "Aggiornato", 105),
                ("summary", "Descrizione", 670),
                ("url", "URL", 280),
            ],
        )
        self.cyber_tree.bind("<Double-1>", lambda _event: self.open_from_tree(self.cyber_tree, 4))

    def build_bitcoin_page(self, parent):
        c = self.colors
        self.section_label(parent, "Bitcoin Network", "Stato mempool, fee consigliate e blocco corrente.")
        self.btc_text = tk.Text(
            parent,
            bg=c["panel"],
            fg=c["text"],
            insertbackground=c["text"],
            relief="flat",
            wrap="word",
            font=("DejaVu Sans Mono", 11),
            padx=16,
            pady=16,
        )
        self.btc_text.pack(fill="both", expand=True)
        self.btc_text.insert("end", "Caricamento dati Bitcoin Network…\n")
        self.btc_text.configure(state="disabled")

    # ------------------------------------------------------------------
    # Data loading
    # ------------------------------------------------------------------
    def refresh_all(self) -> None:
        if self.refresh_in_progress:
            self.status.config(text="Aggiornamento già in corso…")
            return

        if not self.live_data_consent:
            accepted = self.show_live_data_notice()
            if not accepted:
                self.status.config(text="Aggiornamento annullato: consenso ai dati live non fornito.")
                self.status_dot.config(fg=self.colors["yellow"])
                return
            # Fix: quando l'utente prima rifiuta e poi accetta da Aggiorna tutto,
            # il refresh viene lanciato dopo la chiusura effettiva del dialog.
            self.root.after(50, self.refresh_all)
            return

        self.refresh_in_progress = True
        self.status.config(text="Aggiornamento in corso…")
        self.status_dot.config(fg=self.colors["yellow"])
        threading.Thread(target=self.load_all_data, daemon=True).start()

    def load_all_data(self) -> None:
        errors: List[str] = []

        def try_load(label: str, func: Callable[[], Any], target_key: Optional[str] = None) -> None:
            try:
                value = func()
                if target_key:
                    self.data[target_key] = value
            except Exception as exc:
                errors.append(f"{label}: {exc}")

        try_load("Articoli", lambda: fetch_json(URLS["articles"]).get("items", []), "articles")
        try_load("News principali", lambda: fetch_json(URLS["home_feeds"]).get("items", []), "home_feeds")
        try_load("News extra", lambda: fetch_json(URLS["extra_feeds"]).get("items", []), "extra_feeds")
        try_load("World news", lambda: fetch_json(URLS["world_news"]).get("items", []), "world_news")
        try_load("Cyber globe cache", lambda: fetch_json(URLS["cyber_globe_cache"]), "globe")
        try_load("Kraken", lambda: self.parse_kraken(fetch_json(URLS["kraken"])), "crypto")
        def load_github_advisories() -> List[Dict[str, Any]]:
            advisories = fetch_json(URLS["github_advisories"])
            return advisories if isinstance(advisories, list) else []
        try_load("GitHub advisories", load_github_advisories, "advisories")
        try_load("Fear & Greed", lambda: fetch_json(URLS["fear_greed"]), "fng")

        def load_mempool() -> Dict[str, Any]:
            return {
                "stats": fetch_json(URLS["mempool_stats"]),
                "fees": fetch_json(URLS["mempool_fees"]),
                "height": fetch_text(URLS["mempool_height"]).strip(),
            }
        try_load("Mempool", load_mempool, "mempool")

        self.data["loaded_at"] = time.strftime("%d/%m/%Y %H:%M:%S")
        self.errors = errors
        self.root.after(0, self.update_ui)

    def parse_kraken(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        result = data.get("result", {})
        assets: List[Dict[str, Any]] = [
            {"asset": "BTC", "label": "Bitcoin", "keys": ["XXBTZEUR", "XBTEUR"], "ohlc": "XBTEUR"},
            {"asset": "BCH", "label": "Bitcoin Cash", "keys": ["BCHEUR", "BCHZEUR"], "ohlc": "BCHEUR"},
            {"asset": "ETH", "label": "Ethereum", "keys": ["XETHZEUR", "ETHEUR"], "ohlc": "ETHEUR"},
            {"asset": "SOL", "label": "Solana", "keys": ["SOLEUR"], "ohlc": "SOLEUR"},
            {"asset": "XRP", "label": "XRP", "keys": ["XXRPZEUR", "XRPEUR"], "ohlc": "XRPEUR"},
            {"asset": "ADA", "label": "Cardano", "keys": ["ADAEUR"], "ohlc": "ADAEUR"},
            {"asset": "DOT", "label": "Polkadot", "keys": ["DOTEUR"], "ohlc": "DOTEUR"},
            {"asset": "LINK", "label": "Chainlink", "keys": ["LINKEUR"], "ohlc": "LINKEUR"},
            {"asset": "AVAX", "label": "Avalanche", "keys": ["AVAXEUR"], "ohlc": "AVAXEUR"},
            {"asset": "DOGE", "label": "Dogecoin", "keys": ["XDGEUR", "XDGZEUR", "DOGEEUR"], "ohlc": "XDGEUR"},
            {"asset": "BNB", "label": "BNB", "keys": ["BNBEUR"], "ohlc": "BNBEUR"},
        ]
        rows: List[Dict[str, Any]] = []
        for asset_info in assets:
            key = next((k for k in asset_info["keys"] if k in result), None)
            if not key:
                continue
            item = result[key]
            last = float(item.get("c", [0])[0])
            open_price = float(item.get("o", 0))
            high = float(item.get("h", [0, 0])[1])
            low = float(item.get("l", [0, 0])[1])
            volume = float(item.get("v", [0, 0])[1])
            change = ((last - open_price) / open_price) * 100 if open_price else 0.0
            rows.append({
                "asset": asset_info["asset"],
                "label": asset_info["label"],
                "ohlc": asset_info["ohlc"],
                "price": last,
                "change": change,
                "high": high,
                "low": low,
                "volume": volume,
            })
        rows.sort(key=lambda row: row["asset"] != "BTC")
        return rows

    # ------------------------------------------------------------------
    # Populate UI
    # ------------------------------------------------------------------
    def update_ui(self) -> None:
        self.refresh_in_progress = False
        self.populate_dashboard()
        self.populate_articles()
        self.populate_news()
        self.populate_crypto()
        self.populate_cyber()
        self.populate_bitcoin()

        if self.errors:
            self.status.config(text=f"Aggiornato con {len(self.errors)} avvisi · ultimo refresh {self.data.get('loaded_at', '—')}")
            self.status_dot.config(fg=self.colors["yellow"])
        else:
            self.status.config(text=f"Aggiornamento completato · ultimo refresh {self.data.get('loaded_at', '—')}")
            self.status_dot.config(fg=self.colors["green"])

    def populate_dashboard(self) -> None:
        articles = self.data["articles"]
        crypto = self.data["crypto"]
        fng = self.data["fng"]
        mempool = self.data["mempool"]
        globe = self.data["globe"]
        advisories = self.data["advisories"]
        home = self.data["home_feeds"]
        extra = self.data["extra_feeds"]
        world = self.data["world_news"]

        if articles:
            latest = articles[0]
            self.card_articles.set(
                str(len(articles)),
                f"Ultimo: {shorten(latest.get('title'), 88)}\n{latest.get('label', '—')} · {latest.get('date_human', latest.get('date', '—'))}",
            )
        else:
            self.card_articles.set("—", "Articoli non disponibili")

        if crypto:
            top = max(crypto, key=lambda row: row.get("change", 0))
            btc = next((row for row in crypto if row.get("asset") == "BTC"), crypto[0])
            sign = "+" if top["change"] >= 0 else ""
            self.card_crypto.set(
                format_eur(btc.get("price")),
                f"BTC/EUR · top mover {top['asset']} {sign}{top['change']:.2f}%",
                accent=self.colors["green"] if btc.get("change", 0) >= 0 else self.colors["red"],
            )
        else:
            self.card_crypto.set("—", "Prezzi non disponibili")

        if fng and fng.get("data"):
            today = fng["data"][0]
            value = safe(today.get("value", "—"))
            cls = safe(today.get("value_classification", "—"))
            accent = self.colors["green"] if value.isdigit() and int(value) >= 50 else self.colors["yellow"]
            self.card_fng.set(f"{value}/100", cls, accent=accent)
        else:
            self.card_fng.set("—", "Fear & Greed non disponibile")

        if mempool:
            stats = mempool.get("stats", {})
            fees = mempool.get("fees", {})
            self.card_btc.set(
                f"#{mempool.get('height', '—')}",
                f"Tx mempool: {format_int(stats.get('count'))}\nFastest: {fees.get('fastestFee', '—')} sat/vB · Min: {fees.get('minimumFee', '—')} sat/vB",
            )
        else:
            self.card_btc.set("—", "Bitcoin Network non disponibile")

        if globe:
            stats = globe.get("stats", {})
            self.card_cyber.set(
                format_int(stats.get("events_sampled")),
                f"Paesi sorgente: {stats.get('source_countries', '—')} · target: {stats.get('target_countries', '—')}\nAdvisory GitHub: {len(advisories)}",
            )
        else:
            self.card_cyber.set(str(len(advisories)) if advisories else "—", "Cyber cache non disponibile")

        news_total = len(home) + len(extra) + len(world)
        first_news = (home or extra or world or [{}])[0]
        self.card_news.set(
            str(news_total) if news_total else "—",
            f"Main {len(home)} · Extra {len(extra)} · World {len(world)}\n{shorten(first_news.get('title', 'Nessuna news disponibile'), 85)}",
        )

        lines: List[str] = []
        if articles:
            lines.append(f"ARTICOLO · {articles[0].get('label', '—')} · {shorten(articles[0].get('title'), 120)}")
        if home:
            lines.append(f"NEWS · {home[0].get('source', '—')} · {shorten(home[0].get('title'), 120)}")
        if advisories:
            adv = advisories[0]
            lines.append(f"ADVISORY · {(adv.get('severity') or '').upper()} · {adv.get('cve_id') or adv.get('ghsa_id') or 'ADVISORY'} · {shorten(adv.get('summary'), 100)}")
        if mempool:
            lines.append(f"BITCOIN · blocco {mempool.get('height', '—')} · tx mempool {format_int(mempool.get('stats', {}).get('count'))}")
        if crypto:
            btc = next((row for row in crypto if row.get("asset") == "BTC"), crypto[0])
            lines.append(f"MARKET · BTC/EUR {format_eur(btc.get('price'))} · var. 24h {btc.get('change', 0):+.2f}%")
        if self.errors:
            lines.append("")
            lines.append("AVVISI CARICAMENTO")
            lines.extend([f"- {error}" for error in self.errors[:6]])

        self.dashboard_feed.configure(state="normal")
        self.dashboard_feed.delete("1.0", "end")
        self.dashboard_feed.insert("end", "\n".join(lines) if lines else "In attesa dati…")
        self.dashboard_feed.configure(state="disabled")

    def populate_articles(self) -> None:
        self.clear_table(self.articles_tree)
        selected = self.article_filter.get() if hasattr(self, "article_filter") else "tutti"
        query = self.article_search.get().strip().lower() if hasattr(self, "article_search") else ""

        for item in self.data["articles"]:
            category = safe(item.get("category", "")).lower()
            label = safe(item.get("label", "")).lower()
            title = safe(item.get("title", ""))
            if selected != "tutti" and selected not in category and selected not in label:
                continue
            haystack = f"{title} {category} {label} {item.get('date_human', '')}".lower()
            if query and query not in haystack:
                continue
            self.articles_tree.insert(
                "",
                "end",
                values=(
                    item.get("date_human", item.get("date", "")),
                    item.get("label", item.get("category", "")),
                    title,
                    item.get("url", ""),
                ),
            )

    def populate_news(self) -> None:
        self.clear_table(self.news_tree)
        combined: List[Tuple[str, Dict[str, Any]]] = []
        combined.extend(("Main", item) for item in self.data["home_feeds"])
        combined.extend(("Extra", item) for item in self.data["extra_feeds"])
        combined.extend(("World", item) for item in self.data["world_news"])

        for kind, item in combined:
            self.news_tree.insert(
                "",
                "end",
                values=(
                    kind,
                    safe(item.get("published_at", item.get("date", "")))[:10],
                    item.get("source", ""),
                    item.get("slot") or item.get("category") or item.get("cat", ""),
                    item.get("title", ""),
                    item.get("url", ""),
                ),
            )

    def populate_crypto(self) -> None:
        self.clear_table(self.crypto_tree)
        rows = sorted(self.data["crypto"], key=lambda row: row.get("asset") != "BTC")
        for item in rows:
            change = item.get("change", 0)
            tag = "positive" if change >= 0 else "negative"
            self.crypto_tree.insert(
                "",
                "end",
                values=(
                    item.get("asset", ""),
                    item.get("label", ""),
                    format_eur(item.get("price")),
                    f"{change:+.2f}%",
                    format_eur(item.get("high")),
                    format_eur(item.get("low")),
                    format_float(item.get("volume"), 2),
                ),
                tags=(tag,),
            )

    def populate_cyber(self) -> None:
        globe = self.data["globe"]
        if globe:
            stats = globe.get("stats", {})
            text = (
                f"Cyber threat cache · Eventi campione: {format_int(stats.get('events_sampled'))} · "
                f"Paesi sorgente: {stats.get('source_countries', '—')} · "
                f"Paesi target: {stats.get('target_countries', '—')} · Feed: {stats.get('feeds', {})}"
            )
        else:
            text = "Cyber globe cache non disponibile."
        self.globe_summary.config(text=text)

        self.clear_table(self.telemetry_tree)
        if globe:
            feed_items = globe.get("feed", []) or globe.get("timeline", []) or globe.get("events", [])
            for item in feed_items[:35]:
                source = item.get("src_name") or item.get("source_name") or item.get("source") or "—"
                target = item.get("dst_name") or item.get("target_name") or item.get("target") or "—"
                category = item.get("category", item.get("type", "—"))
                severity = safe(item.get("severity", item.get("level", "—"))).upper()
                description = item.get("description") or item.get("event") or f"{source} → {target}"
                tag = "negative" if severity in {"HIGH", "CRITICAL", "ALTA", "CRITICA"} else "warning" if severity in {"MEDIUM", "MEDIA"} else "muted"
                self.telemetry_tree.insert("", "end", values=(safe(source), safe(target), safe(category), severity, shorten(description, 160)), tags=(tag,))

        self.clear_table(self.cyber_tree)
        for item in self.data["advisories"]:
            cve = item.get("cve_id") or item.get("ghsa_id") or "ADVISORY"
            severity = safe(item.get("severity", "")).upper()
            tag = "negative" if severity in {"HIGH", "CRITICAL"} else "warning" if severity == "MEDIUM" else "muted"
            self.cyber_tree.insert(
                "",
                "end",
                values=(severity, cve, safe(item.get("updated_at", ""))[:10], shorten(item.get("summary", ""), 180), item.get("html_url", "")),
                tags=(tag,),
            )

    def populate_bitcoin(self) -> None:
        mempool = self.data["mempool"]
        lines: List[str] = []
        if not mempool:
            lines.append("Dati mempool non disponibili.")
        else:
            stats = mempool.get("stats", {})
            fees = mempool.get("fees", {})
            lines.append("Bitcoin Network · Mempool Live")
            lines.append("=" * 44)
            lines.append(f"Blocco corrente:            {mempool.get('height', '—')}")
            lines.append(f"Transazioni in mempool:     {format_int(stats.get('count'))}")
            lines.append(f"Dimensione virtuale:        {format_int(stats.get('vsize'))}")
            lines.append(f"Fee totale mempool:         {format_int(stats.get('total_fee'))}")
            lines.append("")
            lines.append("Fee consigliate")
            lines.append("-" * 44)
            lines.append(f"Fastest fee:                {fees.get('fastestFee', '—')} sat/vB")
            lines.append(f"Half hour fee:              {fees.get('halfHourFee', '—')} sat/vB")
            lines.append(f"Hour fee:                   {fees.get('hourFee', '—')} sat/vB")
            lines.append(f"Economy fee:                {fees.get('economyFee', '—')} sat/vB")
            lines.append(f"Minimum fee:                {fees.get('minimumFee', '—')} sat/vB")
            lines.append("")
            lines.append("Fonte: mempool.space API")
            lines.append("Nota: dati informativi, aggiornati tramite API pubbliche.")
        self.btc_text.configure(state="normal")
        self.btc_text.delete("1.0", "end")
        self.btc_text.insert("end", "\n".join(lines))
        self.btc_text.configure(state="disabled")

    # ------------------------------------------------------------------
    # Crypto chart panel
    # ------------------------------------------------------------------
    def open_selected_crypto_from_main_table(self, _event=None):
        selected = self.crypto_tree.selection()
        if not selected:
            return
        values = self.crypto_tree.item(selected[0], "values")
        if not values:
            return
        asset = values[0]
        for item in self.data["crypto"]:
            if item.get("asset") == asset:
                self.open_crypto_panel(selected_asset=item)
                return

    def open_crypto_panel(self, selected_asset=None):
        if not self.data["crypto"]:
            messagebox.showinfo("Crypto Live", "Nessun asset disponibile. Premi prima 'Aggiorna tutto'.")
            return

        c = self.colors
        win = tk.Toplevel(self.root)
        win.title("MolinaCrypto · Crypto Asset Panel")
        win.geometry("1080x660")
        win.minsize(920, 560)
        win.configure(bg=c["bg"])

        header = tk.Frame(win, bg=c["bg"])
        header.pack(fill="x", padx=18, pady=(16, 10))
        tk.Label(header, text="Crypto Asset Panel", bg=c["bg"], fg=c["text"], font=("DejaVu Sans", 20, "bold"), anchor="w").pack(fill="x")
        tk.Label(header, text="Prezzi Kraken e grafico OHLC semplificato. Solo informazione, non consulenza finanziaria.", bg=c["bg"], fg=c["muted"], font=("DejaVu Sans", 9), anchor="w").pack(fill="x", pady=(2, 0))

        body = tk.Frame(win, bg=c["bg"])
        body.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        left = self.panel(body, padx=8, pady=8)
        left.pack(side="left", fill="y", padx=(0, 12))

        right = self.panel(body, padx=14, pady=14)
        right.pack(side="right", fill="both", expand=True)

        asset_tree = ttk.Treeview(left, columns=("asset", "price", "change"), show="headings", height=18)
        for key, label, width in [("asset", "Asset", 80), ("price", "Prezzo", 125), ("change", "24h", 85)]:
            asset_tree.heading(key, text=label)
            asset_tree.column(key, width=width, anchor="w")
        asset_tree.pack(fill="y")
        asset_tree.tag_configure("positive", foreground=c["green"])
        asset_tree.tag_configure("negative", foreground=c["red"])

        for item in self.data["crypto"]:
            change = item.get("change", 0)
            asset_tree.insert("", "end", values=(item["asset"], format_eur(item["price"]), f"{change:+.2f}%"), tags=("positive" if change >= 0 else "negative",))

        title_label = tk.Label(right, text="Seleziona un asset", bg=c["panel"], fg=c["accent"], font=("DejaVu Sans", 16, "bold"), anchor="w")
        title_label.pack(fill="x")
        meta_label = tk.Label(right, text="Clicca un asset a sinistra per caricare il grafico.", bg=c["panel"], fg=c["muted"], font=("DejaVu Sans", 9), anchor="w", justify="left")
        meta_label.pack(fill="x", pady=(4, 10))

        range_row = tk.Frame(right, bg=c["panel"])
        range_row.pack(fill="x", pady=(0, 8))
        chart_canvas = tk.Canvas(right, bg="#071021", highlightthickness=1, highlightbackground=c["line"], height=370)
        chart_canvas.pack(fill="both", expand=True)

        chart_state = {"asset": None, "range": "1d", "canvas": chart_canvas, "title_label": title_label, "meta_label": meta_label}

        def set_range(selected_range):
            chart_state["range"] = selected_range
            if chart_state["asset"]:
                self.load_asset_chart(chart_state)

        self.ghost_button(range_row, "1 giorno", lambda: set_range("1d")).pack(side="left", padx=(0, 6))
        self.ghost_button(range_row, "7 giorni", lambda: set_range("7d")).pack(side="left", padx=(0, 6))
        self.ghost_button(range_row, "30 giorni", lambda: set_range("30d")).pack(side="left", padx=(0, 6))

        tk.Label(right, text="Fonte: Kraken public API · grafico OHLC semplificato su close price", bg=c["panel"], fg=c["muted2"], font=("DejaVu Sans", 8), anchor="w").pack(fill="x", pady=(8, 0))

        def on_select(_event=None):
            selected = asset_tree.selection()
            if not selected:
                return
            values = asset_tree.item(selected[0], "values")
            asset_code = values[0] if values else ""
            for item in self.data["crypto"]:
                if item.get("asset") == asset_code:
                    chart_state["asset"] = item
                    self.load_asset_chart(chart_state)
                    return

        asset_tree.bind("<<TreeviewSelect>>", on_select)
        asset_tree.bind("<Double-1>", on_select)
        initial_asset = selected_asset or self.data["crypto"][0]
        chart_state["asset"] = initial_asset
        self.load_asset_chart(chart_state)

    def load_asset_chart(self, chart_state):
        asset = chart_state.get("asset")
        if not asset:
            return
        canvas = chart_state["canvas"]
        selected_range = chart_state.get("range", "1d")
        chart_state["title_label"].config(text=f"{asset.get('asset')} · {asset.get('label', '')}")
        chart_state["meta_label"].config(text=f"Prezzo: {format_eur(asset.get('price'))} · Var. 24h: {asset.get('change', 0):+.2f}% · Max: {format_eur(asset.get('high'))} · Min: {format_eur(asset.get('low'))}")
        canvas.delete("all")
        canvas.create_text(20, 20, text="Caricamento grafico…", fill=self.colors["muted"], anchor="w", font=("DejaVu Sans", 11))

        def worker():
            try:
                series = self.fetch_ohlc_series(asset.get("ohlc"), selected_range)
                self.root.after(0, lambda: self.draw_price_chart(canvas, asset, series, selected_range))
            except Exception as exc:
                self.root.after(0, lambda: self.draw_chart_error(canvas, str(exc)))

        threading.Thread(target=worker, daemon=True).start()

    def fetch_ohlc_series(self, pair, selected_range):
        if selected_range == "1d":
            interval, limit = 15, 96
        elif selected_range == "7d":
            interval, limit = 60, 168
        else:
            interval, limit = 240, 180
        data = fetch_json(f"https://api.kraken.com/0/public/OHLC?pair={pair}&interval={interval}")
        result = data.get("result", {})
        key = next((k for k in result.keys() if k != "last"), None)
        if not key:
            raise ValueError("Nessun dato OHLC ricevuto da Kraken.")
        series: List[Dict[str, Any]] = []
        for row in result[key][-limit:]:
            series.append({"time": int(row[0]), "open": float(row[1]), "high": float(row[2]), "low": float(row[3]), "close": float(row[4])})
        if len(series) < 2:
            raise ValueError("Serie dati troppo breve.")
        return series

    def draw_chart_error(self, canvas, error):
        canvas.delete("all")
        canvas.create_text(20, 20, text=f"Errore grafico: {error}", fill=self.colors["red"], anchor="w", font=("DejaVu Sans", 11, "bold"))

    def draw_price_chart(self, canvas, asset, series, selected_range):
        c = self.colors
        canvas.delete("all")
        width = max(canvas.winfo_width(), 820)
        height = max(canvas.winfo_height(), 330)
        pad_left, pad_right, pad_top, pad_bottom = 75, 35, 44, 45
        plot_w = width - pad_left - pad_right
        plot_h = height - pad_top - pad_bottom
        lows = [p["low"] for p in series]
        highs = [p["high"] for p in series]
        closes = [p["close"] for p in series]
        min_price, max_price = min(lows), max(highs)
        if min_price == max_price:
            min_price -= 1
            max_price += 1
        pad = (max_price - min_price) * 0.055
        min_price -= pad
        max_price += pad

        def x_for(i):
            return pad_left + (i / (len(series) - 1)) * plot_w

        def y_for(price):
            return pad_top + (1 - ((price - min_price) / (max_price - min_price))) * plot_h

        for i in range(6):
            y = pad_top + (i / 5) * plot_h
            price = max_price - (i / 5) * (max_price - min_price)
            canvas.create_line(pad_left, y, width - pad_right, y, fill="#123052")
            canvas.create_text(10, y, text=format_eur(price), fill=c["muted"], anchor="w", font=("DejaVu Sans", 8))

        color = c["green"] if closes[-1] >= closes[0] else c["red"]
        points: List[Tuple[float, float]] = [(x_for(i), y_for(point["close"])) for i, point in enumerate(series)]
        for i in range(len(points) - 1):
            canvas.create_line(*points[i], *points[i + 1], fill=color, width=2)

        last_x, last_y = points[-1]
        canvas.create_oval(last_x - 4, last_y - 4, last_x + 4, last_y + 4, fill=c["accent"], outline="white")
        first, last = closes[0], closes[-1]
        change = ((last - first) / first) * 100 if first else 0
        canvas.create_text(pad_left, 22, text=f"{asset.get('asset')} / EUR · {selected_range.upper()} · {format_eur(last)} · {change:+.2f}%", fill=c["accent"], anchor="w", font=("DejaVu Sans", 12, "bold"))
        canvas.create_text(width - pad_right, height - 18, text="Kraken OHLC · close price", fill=c["muted"], anchor="e", font=("DejaVu Sans", 8))
        canvas.create_line(pad_left, height - pad_bottom, width - pad_right, height - pad_bottom, fill=c["accent2"])


if __name__ == "__main__":
    app_root = tk.Tk()
    _app = MolinaCryptoApp(app_root)
    app_root.mainloop()
