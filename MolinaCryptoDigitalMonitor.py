import json
import urllib.request
import urllib.error
import webbrowser
import threading
import tkinter as tk
from tkinter import ttk, messagebox


APP_TITLE = "molinacrypto.eu · Digital Monitor"

URLS = {
    "site": "https://www.molinacrypto.eu",
    "archive": "https://www.molinacrypto.eu/archivio.html",
    "resources": "https://www.molinacrypto.eu/risorse.html",
    "articles": "https://www.molinacrypto.eu/data/approfondimenti-list.php",
    "home_feeds": "https://www.molinacrypto.eu/data/home-feeds.php",
    "extra_feeds": "https://www.molinacrypto.eu/data/home-feeds-extra.php",
    "world_news": "https://www.molinacrypto.eu/data/world-news.php",
    "cyber_globe_cache": "https://www.molinacrypto.eu/data/cache/cyber-globe-cache.json",
    "kraken": "https://api.kraken.com/0/public/Ticker?pair=xbteur,bcheur,etheur,soleur,xrpeur,adaeur,doteur,linkeur,avaxeur,xdgeur,bnbeur",
    "github_advisories": "https://api.github.com/advisories?per_page=15&sort=updated&direction=desc",
    "fear_greed": "https://api.alternative.me/fng/?limit=3&format=json",
    "mempool_stats": "https://mempool.space/api/mempool",
    "mempool_fees": "https://mempool.space/api/v1/fees/recommended",
    "mempool_height": "https://mempool.space/api/blocks/tip/height",
    "github_checklist": "https://github.com/molpaolo3/crypto-security-checklist-it",
    "github_glossario": "https://github.com/molpaolo3/glossario-crypto-web3-cybersecurity-it",
}


def fetch_text(url, timeout=15):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "MolinaCryptoDigitalMonitor/0.1"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def fetch_json(url, timeout=15):
    return json.loads(fetch_text(url, timeout=timeout))


def safe(value, default=""):
    if value is None:
        return default
    return str(value)


class MolinaCryptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("1180x720")
        self.root.minsize(980, 620)

        self.data = {
            "articles": [],
            "home_feeds": [],
            "extra_feeds": [],
            "world_news": [],
            "crypto": [],
            "advisories": [],
            "fng": None,
            "mempool": None,
            "globe": None,
        }

        self.setup_style()
        self.build_ui()
        self.refresh_all()

    def setup_style(self):
        self.bg = "#060e1f"
        self.panel = "#0b1220"
        self.panel2 = "#111827"
        self.text = "#d8e8fa"
        self.muted = "#8099be"
        self.accent = "#1e90ff"
        self.accent2 = "#00cfff"
        self.danger = "#ff3d5a"
        self.ok = "#00d4a0"
        self.warn = "#ffb300"

        self.root.configure(bg=self.bg)

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TNotebook", background=self.bg, borderwidth=0)
        style.configure("TNotebook.Tab", background=self.panel2, foreground=self.text, padding=(14, 8))
        style.map("TNotebook.Tab", background=[("selected", self.accent)], foreground=[("selected", "white")])

        style.configure(
            "Treeview",
            background=self.panel,
            foreground=self.text,
            fieldbackground=self.panel,
            bordercolor=self.panel2,
            rowheight=32,
            font=("Arial", 10)
        )
        style.configure(
            "Treeview.Heading",
            background=self.panel2,
            foreground=self.accent2,
            font=("Arial", 10, "bold")
        )
        style.map(
            "Treeview",
            background=[("selected", self.accent)],
            foreground=[("selected", "white")]
        )

    def build_ui(self):
        header = tk.Frame(self.root, bg=self.bg)
        header.pack(fill="x", padx=16, pady=(14, 8))

        brand_row = tk.Frame(header, bg=self.bg)
        brand_row.pack(fill="x")

        logo = tk.Label(
            brand_row,
            text="M",
            bg="#0b3d91",
            fg="#ffffff",
            font=("Arial", 24, "bold"),
            width=3,
            height=1,
            relief="solid",
            bd=1
        )
        logo.pack(side="left", padx=(0, 14))

        brand_text = tk.Frame(brand_row, bg=self.bg)
        brand_text.pack(side="left", fill="x", expand=True)

        title = tk.Label(
            brand_text,
            text="molinacrypto.eu",
            bg=self.bg,
            fg=self.accent2,
            font=("Arial", 26, "bold")
        )
        title.pack(anchor="w")

        subtitle = tk.Label(
            brand_text,
            text="Bitcoin · Crypto · Cybersecurity · AI & Web3 | dashboard desktop",
            bg=self.bg,
            fg=self.muted,
            font=("Arial", 11)
        )
        subtitle.pack(anchor="w", pady=(2, 0))

        intro = tk.Label(
            brand_text,
            text="Contenuti, feed e dati live aggregati da molinacrypto.eu",
            bg=self.bg,
            fg="#5a7099",
            font=("Arial", 9)
        )
        intro.pack(anchor="w", pady=(2, 0))
        meta_right = tk.Frame(brand_row, bg=self.bg)
        meta_right.pack(side="right", anchor="ne", padx=(12, 0))

        copyright_label = tk.Label(
            meta_right,
            text="© 2026 Paolo Molina",
            bg=self.bg,
            fg=self.muted,
            font=("Arial", 8),
            anchor="e"
        )
        copyright_label.pack(anchor="e")

        version_label = tk.Label(
            meta_right,
            text="Digital Monitor v0.5 · Open source",
            bg=self.bg,
            fg="#5a7099",
            font=("Arial", 8),
            anchor="e"
        )
        version_label.pack(anchor="e", pady=(2, 0))

        disclaimer_label = tk.Label(
            meta_right,
            text="Dati informativi · non consulenza",
            bg=self.bg,
            fg="#5a7099",
            font=("Arial", 8),
            anchor="e"
        )
        disclaimer_label.pack(anchor="e", pady=(2, 0))

        line = tk.Frame(header, bg=self.accent, height=1)
        line.pack(fill="x", pady=(10, 0))

        line2 = tk.Frame(header, bg=self.accent2, height=3, width=280)
        line2.pack(anchor="w")

        buttons = tk.Frame(self.root, bg=self.bg)
        buttons.pack(fill="x", padx=16, pady=(4, 10))

        self.button(buttons, "Apri sito", lambda: webbrowser.open(URLS["site"])).pack(side="left", padx=(0, 8))
        self.button(buttons, "Archivio", lambda: webbrowser.open(URLS["archive"])).pack(side="left", padx=(0, 8))
        self.button(buttons, "Risorse", lambda: webbrowser.open(URLS["resources"])).pack(side="left", padx=(0, 8))
        self.button(buttons, "Aggiorna tutto", self.refresh_all).pack(side="left", padx=(0, 8))

        self.status = tk.Label(
            buttons,
            text="Pronto.",
            bg=self.bg,
            fg=self.muted,
            font=("Arial", 9)
        )
        self.status.pack(side="right")

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True, padx=16, pady=(0, 12))

        self.tab_dashboard = self.make_tab("Dashboard")
        self.tab_articles = self.make_tab("Articoli")
        self.tab_news = self.make_tab("News")
        self.tab_crypto = self.make_tab("Crypto Live")
        self.tab_cyber = self.make_tab("Cybersecurity")
        self.tab_btc = self.make_tab("Bitcoin Network")
        self.tab_resources = self.make_tab("Risorse")

        self.build_dashboard_tab()
        self.build_articles_tab()
        self.build_news_tab()
        self.build_crypto_tab()
        self.build_cyber_tab()
        self.build_btc_tab()
        self.build_resources_tab()

    def make_tab(self, name):
        frame = tk.Frame(self.tabs, bg=self.bg)
        self.tabs.add(frame, text=name)
        return frame

    def button(self, parent, text, command):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg="#0f766e",
            fg="white",
            activebackground="#14b8a6",
            activeforeground="white",
            relief="flat",
            padx=13,
            pady=7,
            font=("Arial", 10, "bold"),
            cursor="hand2"
        )

    def label(self, parent, text, size=11, bold=False, color=None):
        return tk.Label(
            parent,
            text=text,
            bg=self.bg,
            fg=color or self.text,
            font=("Arial", size, "bold" if bold else "normal"),
            anchor="w",
            justify="left"
        )

    def make_table(self, parent, columns):
        frame = tk.Frame(parent, bg=self.bg)
        frame.pack(fill="both", expand=True, padx=8, pady=8)

        tree = ttk.Treeview(frame, columns=[c[0] for c in columns], show="headings")
        for key, label, width in columns:
            tree.heading(key, text=label)
            tree.column(key, width=width, anchor="w")

        scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)

        tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

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

    def build_dashboard_tab(self):
        self.dashboard_container = tk.Frame(self.tab_dashboard, bg=self.bg)
        self.dashboard_container.pack(fill="both", expand=True, padx=10, pady=10)

        self.dashboard_top = tk.Frame(self.dashboard_container, bg=self.bg)
        self.dashboard_top.pack(fill="x", pady=(0, 10))

        self.dashboard_title = tk.Label(
            self.dashboard_top,
            text="Dashboard live molinacrypto.eu",
            bg=self.bg,
            fg=self.accent2,
            font=("Arial", 18, "bold")
        )
        self.dashboard_title.pack(anchor="w")

        self.dashboard_subtitle = tk.Label(
            self.dashboard_top,
            text="Sintesi rapida di articoli, news, crypto, Bitcoin Network e cybersecurity.",
            bg=self.bg,
            fg=self.muted,
            font=("Arial", 10)
        )
        self.dashboard_subtitle.pack(anchor="w", pady=(2, 0))

        self.cards_frame = tk.Frame(self.dashboard_container, bg=self.bg)
        self.cards_frame.pack(fill="both", expand=True)

        self.card_articles = self.create_dashboard_card(self.cards_frame, "Ultimi articoli")
        self.card_crypto = self.create_dashboard_card(self.cards_frame, "Crypto live")
        self.card_fng = self.create_dashboard_card(self.cards_frame, "Fear & Greed")
        self.card_btc = self.create_dashboard_card(self.cards_frame, "Bitcoin Network")
        self.card_cyber = self.create_dashboard_card(self.cards_frame, "Cybersecurity")
        self.card_news = self.create_dashboard_card(self.cards_frame, "News esterne")

        self.card_articles.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
        self.card_crypto.grid(row=0, column=1, sticky="nsew", padx=6, pady=6)
        self.card_fng.grid(row=0, column=2, sticky="nsew", padx=6, pady=6)

        self.card_btc.grid(row=1, column=0, sticky="nsew", padx=6, pady=6)
        self.card_cyber.grid(row=1, column=1, sticky="nsew", padx=6, pady=6)
        self.card_news.grid(row=1, column=2, sticky="nsew", padx=6, pady=6)

        for col in range(3):
            self.cards_frame.grid_columnconfigure(col, weight=1)

        for row in range(2):
            self.cards_frame.grid_rowconfigure(row, weight=1)

        self.dashboard_note = tk.Label(
            self.dashboard_container,
            text="Suggerimento: usa le tab in alto per vedere il dettaglio e fai doppio click sulle righe per aprire i link nel browser.",
            bg=self.bg,
            fg=self.muted,
            font=("Arial", 9)
        )
        self.dashboard_note.pack(anchor="w", pady=(10, 0))

    def create_dashboard_card(self, parent, title):
        card = tk.Frame(
            parent,
            bg=self.panel,
            highlightbackground="#1e90ff",
            highlightthickness=1,
            padx=12,
            pady=10
        )

        title_label = tk.Label(
            card,
            text=title,
            bg=self.panel,
            fg=self.accent2,
            font=("Arial", 12, "bold"),
            anchor="w"
        )
        title_label.pack(anchor="w", pady=(0, 8))

        body_label = tk.Label(
            card,
            text="In attesa dati...",
            bg=self.panel,
            fg=self.text,
            font=("Arial", 10),
            justify="left",
            anchor="nw",
            wraplength=310
        )
        body_label.pack(fill="both", expand=True, anchor="w")

        card.body_label = body_label
        return card

    def build_articles_tab(self):
        top = tk.Frame(self.tab_articles, bg=self.bg)
        top.pack(fill="x", padx=8, pady=(8, 0))

        self.label(top, "Ultimi articoli molinacrypto.eu", 13, True, self.accent2).pack(side="left")

        self.article_filter = tk.StringVar(value="tutti")
        combo = ttk.Combobox(
            top,
            textvariable=self.article_filter,
            values=["tutti", "crypto", "cybersecurity", "digital"],
            state="readonly",
            width=18
        )
        combo.pack(side="right")
        combo.bind("<<ComboboxSelected>>", lambda event: self.populate_articles())

        self.articles_tree = self.make_table(
            self.tab_articles,
            [
                ("date", "Data", 130),
                ("label", "Categoria", 130),
                ("title", "Titolo", 620),
                ("url", "URL", 300),
            ]
        )
        self.articles_tree.bind("<Double-1>", lambda event: self.open_from_tree(self.articles_tree, 3))

    def build_news_tab(self):
        self.news_tree = self.make_table(
            self.tab_news,
            [
                ("type", "Tipo", 120),
                ("date", "Data", 140),
                ("source", "Fonte", 150),
                ("category", "Categoria", 130),
                ("title", "Titolo", 560),
                ("url", "URL", 300),
            ]
        )
        self.news_tree.bind("<Double-1>", lambda event: self.open_from_tree(self.news_tree, 5))

    def build_crypto_tab(self):
        top = tk.Frame(self.tab_crypto, bg=self.bg)
        top.pack(fill="x", padx=8, pady=(8, 0))

        self.label(
            top,
            "Prezzi crypto live da Kraken",
            13,
            True,
            self.accent2
        ).pack(side="left")

        self.button(
            top,
            "Apri pannello asset / grafici",
            self.open_crypto_panel
        ).pack(side="right")

        self.crypto_tree = self.make_table(
            self.tab_crypto,
            [
                ("asset", "Asset", 90),
                ("label", "Nome", 160),
                ("price", "Prezzo EUR", 160),
                ("change", "Var. 24h", 120),
                ("high", "Max 24h", 160),
                ("low", "Min 24h", 160),
                ("volume", "Volume", 160),
            ]
        )

        self.crypto_tree.bind("<Double-1>", self.open_selected_crypto_from_main_table)

    def open_selected_crypto_from_main_table(self, event=None):
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
            messagebox.showinfo(
                "Crypto Live",
                "Nessun asset disponibile. Premi prima 'Aggiorna tutto'."
            )
            return

        win = tk.Toplevel(self.root)
        win.title("molinacrypto.eu · Crypto Asset Panel")
        win.geometry("1050x650")
        win.minsize(900, 560)
        win.configure(bg=self.bg)

        header = tk.Frame(win, bg=self.bg)
        header.pack(fill="x", padx=14, pady=(12, 8))

        tk.Label(
            header,
            text="Crypto Asset Panel",
            bg=self.bg,
            fg=self.accent2,
            font=("Arial", 18, "bold")
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Prezzi live Kraken e grafico OHLC semplificato. Dati informativi, non consulenza finanziaria.",
            bg=self.bg,
            fg=self.muted,
            font=("Arial", 10)
        ).pack(anchor="w", pady=(2, 0))

        body = tk.Frame(win, bg=self.bg)
        body.pack(fill="both", expand=True, padx=14, pady=10)

        left = tk.Frame(body, bg=self.bg)
        left.pack(side="left", fill="y", padx=(0, 10))

        right = tk.Frame(body, bg=self.panel, padx=12, pady=12)
        right.pack(side="right", fill="both", expand=True)

        columns = ("asset", "price", "change")
        asset_tree = ttk.Treeview(left, columns=columns, show="headings", height=18)
        asset_tree.heading("asset", text="Asset")
        asset_tree.heading("price", text="Prezzo")
        asset_tree.heading("change", text="24h")

        asset_tree.column("asset", width=90, anchor="w")
        asset_tree.column("price", width=130, anchor="w")
        asset_tree.column("change", width=90, anchor="w")

        asset_tree.pack(fill="y", expand=False)

        for item in self.data["crypto"]:
            sign = "+" if item["change"] >= 0 else ""
            asset_tree.insert(
                "",
                "end",
                values=(
                    item["asset"],
                    f"€ {item['price']:.5f}",
                    f"{sign}{item['change']:.2f}%"
                )
            )

        title_label = tk.Label(
            right,
            text="Seleziona un asset",
            bg=self.panel,
            fg=self.accent2,
            font=("Arial", 15, "bold"),
            anchor="w"
        )
        title_label.pack(fill="x")

        meta_label = tk.Label(
            right,
            text="Clicca un asset a sinistra per caricare il grafico.",
            bg=self.panel,
            fg=self.muted,
            font=("Arial", 10),
            anchor="w",
            justify="left"
        )
        meta_label.pack(fill="x", pady=(4, 10))

        range_row = tk.Frame(right, bg=self.panel)
        range_row.pack(fill="x", pady=(0, 8))

        chart_canvas = tk.Canvas(
            right,
            bg="#071021",
            highlightthickness=1,
            highlightbackground="#1e90ff",
            height=360
        )
        chart_canvas.pack(fill="both", expand=True)

        chart_state = {
            "asset": None,
            "range": "1d",
            "canvas": chart_canvas,
            "title_label": title_label,
            "meta_label": meta_label,
        }

        def set_range(r):
            chart_state["range"] = r
            if chart_state["asset"]:
                self.load_asset_chart(chart_state)

        self.button(range_row, "1 giorno", lambda: set_range("1d")).pack(side="left", padx=(0, 6))
        self.button(range_row, "7 giorni", lambda: set_range("7d")).pack(side="left", padx=(0, 6))
        self.button(range_row, "30 giorni", lambda: set_range("30d")).pack(side="left", padx=(0, 6))

        bottom = tk.Label(
            right,
            text="Fonte: Kraken public API · seleziona un asset · grafico OHLC semplificato",
            bg=self.panel,
            fg=self.muted,
            font=("Arial", 9),
            anchor="w"
        )
        bottom.pack(fill="x", pady=(8, 0))

        def on_select(event=None):
            selected = asset_tree.selection()

            if not selected:
                return

            values = asset_tree.item(selected[0], "values")

            if not values:
                return

            asset_code = values[0]

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
        title_label = chart_state["title_label"]
        meta_label = chart_state["meta_label"]
        selected_range = chart_state.get("range", "1d")

        title_label.config(
            text=f"{asset.get('asset')} · {asset.get('label', '')}"
        )

        sign = "+" if asset["change"] >= 0 else ""

        meta_label.config(
            text=(
                f"Prezzo: € {asset['price']:.6f} · "
                f"Var. 24h: {sign}{asset['change']:.2f}% · "
                f"Max: € {asset['high']:.6f} · "
                f"Min: € {asset['low']:.6f}"
            )
        )

        canvas.delete("all")
        canvas.create_text(
            20,
            20,
            text="Caricamento grafico...",
            fill=self.muted,
            anchor="w",
            font=("Arial", 11)
        )

        def worker():
            try:
                series = self.fetch_ohlc_series(asset.get("ohlc"), selected_range)
                self.root.after(
                    0,
                    lambda: self.draw_price_chart(canvas, asset, series, selected_range)
                )
            except Exception as e:
                self.root.after(0, lambda: self.draw_chart_error(canvas, str(e)))

        threading.Thread(target=worker, daemon=True).start()

    def fetch_ohlc_series(self, pair, selected_range):
        if selected_range == "1d":
            interval = 15
            limit = 96
        elif selected_range == "7d":
            interval = 60
            limit = 168
        else:
            interval = 240
            limit = 180

        url = f"https://api.kraken.com/0/public/OHLC?pair={pair}&interval={interval}"
        data = fetch_json(url)

        result = data.get("result", {})
        key = next((k for k in result.keys() if k != "last"), None)

        if not key:
            raise ValueError("Nessun dato OHLC ricevuto da Kraken.")

        raw_rows = result[key][-limit:]

        series = []

        for row in raw_rows:
            series.append({
                "time": int(row[0]),
                "open": float(row[1]),
                "high": float(row[2]),
                "low": float(row[3]),
                "close": float(row[4]),
            })

        if len(series) < 2:
            raise ValueError("Serie dati troppo breve.")

        return series

    def draw_chart_error(self, canvas, error):
        canvas.delete("all")
        canvas.create_text(
            20,
            20,
            text=f"Errore grafico: {error}",
            fill=self.danger,
            anchor="w",
            font=("Arial", 11, "bold")
        )

    def draw_price_chart(self, canvas, asset, series, selected_range):
        canvas.delete("all")

        width = max(canvas.winfo_width(), 800)
        height = max(canvas.winfo_height(), 320)

        pad_left = 70
        pad_right = 35
        pad_top = 42
        pad_bottom = 45

        plot_w = width - pad_left - pad_right
        plot_h = height - pad_top - pad_bottom

        lows = [p["low"] for p in series]
        highs = [p["high"] for p in series]
        closes = [p["close"] for p in series]

        min_price = min(lows)
        max_price = max(highs)

        if min_price == max_price:
            min_price -= 1
            max_price += 1

        price_pad = (max_price - min_price) * 0.05
        min_price -= price_pad
        max_price += price_pad

        def x_for(i):
            if len(series) == 1:
                return pad_left
            return pad_left + (i / (len(series) - 1)) * plot_w

        def y_for(price):
            return pad_top + (1 - ((price - min_price) / (max_price - min_price))) * plot_h

        # Griglia orizzontale
        for i in range(6):
            y = pad_top + (i / 5) * plot_h
            price = max_price - (i / 5) * (max_price - min_price)

            canvas.create_line(
                pad_left,
                y,
                width - pad_right,
                y,
                fill="#123052"
            )

            canvas.create_text(
                8,
                y,
                text=f"€{price:.2f}",
                fill=self.muted,
                anchor="w",
                font=("Arial", 8)
            )

        points = []

        for i, point in enumerate(series):
            points.append((x_for(i), y_for(point["close"])))

        color = self.ok if closes[-1] >= closes[0] else self.danger

        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]

            canvas.create_line(
                x1,
                y1,
                x2,
                y2,
                fill=color,
                width=2
            )

        first = closes[0]
        last = closes[-1]
        change = ((last - first) / first) * 100 if first else 0
        sign = "+" if change >= 0 else ""

        last_x, last_y = points[-1]

        canvas.create_oval(
            last_x - 4,
            last_y - 4,
            last_x + 4,
            last_y + 4,
            fill=self.accent2,
            outline="white"
        )

        canvas.create_text(
            pad_left,
            20,
            text=f"{asset.get('asset')} / EUR · {selected_range.upper()} · € {last:.6f} · {sign}{change:.2f}%",
            fill=self.accent2,
            anchor="w",
            font=("Arial", 12, "bold")
        )

        canvas.create_text(
            width - pad_right,
            height - 18,
            text="Kraken OHLC · linea close semplificata",
            fill=self.muted,
            anchor="e",
            font=("Arial", 9)
        )

        canvas.create_line(
            pad_left,
            height - pad_bottom,
            width - pad_right,
            height - pad_bottom,
            fill="#1e90ff"
        )

    def build_cyber_tab(self):
        top = tk.Frame(self.tab_cyber, bg=self.bg)
        top.pack(fill="x", padx=8, pady=8)

        self.globe_summary = tk.Label(
            top,
            text="Cyber globe: in attesa dati...",
            bg=self.panel,
            fg=self.text,
            font=("Arial", 10),
            justify="left",
            anchor="w",
            padx=12,
            pady=10
        )
        self.globe_summary.pack(fill="x")

        # Telemetria cyber recente dal cyber-globe-cache.json
        telemetry_label = tk.Label(
            self.tab_cyber,
            text="Telemetria cyber recente",
            bg=self.bg,
            fg=self.accent2,
            font=("Arial", 12, "bold"),
            anchor="w"
        )
        telemetry_label.pack(fill="x", padx=8, pady=(4, 0))

        self.telemetry_tree = self.make_table(
            self.tab_cyber,
            [
                ("source", "Sorgente", 150),
                ("target", "Target", 150),
                ("category", "Categoria", 130),
                ("severity", "Severità", 110),
                ("description", "Evento", 560),
            ]
        )

        vuln_label = tk.Label(
            self.tab_cyber,
            text="Ultime vulnerabilità GitHub Advisory",
            bg=self.bg,
            fg=self.accent2,
            font=("Arial", 12, "bold"),
            anchor="w"
        )
        vuln_label.pack(fill="x", padx=8, pady=(8, 0))

        self.cyber_tree = self.make_table(
            self.tab_cyber,
            [
                ("severity", "Severity", 110),
                ("id", "ID", 190),
                ("date", "Aggiornato", 130),
                ("summary", "Descrizione", 680),
                ("url", "URL", 280),
            ]
        )
        self.cyber_tree.bind("<Double-1>", lambda event: self.open_from_tree(self.cyber_tree, 4))

    def build_btc_tab(self):
        self.btc_text = tk.Text(
            self.tab_btc,
            bg=self.panel,
            fg=self.text,
            insertbackground=self.text,
            relief="flat",
            wrap="word",
            font=("Arial", 12),
            padx=14,
            pady=14
        )
        self.btc_text.pack(fill="both", expand=True, padx=8, pady=8)
        self.btc_text.insert("end", "Caricamento dati Bitcoin Network...\n")
        self.btc_text.configure(state="disabled")

    def build_resources_tab(self):
        box = tk.Frame(self.tab_resources, bg=self.bg)
        box.pack(fill="both", expand=True, padx=16, pady=16)

        self.label(box, "Risorse gratuite molinacrypto.eu", 16, True, self.accent2).pack(anchor="w", pady=(0, 10))

        resources = [
            ("Pagina risorse", URLS["resources"]),
            ("Checklist sicurezza crypto su GitHub", URLS["github_checklist"]),
            ("Glossario Crypto, Web3 e Cybersecurity su GitHub", URLS["github_glossario"]),
            ("Archivio articoli", URLS["archive"]),
            ("Home molinacrypto.eu", URLS["site"]),
        ]

        for title, url in resources:
            row = tk.Frame(box, bg=self.panel, padx=12, pady=10)
            row.pack(fill="x", pady=5)

            tk.Label(
                row,
                text=title,
                bg=self.panel,
                fg=self.text,
                font=("Arial", 11, "bold")
            ).pack(side="left")

            self.button(row, "Apri", lambda u=url: webbrowser.open(u)).pack(side="right")

    def refresh_all(self):
        self.status.config(text="Aggiornamento in corso...")
        threading.Thread(target=self.load_all_data, daemon=True).start()

    def load_all_data(self):
        errors = []

        try:
            articles = fetch_json(URLS["articles"])
            self.data["articles"] = articles.get("items", [])
        except Exception as e:
            errors.append(f"Articoli: {e}")

        try:
            home = fetch_json(URLS["home_feeds"])
            self.data["home_feeds"] = home.get("items", [])
        except Exception as e:
            errors.append(f"News principali: {e}")

        try:
            extra = fetch_json(URLS["extra_feeds"])
            self.data["extra_feeds"] = extra.get("items", [])
        except Exception as e:
            errors.append(f"News extra: {e}")

        try:
            world = fetch_json(URLS["world_news"])
            self.data["world_news"] = world.get("items", [])
        except Exception as e:
            errors.append(f"World news: {e}")

        try:
            globe = fetch_json(URLS["cyber_globe_cache"])
            self.data["globe"] = globe
        except Exception as e:
            errors.append(f"Cyber globe cache: {e}")

        try:
            kraken = fetch_json(URLS["kraken"])
            self.data["crypto"] = self.parse_kraken(kraken)
        except Exception as e:
            errors.append(f"Kraken: {e}")

        try:
            advisories = fetch_json(URLS["github_advisories"])
            self.data["advisories"] = advisories if isinstance(advisories, list) else []
        except Exception as e:
            errors.append(f"GitHub advisories: {e}")

        try:
            fng = fetch_json(URLS["fear_greed"])
            self.data["fng"] = fng
        except Exception as e:
            errors.append(f"Fear & Greed: {e}")

        try:
            mempool = fetch_json(URLS["mempool_stats"])
            fees = fetch_json(URLS["mempool_fees"])
            height = fetch_text(URLS["mempool_height"]).strip()
            self.data["mempool"] = {
                "stats": mempool,
                "fees": fees,
                "height": height
            }
        except Exception as e:
            errors.append(f"Mempool: {e}")

        self.root.after(0, lambda: self.update_ui(errors))

    def parse_kraken(self, data):
        result = data.get("result", {})

        assets = [
            {
                "asset": "BTC",
                "label": "Bitcoin",
                "keys": ["XXBTZEUR", "XBTEUR"],
                "ohlc": "XBTEUR"
            },
            {
                "asset": "BCH",
                "label": "Bitcoin Cash",
                "keys": ["BCHEUR", "BCHZEUR"],
                "ohlc": "BCHEUR"
            },
            {
                "asset": "ETH",
                "label": "Ethereum",
                "keys": ["XETHZEUR", "ETHEUR"],
                "ohlc": "ETHEUR"
            },
            {
                "asset": "SOL",
                "label": "Solana",
                "keys": ["SOLEUR"],
                "ohlc": "SOLEUR"
            },
            {
                "asset": "XRP",
                "label": "Ripple",
                "keys": ["XXRPZEUR", "XRPEUR"],
                "ohlc": "XRPEUR"
            },
            {
                "asset": "ADA",
                "label": "Cardano",
                "keys": ["ADAEUR"],
                "ohlc": "ADAEUR"
            },
            {
                "asset": "DOT",
                "label": "Polkadot",
                "keys": ["DOTEUR"],
                "ohlc": "DOTEUR"
            },
            {
                "asset": "LINK",
                "label": "Chainlink",
                "keys": ["LINKEUR"],
                "ohlc": "LINKEUR"
            },
            {
                "asset": "AVAX",
                "label": "Avalanche",
                "keys": ["AVAXEUR"],
                "ohlc": "AVAXEUR"
            },
            {
                "asset": "DOGE",
                "label": "Dogecoin",
                "keys": ["XDGEUR", "XDGZEUR", "DOGEEUR"],
                "ohlc": "XDGEUR"
            },
            {
                "asset": "BNB",
                "label": "BNB",
                "keys": ["BNBEUR"],
                "ohlc": "BNBEUR"
            },
        ]

        rows = []

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

            change = 0
            if open_price:
                change = ((last - open_price) / open_price) * 100

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

        return rows

    def update_ui(self, errors):
        self.populate_dashboard()
        self.populate_articles()
        self.populate_news()
        self.populate_crypto()
        self.populate_cyber()
        self.populate_btc()

        if errors:
            self.status.config(text=f"Aggiornato con {len(errors)} avvisi.")
        else:
            self.status.config(text="Aggiornamento completato.")

    def populate_dashboard(self):
        articles = self.data["articles"]
        home = self.data["home_feeds"]
        extra = self.data["extra_feeds"]
        world = self.data["world_news"]
        crypto = self.data["crypto"]
        advisories = self.data["advisories"]
        fng = self.data["fng"]
        globe = self.data["globe"]
        mempool = self.data["mempool"]

        # Card articoli
        if articles:
            latest = articles[0]
            articles_text = (
                f"Totale articoli: {len(articles)}\n\n"
                f"Ultimo:\n{latest.get('title', '—')}\n\n"
                f"Categoria: {latest.get('label', '—')}\n"
                f"Data: {latest.get('date_human', latest.get('date', '—'))}"
            )
        else:
            articles_text = "Nessun articolo disponibile."

        self.card_articles.body_label.config(text=articles_text)

        # Card crypto
        if crypto:
            rows = []
            for item in crypto[:5]:
                sign = "+" if item["change"] >= 0 else ""
                rows.append(
                    f"{item['asset']}: € {item['price']:.4f}  ({sign}{item['change']:.2f}%)"
                )
            crypto_text = "\n".join(rows)
        else:
            crypto_text = "Prezzi crypto non disponibili."

        self.card_crypto.body_label.config(text=crypto_text)

        # Card Fear & Greed
        if fng and fng.get("data"):
            today = fng["data"][0]
            fng_text = (
                f"Valore: {today.get('value', '—')}/100\n"
                f"Classificazione: {today.get('value_classification', '—')}\n\n"
                f"Fonte: alternative.me"
            )
        else:
            fng_text = "Fear & Greed non disponibile."

        self.card_fng.body_label.config(text=fng_text)

        # Card Bitcoin Network
        if mempool:
            stats = mempool["stats"]
            fees = mempool["fees"]
            btc_text = (
                f"Blocco: {mempool.get('height', '—')}\n"
                f"Tx mempool: {stats.get('count', '—')}\n\n"
                f"Fastest: {fees.get('fastestFee', '—')} sat/vB\n"
                f"Half hour: {fees.get('halfHourFee', '—')} sat/vB\n"
                f"Minimum: {fees.get('minimumFee', '—')} sat/vB"
            )
        else:
            btc_text = "Dati Bitcoin Network non disponibili."

        self.card_btc.body_label.config(text=btc_text)

        # Card cybersecurity
        if globe:
            stats = globe.get("stats", {})
            cyber_text = (
                f"Eventi campione: {stats.get('events_sampled', '—')}\n"
                f"Paesi sorgente: {stats.get('source_countries', '—')}\n"
                f"Paesi target: {stats.get('target_countries', '—')}\n\n"
                f"Advisory GitHub: {len(advisories)}"
            )

            if advisories:
                first = advisories[0]
                cyber_text += (
                    f"\n\nUltima:\n"
                    f"{first.get('cve_id') or first.get('ghsa_id') or 'ADVISORY'}\n"
                    f"{safe(first.get('summary', ''))[:90]}..."
                )
        else:
            cyber_text = "Dati cybersecurity non disponibili."

        self.card_cyber.body_label.config(text=cyber_text)

        # Card news
        news_total = len(home) + len(extra) + len(world)
        if news_total:
            title = "—"
            source = "—"

            if home:
                title = home[0].get("title", "—")
                source = home[0].get("source", "—")
            elif extra:
                title = extra[0].get("title", "—")
                source = extra[0].get("source", "—")
            elif world:
                title = world[0].get("title", "—")
                source = world[0].get("source", "—")

            news_text = (
                f"News caricate: {news_total}\n"
                f"Main: {len(home)} · Extra: {len(extra)} · World: {len(world)}\n\n"
                f"Prima news:\n{title}\n\n"
                f"Fonte: {source}"
            )
        else:
            news_text = "News esterne non disponibili."

        self.card_news.body_label.config(text=news_text)

    def populate_articles(self):
        self.clear_table(self.articles_tree)
        selected = self.article_filter.get()

        for item in self.data["articles"]:
            category = item.get("category", "")
            if selected != "tutti" and category != selected:
                continue

            self.articles_tree.insert(
                "",
                "end",
                values=(
                    item.get("date_human", item.get("date", "")),
                    item.get("label", ""),
                    item.get("title", ""),
                    item.get("url", ""),
                )
            )

    def populate_news(self):
        self.clear_table(self.news_tree)

        combined = []

        for item in self.data["home_feeds"]:
            combined.append(("Main", item))

        for item in self.data["extra_feeds"]:
            combined.append(("Extra", item))

        for item in self.data["world_news"]:
            combined.append(("World", item))

        for kind, item in combined:
            self.news_tree.insert(
                "",
                "end",
                values=(
                    kind,
                    safe(item.get("published_at", ""))[:10],
                    item.get("source", ""),
                    item.get("slot") or item.get("category") or item.get("cat", ""),
                    item.get("title", ""),
                    item.get("url", ""),
                )
            )

    def populate_crypto(self):
        self.clear_table(self.crypto_tree)

        for item in self.data["crypto"]:
            sign = "+" if item["change"] >= 0 else ""
            self.crypto_tree.insert(
                "",
                "end",
                values=(
                    item["asset"],
                    item.get("label", ""),
                    f"€ {item['price']:.6f}",
                    f"{sign}{item['change']:.2f}%",
                    f"€ {item['high']:.6f}",
                    f"€ {item['low']:.6f}",
                    f"{item['volume']:.2f}",
                )
            )

    def populate_cyber(self):
        globe = self.data["globe"]

        if globe:
            stats = globe.get("stats", {})
            text = (
                f"Cyber threat cache · Eventi campione: {stats.get('events_sampled', '—')} · "
                f"Paesi sorgente: {stats.get('source_countries', '—')} · "
                f"Paesi target: {stats.get('target_countries', '—')} · "
                f"Feed: {stats.get('feeds', {})}"
            )
        else:
            text = "Cyber globe cache non disponibile."

        self.globe_summary.config(text=text)

        # Popola telemetria cyber recente
        self.clear_table(self.telemetry_tree)

        if globe:
            feed_items = globe.get("feed", []) or globe.get("timeline", [])

            for item in feed_items[:20]:
                source = (
                    item.get("src_name")
                    or item.get("source_name")
                    or item.get("source")
                    or "—"
                )

                target = (
                    item.get("dst_name")
                    or item.get("target_name")
                    or item.get("target")
                    or "—"
                )

                category = item.get("category", "—")
                severity = item.get("severity", item.get("level", "—"))

                description = (
                    item.get("description")
                    or item.get("type")
                    or item.get("event")
                    or f"{source} → {target}"
                )

                self.telemetry_tree.insert(
                    "",
                    "end",
                    values=(
                        safe(source),
                        safe(target),
                        safe(category),
                        safe(severity).upper(),
                        safe(description)[:160],
                    )
                )

        # Popola vulnerabilità
        self.clear_table(self.cyber_tree)

        for item in self.data["advisories"]:
            cve = item.get("cve_id") or item.get("ghsa_id") or "ADVISORY"
            self.cyber_tree.insert(
                "",
                "end",
                values=(
                    safe(item.get("severity", "")).upper(),
                    cve,
                    safe(item.get("updated_at", ""))[:10],
                    safe(item.get("summary", ""))[:180],
                    item.get("html_url", ""),
                )
            )

    def populate_btc(self):
        mempool = self.data["mempool"]

        lines = []

        if not mempool:
            lines.append("Dati mempool non disponibili.")
        else:
            stats = mempool["stats"]
            fees = mempool["fees"]

            lines.append("Bitcoin Network · Mempool Live\n")
            lines.append(f"Blocco corrente: {mempool.get('height', '—')}")
            lines.append(f"Transazioni in mempool: {stats.get('count', '—')}")
            lines.append(f"Dimensione virtuale mempool: {stats.get('vsize', '—')}")
            lines.append(f"Fee totale mempool: {stats.get('total_fee', '—')}")
            lines.append("")
            lines.append("Fee consigliate:")
            lines.append(f"  Fastest fee: {fees.get('fastestFee', '—')} sat/vB")
            lines.append(f"  Half hour fee: {fees.get('halfHourFee', '—')} sat/vB")
            lines.append(f"  Hour fee: {fees.get('hourFee', '—')} sat/vB")
            lines.append(f"  Economy fee: {fees.get('economyFee', '—')} sat/vB")
            lines.append(f"  Minimum fee: {fees.get('minimumFee', '—')} sat/vB")
            lines.append("")
            lines.append("Fonte: mempool.space API")

        self.btc_text.configure(state="normal")
        self.btc_text.delete("1.0", "end")
        self.btc_text.insert("end", "\n".join(lines))
        self.btc_text.configure(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = MolinaCryptoApp(root)
    root.mainloop()