"""
Network Commands for Windows By Mohamed Ben slimane
Dark-themed GUI — Python 3 + Tkinter only (no extra deps)
"""

import tkinter as tk
from tkinter import scrolledtext
import re
import os
import subprocess
import threading
import sys

# ── Palette ───────────────────────────────────────────────────────────────────
BG        = "#0a0e1a"
PANEL     = "#0d1220"
BORDER    = "#1a2744"
ACCENT    = "#1e6fff"
ACCENT2   = "#00d4ff"
HIGHLIGHT = "#103080"
TEXT      = "#c8deff"
MUTED     = "#4a6fa5"
CMD_CLR   = "#7dd4fc"
SUCCESS   = "#22c55e"
WARNING   = "#f59e0b"
DANGER    = "#ef4444"
WHITE     = "#ffffff"
CMD_BG    = "#0d1f3c"

# ── Data ──────────────────────────────────────────────────────────────────────
COMMANDS = [
    ("ipconfig",                         "Show network configuration",                         "IP",        "ipconfig"),
    ("ipconfig /all",                    "Show detailed IP information",                       "IP",        "ipconfig /all"),
    ("ipconfig /release",                "Release IP address",                                 "IP",        "ipconfig /release"),
    ("ipconfig /renew",                  "Renew IP address",                                   "IP",        "ipconfig /renew"),
    ("ipconfig /displaydns",             "Show local DNS resolver cache",                      "DNS",       "ipconfig /displaydns"),
    ("ipconfig /flushdns",               "Clear DNS cache",                                    "DNS",       "ipconfig /flushdns"),
    ("ipconfig /registerdns",            "Refresh DHCP leases and DNS names",                  "DNS",       "ipconfig /registerdns"),
    ("ping [host]",                      "Check network connectivity to a host",               "Ping",      "ping 8.8.8.8"),
    ("ping -t [host]",                   "Ping continuously until stopped",                    "Ping",      "ping -t 8.8.8.8"),
    ("ping -4 [host]",                   "Force IPv4 ping",                                    "Ping",      "ping -4 google.com"),
    ("ping -6 [host]",                   "Force IPv6 ping",                                    "Ping",      "ping -6 google.com"),
    ("tracert [host]",                   "Trace route to a destination",                       "Trace",     "tracert 8.8.8.8"),
    ("tracert -d [host]",                "Trace route without DNS lookups",                    "Trace",     "tracert -d 8.8.8.8"),
    ("pathping [host]",                  "Trace route and packet loss by hop",                 "Trace",     "pathping -n -q 1 -p 100 8.8.8.8"),
    ("nslookup [domain]",                "Query DNS for domain details",                       "DNS",       "nslookup google.com"),
    ("nslookup -type=mx [domain]",       "Query mail exchanger DNS records",                   "DNS",       "nslookup -type=mx google.com"),
    ("nslookup -type=txt [domain]",      "Query TXT DNS records",                              "DNS",       "nslookup -type=txt google.com"),
    ("netstat -an",                      "Show active network connections",                    "Stats",     "netstat -an"),
    ("netstat -ano",                     "Show connections with process IDs",                  "Stats",     "netstat -ano"),
    ("netstat -e",                       "Show Ethernet statistics",                           "Stats",     "netstat -e"),
    ("netstat -r",                       "Show routing table",                                 "Stats",     "netstat -r"),
    ("netstat -s",                       "Show protocol statistics",                           "Stats",     "netstat -s"),
    ("arp -a",                           "Show ARP cache",                                     "ARP",       "arp -a"),
    ("arp -d [IP]",                      "Delete an ARP cache entry",                          "ARP",       "arp /?"),
    ("route print",                      "Show IPv4 and IPv6 route tables",                    "Route",     "route print"),
    ("route -4 print",                   "Show IPv4 route table",                              "Route",     "route -4 print"),
    ("route -6 print",                   "Show IPv6 route table",                              "Route",     "route -6 print"),
    ("nbtstat -n",                       "Show local NetBIOS names",                           "NetBIOS",   "nbtstat -n"),
    ("nbtstat -c",                       "Show NetBIOS name cache",                            "NetBIOS",   "nbtstat -c"),
    ("nbtstat -r",                       "Show NetBIOS name resolution stats",                 "NetBIOS",   "nbtstat -r"),
    ("hostname",                         "Display computer name",                              "Info",      "hostname"),
    ("getmac",                           "Show MAC address of network adapters",               "Info",      "getmac"),
    ("systeminfo",                       "Show system information including network hotfixes",  "Info",      "systeminfo"),
    ("whoami /fqdn",                     "Show fully qualified domain user name",              "Info",      "whoami /fqdn"),
    ("curl [url]",                       "Make an HTTP request",                               "Web",       "curl.exe -I https://www.microsoft.com"),
    ("curl -v [url]",                    "Show detailed HTTP connection information",          "Web",       "curl.exe -v https://www.microsoft.com"),
    ("telnet [host] [port]",             "Test a TCP port with Telnet if installed",           "Web",       "telnet /?"),
    ("ftp",                              "Open the Windows FTP client help",                   "Web",       "ftp -?"),
    ("tftp",                             "Open the Windows TFTP client help",                  "Web",       "tftp /?"),
    ("ssh [user@host]",                  "Connect to a remote SSH server",                     "Remote",    "ssh -V"),
    ("scp [file] [host:path]",           "Copy files over SSH",                                "Remote",    "scp -V"),
    ("net use",                          "Show or connect to shared resources",                "Net",       "net use"),
    ("net view",                         "Show computers or shares on the network",            "Net",       "net view"),
    ("net share",                        "List shared resources",                              "Net",       "net share"),
    ("net session",                      "List active sessions on local shares",               "Net",       "net session"),
    ("net file",                         "List open shared files",                             "Net",       "net file"),
    ("net config workstation",           "Show workstation service settings",                  "Net",       "net config workstation"),
    ("net config server",                "Show server service settings",                       "Net",       "net config server"),
    ("net accounts",                     "Show password and logon policy",                     "Net",       "net accounts"),
    ("net user",                         "List local users",                                   "Net",       "net user"),
    ("net localgroup",                   "List local groups",                                  "Net",       "net localgroup"),
    ("net group",                        "List domain groups when joined to a domain",         "Net",       "net group /?"),
    ("net computer",                     "Manage domain computer accounts",                    "Net",       "net computer /?"),
    ("net statistics workstation",        "Show workstation network statistics",                "Net",       "net statistics workstation"),
    ("net statistics server",             "Show server network statistics",                     "Net",       "net statistics server"),
    ("net start",                        "Show running services",                              "Net",       "net start"),
    ("net stop",                         "Stop a Windows service",                             "Net",       "net stop /?"),
    ("net help",                         "Show NET command help",                              "Net",       "net help"),
    ("netsh /?",                         "Show Netsh help",                                    "Netsh",     "netsh /?"),
    ("netsh interface show interface",    "Show network interfaces",                            "Netsh",     "netsh interface show interface"),
    ("netsh interface ip show config",    "Show IPv4 interface configuration",                  "Netsh",     "netsh interface ip show config"),
    ("netsh interface ipv6 show config",  "Show IPv6 interface configuration",                  "Netsh",     "netsh interface ipv6 show config"),
    ("netsh interface ip show dns",       "Show DNS server settings",                           "Netsh",     "netsh interface ip show dns"),
    ("netsh interface ipv4 show route",   "Show IPv4 routes",                                   "Netsh",     "netsh interface ipv4 show route"),
    ("netsh interface ipv6 show route",   "Show IPv6 routes",                                   "Netsh",     "netsh interface ipv6 show route"),
    ("netsh interface tcp show global",   "Show global TCP settings",                           "Netsh",     "netsh interface tcp show global"),
    ("netsh wlan show interfaces",        "Show Wi-Fi interface status",                        "WiFi",      "netsh wlan show interfaces"),
    ("netsh wlan show profiles",          "Show saved Wi-Fi profiles",                          "WiFi",      "netsh wlan show profiles"),
    ("netsh wlan show drivers",           "Show Wi-Fi driver capabilities",                     "WiFi",      "netsh wlan show drivers"),
    ("netsh wlan show networks",          "Show visible Wi-Fi networks",                        "WiFi",      "netsh wlan show networks"),
    ("netsh advfirewall show allprofiles", "Show Windows Firewall profile status",              "Firewall",  "netsh advfirewall show allprofiles"),
    ("netsh advfirewall firewall show rule name=all", "Show Windows Firewall rules",            "Firewall",  "netsh advfirewall firewall show rule name=all"),
    ("netsh winhttp show proxy",          "Show WinHTTP proxy settings",                        "Proxy",     "netsh winhttp show proxy"),
    ("netsh winsock show catalog",        "Show Winsock catalog",                               "Netsh",     "netsh winsock show catalog"),
    ("netsh http show servicestate",      "Show HTTP.sys service state",                        "Web",       "netsh http show servicestate"),
    ("Get-NetIPConfiguration",            "Show PowerShell IP configuration",                   "PowerShell", "Get-NetIPConfiguration"),
    ("Get-NetAdapter",                    "List network adapters",                              "PowerShell", "Get-NetAdapter"),
    ("Get-NetAdapterStatistics",          "Show adapter statistics",                            "PowerShell", "Get-NetAdapterStatistics"),
    ("Get-NetIPAddress",                  "List IP addresses",                                  "PowerShell", "Get-NetIPAddress"),
    ("Get-NetIPInterface",                "List IP interfaces",                                 "PowerShell", "Get-NetIPInterface"),
    ("Get-NetRoute",                      "List network routes",                                "PowerShell", "Get-NetRoute"),
    ("Get-DnsClient",                     "Show DNS client interfaces",                         "PowerShell", "Get-DnsClient"),
    ("Get-DnsClientServerAddress",        "Show DNS server addresses",                          "PowerShell", "Get-DnsClientServerAddress"),
    ("Get-DnsClientCache",                "Show DNS client cache",                              "PowerShell", "Get-DnsClientCache"),
    ("Resolve-DnsName [domain]",          "Resolve DNS names with PowerShell",                  "PowerShell", "Resolve-DnsName google.com"),
    ("Test-NetConnection [host]",         "Test host reachability with PowerShell",             "PowerShell", "Test-NetConnection google.com"),
    ("Test-NetConnection [host] -Port 443", "Test TCP port connectivity",                       "PowerShell", "Test-NetConnection google.com -Port 443"),
    ("Get-NetTCPConnection",              "List TCP connections",                               "PowerShell", "Get-NetTCPConnection"),
    ("Get-NetUDPEndpoint",                "List UDP endpoints",                                 "PowerShell", "Get-NetUDPEndpoint"),
    ("Get-NetFirewallProfile",            "Show firewall profiles",                             "PowerShell", "Get-NetFirewallProfile"),
    ("Get-NetFirewallRule",               "List firewall rules",                                "PowerShell", "Get-NetFirewallRule"),
    ("Get-NetConnectionProfile",          "Show network location profiles",                     "PowerShell", "Get-NetConnectionProfile"),
    ("Get-SmbShare",                      "List SMB shares",                                    "PowerShell", "Get-SmbShare"),
    ("Get-SmbConnection",                 "List SMB client connections",                        "PowerShell", "Get-SmbConnection"),
    ("Get-SmbSession",                    "List SMB server sessions",                           "PowerShell", "Get-SmbSession"),
    ("Get-Command *Net*",                 "Search installed PowerShell network commands",       "PowerShell", "Get-Command *Net*"),
]

CATEGORIES = ["All"] + sorted(set(c[2] for c in COMMANDS))


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


INPUT_HINTS = {
    "arp -d [IP]": "IP address",
    "net use": "drive: \\\\server\\share",
    "net view": "\\\\computer",
    "net share": "share name or name=path",
    "net session": "\\\\computer",
    "net file": "file ID",
    "net user": "username or username password /add",
    "net localgroup": "group name",
    "net group": "domain group name",
    "net computer": "\\\\computer /add",
    "net stop": "service name",
}


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Network Commands for Windows By Mohamed Ben Slimane")
        self.geometry("1180x720")
        self.minsize(960, 520)
        self.configure(bg=BG)
        self.resizable(True, True)
        try:
            self.iconbitmap(resource_path("icon.ico"))
        except Exception:
            pass

        # State — set BEFORE any method that reads them
        self._active_cat     = "All"
        self._search_text    = ""
        self._proc           = None
        self._running        = False
        self._cat_btns       = {}
        self._output_visible = False
        self._cmd_col_width  = 360
        self._input_col_width = 240
        self._cmd_col_frames = []
        self._input_col_frames = []
        self._input_values = {}
        self._split_drag_start_x = 0
        self._split_drag_start_width = self._cmd_col_width
        self._split_drag_target = "cmd"
        self.list_frame      = None   # will be set in _build_list_area

        # Build in strict order
        self._build_header()
        self._build_toolbar()
        self._build_cat_bar()
        self._build_list_area()
        self._build_output()
        self._build_footer()

        # Initial population
        self.refresh_list()

    # ── Header ────────────────────────────────────────────────────────────────
    def _build_header(self):
        hdr = tk.Frame(self, bg=BG)
        hdr.pack(fill="x", padx=20, pady=(16, 0))

        self._win_logo(hdr).pack(side="left")

        mid = tk.Frame(hdr, bg=BG)
        mid.pack(side="left", padx=12)
        tk.Label(mid, text="NETWORK COMMANDS FOR WINDOWS By Mohamed Ben Slimane ",
                 bg=BG, fg=WHITE, font=("Consolas", 15, "bold")).pack(anchor="w")
        tk.Label(mid, text="// Click row to copy  |  [Run] executes here  |  [PS] opens PowerShell window",
                 bg=BG, fg=MUTED, font=("Consolas", 9)).pack(anchor="w")

        self._win_logo(hdr).pack(side="left", padx=6)
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=20, pady=(10, 0))

    def _win_logo(self, parent):
        f = tk.Frame(parent, bg=BG)
        for i, c in enumerate(["#3b82f6", "#60a5fa", "#93c5fd", "#2563eb"]):
            r, col = divmod(i, 2)
            tk.Frame(f, bg=c, width=11, height=11).grid(row=r, column=col, padx=1, pady=1)
        return f

    # ── Toolbar ───────────────────────────────────────────────────────────────
    def _build_toolbar(self):
        bar = tk.Frame(self, bg=BG)
        bar.pack(fill="x", padx=20, pady=10)

        sf = tk.Frame(bar, bg=BORDER, padx=1, pady=1)
        sf.pack(side="left", fill="x", expand=True)
        inner = tk.Frame(sf, bg=PANEL)
        inner.pack(fill="both")
        tk.Label(inner, text="?", bg=PANEL, fg=MUTED,
                 font=("Consolas", 13)).pack(side="left", padx=(8, 2))

        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", lambda *_: self._on_search())
        self._entry = tk.Entry(inner, textvariable=self._search_var,
                               bg=PANEL, fg=TEXT, insertbackground=ACCENT2,
                               relief="flat", font=("Consolas", 12), bd=0)
        self._entry.pack(side="left", fill="x", expand=True, ipady=7, padx=(0, 8))

        self._ph = "Search commands..."
        self._entry.insert(0, self._ph)
        self._entry.config(fg=MUTED)
        self._entry.bind("<FocusIn>",  self._ph_in)
        self._entry.bind("<FocusOut>", self._ph_out)

        self._count_lbl = tk.Label(bar, text=f"{len(COMMANDS)} commands",
                                   bg=PANEL, fg=MUTED, font=("Consolas", 10),
                                   padx=10, pady=7)
        self._count_lbl.pack(side="left", padx=(8, 0))

        self._lbl_btn(bar, "X Clear Output", self._clear_output,
                      PANEL, MUTED).pack(side="right")

    def _ph_in(self, _):
        if self._entry.get() == self._ph:
            self._entry.delete(0, "end")
            self._entry.config(fg=TEXT)

    def _ph_out(self, _):
        if not self._entry.get():
            self._entry.insert(0, self._ph)
            self._entry.config(fg=MUTED)

    def _on_search(self):
        v = self._search_var.get()
        self._search_text = "" if v == self._ph else v.lower()
        self.refresh_list()

    # ── List area ─────────────────────────────────────────────────────────────
    def _build_list_area(self):
        container = tk.Frame(self, bg=BG)
        container.pack(fill="both", expand=True, padx=20)

        self._canvas = tk.Canvas(container, bg=BG, highlightthickness=0, bd=0)
        vsb = tk.Scrollbar(container, orient="vertical", command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self._canvas.pack(side="left", fill="both", expand=True)

        self.list_frame = tk.Frame(self._canvas, bg=BG)
        self._list_win  = self._canvas.create_window((0, 0),
                                                     window=self.list_frame,
                                                     anchor="nw")

        self.list_frame.bind("<Configure>",
            lambda e: self._canvas.configure(
                scrollregion=self._canvas.bbox("all")))
        self._canvas.bind("<Configure>",
            lambda e: self._canvas.itemconfig(self._list_win, width=e.width))
        self._canvas.bind("<MouseWheel>", self._scroll)
        self.list_frame.bind("<MouseWheel>", self._scroll)

    def _scroll(self, e):
        self._canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")

    # ── Category bar ──────────────────────────────────────────────────────────
    def _build_cat_bar(self):
        self._cat_frame = tk.Frame(self, bg=BG)
        self._cat_frame.pack(fill="x", padx=20, pady=(0, 6))

        for cat in CATEGORIES:
            btn = tk.Label(self._cat_frame, text=cat, bg=BG, fg=MUTED,
                           font=("Consolas", 10), padx=10, pady=4, cursor="hand2")
            btn.pack(side="left", padx=(0, 5))
            btn.bind("<Button-1>", lambda e, c=cat: self._set_cat(c))
            btn.bind("<Enter>",    lambda e, b=btn: b.config(fg=ACCENT2, bg=HIGHLIGHT))
            btn.bind("<Leave>",    lambda e, b=btn, c=cat:
                     b.config(fg=ACCENT2 if self._active_cat == c else MUTED,
                              bg=HIGHLIGHT if self._active_cat == c else BG))
            self._cat_btns[cat] = btn

        self._cat_btns["All"].config(fg=ACCENT2, bg=HIGHLIGHT)

    def _set_cat(self, cat):
        self._active_cat = cat
        for c, b in self._cat_btns.items():
            b.config(fg=ACCENT2 if c == cat else MUTED,
                     bg=HIGHLIGHT if c == cat else BG)
        self.refresh_list()

    # ── Output panel ──────────────────────────────────────────────────────────
    def _build_output(self):
        self._out_frame = tk.Frame(self, bg=BG)

        ohdr = tk.Frame(self._out_frame, bg=HIGHLIGHT)
        ohdr.pack(fill="x")

        self._out_title = tk.Label(ohdr, text="OUTPUT",
                                   bg=HIGHLIGHT, fg=ACCENT2,
                                   font=("Consolas", 11, "bold"), padx=12, pady=5)
        self._out_title.pack(side="left")
        self._lbl_btn(ohdr, "STOP", self._stop_cmd, HIGHLIGHT, DANGER).pack(side="right", padx=(0, 4))
        self._lbl_btn(ohdr, "CLOSE", self._clear_output, HIGHLIGHT, MUTED).pack(side="right")

        self._out_text = scrolledtext.ScrolledText(
            self._out_frame,
            bg="#050810", fg="#a0c4ff",
            insertbackground=ACCENT2,
            font=("Consolas", 11),
            relief="flat", bd=0,
            padx=14, pady=10,
            height=9, wrap="word",
            state="disabled",
        )
        self._out_text.pack(fill="both", expand=True)
        self._out_text.tag_config("prompt", foreground=SUCCESS)
        self._out_text.tag_config("error",  foreground=DANGER)
        self._out_text.tag_config("info",   foreground=WARNING)

    # ── Footer ────────────────────────────────────────────────────────────────
    def _build_footer(self):
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=20, pady=(6, 0))
        tk.Label(self,
                 text="Networking with Mohamed Ben Slimane  |  Click = Copy  |  Run = Execute  |  PS = Open PowerShell",
                 bg=BG, fg=MUTED, font=("Consolas", 9), pady=7).pack()

    # ── Render list ───────────────────────────────────────────────────────────
    def refresh_list(self):
        if self.list_frame is None:
            return
        for w in self.list_frame.winfo_children():
            w.destroy()
        self._cmd_col_frames = []
        self._input_col_frames = []

        q = self._search_text
        visible = [
            c for c in COMMANDS
            if (self._active_cat == "All" or c[2] == self._active_cat)
            and (not q or q in c[0].lower() or q in c[1].lower())
        ]
        self._count_lbl.config(
            text=f"{len(visible)} command{'s' if len(visible) != 1 else ''}")

        if not visible:
            tk.Label(self.list_frame, text="// No commands found",
                     bg=BG, fg=MUTED, font=("Consolas", 12), pady=40).pack()
            self.after_idle(self._reset_list_view)
            return

        for item in visible:
            cmd, desc, _, run = item[:4]
            self._make_row(cmd, desc, run)
        self.after_idle(self._reset_list_view)

    def _reset_list_view(self):
        if self.list_frame is None:
            return
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))
        self._canvas.yview_moveto(0)

    def _make_row(self, cmd, desc, run):
        row = tk.Frame(self.list_frame, bg=PANEL, cursor="hand2")
        row.pack(fill="x", pady=(0, 3))

        arrow_lbl = tk.Label(row, text=">", bg=PANEL, fg=ACCENT,
                             font=("Consolas", 14, "bold"), width=2)
        arrow_lbl.pack(side="left", fill="y")

        cmd_box = tk.Frame(row, bg=CMD_BG, width=self._cmd_col_width)
        cmd_box.pack(side="left", fill="y")
        cmd_box.pack_propagate(False)
        self._cmd_col_frames.append(cmd_box)

        cmd_lbl = tk.Label(cmd_box, text=cmd, bg=CMD_BG, fg=CMD_CLR,
                           font=("Consolas", 12),
                           anchor="w", padx=10, pady=10)
        cmd_lbl.pack(fill="both", expand=True)

        split = tk.Frame(row, bg=BORDER, width=6, cursor="sb_h_double_arrow")
        split.pack(side="left", fill="y")
        split.bind("<Enter>", lambda e: split.config(bg=ACCENT2))
        split.bind("<Leave>", lambda e: split.config(bg=BORDER))
        split.bind("<Button-1>", lambda e: self._start_split_drag(e, "cmd"))
        split.bind("<B1-Motion>", self._drag_split)
        split.bind("<MouseWheel>", self._scroll)

        acts = tk.Frame(row, bg=PANEL)
        acts.pack(side="right")

        hint = self._input_hint(cmd)
        input_box = tk.Frame(row, bg=PANEL, width=self._input_col_width)
        input_box.pack(side="right", fill="y")
        input_box.pack_propagate(False)
        self._input_col_frames.append(input_box)

        input_entry = None
        if hint:
            input_entry = tk.Entry(
                input_box,
                bg="#07142a", fg=TEXT, insertbackground=ACCENT2,
                relief="flat", font=("Consolas", 10), bd=0)
            input_entry.pack(fill="both", expand=True, padx=6, pady=7, ipady=4)
            self._prepare_input_entry(input_entry, cmd, hint)
        else:
            tk.Label(input_box, text="", bg=PANEL, fg=MUTED,
                     font=("Consolas", 10), padx=6, pady=10).pack(fill="both")

        input_split = tk.Frame(row, bg=BORDER, width=6, cursor="sb_h_double_arrow")
        input_split.pack(side="right", fill="y")
        input_split.bind("<Enter>", lambda e: input_split.config(bg=ACCENT2))
        input_split.bind("<Leave>", lambda e: input_split.config(bg=BORDER))
        input_split.bind("<Button-1>", lambda e: self._start_split_drag(e, "input"))
        input_split.bind("<B1-Motion>", self._drag_split)
        input_split.bind("<MouseWheel>", self._scroll)

        self._lbl_btn(acts, "Copy",
                      lambda c=cmd, r=run: self.copy_cmd(
                          self._build_command(c, r)),
                      PANEL, ACCENT2).pack(side="left", fill="y", ipady=6, padx=(0,1))
        tk.Frame(acts, bg=BORDER, width=1).pack(side="left", fill="y")
        self._lbl_btn(acts, "Run",
                      lambda r=run, c=cmd: self.run_cmd(
                          self._build_command(c, r), c),
                      PANEL, SUCCESS).pack(side="left", fill="y", ipady=6, padx=(0,1))
        tk.Frame(acts, bg=BORDER, width=1).pack(side="left", fill="y")
        self._lbl_btn(acts, "PS",
                      lambda r=run, c=cmd: self.open_ps(
                          self._build_command(c, r)),
                      PANEL, WARNING).pack(side="left", fill="y", ipady=6)

        desc_lbl = tk.Label(row, text=desc, bg=PANEL, fg=TEXT,
                            font=("Consolas", 11), anchor="w",
                            padx=12, pady=10)
        desc_lbl.pack(side="left", fill="x", expand=True)

        # Hover
        def enter(e):
            for w in (row, desc_lbl, acts, arrow_lbl, input_box):
                w.config(bg="#0f1830")
            cmd_lbl.config(bg="#142040")
            cmd_box.config(bg="#142040")

        def leave(e):
            for w in (row, desc_lbl, acts, arrow_lbl, input_box):
                w.config(bg=PANEL)
            cmd_lbl.config(bg=CMD_BG)
            cmd_box.config(bg=CMD_BG)

        for w in (row, arrow_lbl, cmd_box, cmd_lbl, desc_lbl):
            w.bind("<Enter>", enter)
            w.bind("<Leave>", leave)
            w.bind("<Button-1>", lambda e, c=cmd, r=run: self.copy_cmd(
                self._build_command(c, r)))
            w.bind("<MouseWheel>", self._scroll)

        if input_entry:
            input_entry.bind("<MouseWheel>", self._scroll)

    def _input_hint(self, cmd):
        placeholders = re.findall(r"\[([^\]]+)\]", cmd)
        if placeholders:
            return " ".join(placeholders)
        return INPUT_HINTS.get(cmd)

    def _prepare_input_entry(self, entry, cmd, hint):
        saved = self._input_values.get(cmd, "")
        if saved:
            entry.insert(0, saved)
        else:
            entry.insert(0, hint)
            entry.config(fg=MUTED)

        entry.bind("<FocusIn>", lambda e: self._input_focus_in(entry, hint))
        entry.bind("<FocusOut>", lambda e: self._input_focus_out(entry, cmd, hint))
        entry.bind("<KeyRelease>", lambda e: self._save_input(entry, cmd, hint))

    def _input_focus_in(self, entry, hint):
        if entry.get() == hint and entry.cget("fg") == MUTED:
            entry.delete(0, "end")
            entry.config(fg=TEXT)

    def _input_focus_out(self, entry, cmd, hint):
        self._save_input(entry, cmd, hint)
        if not entry.get():
            entry.insert(0, hint)
            entry.config(fg=MUTED)

    def _save_input(self, entry, cmd, hint):
        value = entry.get().strip()
        self._input_values[cmd] = "" if value == hint and entry.cget("fg") == MUTED else value

    def _build_command(self, display, fallback):
        value = self._input_values.get(display, "").strip()
        if not value:
            return fallback

        placeholders = re.findall(r"\[[^\]]+\]", display)
        if not placeholders:
            return f"{display} {value}".strip()

        if len(placeholders) == 1:
            return display.replace(placeholders[0], value, 1)

        values = value.split()
        result = display
        for placeholder, replacement in zip(placeholders, values):
            result = result.replace(placeholder, replacement, 1)
        if len(values) > len(placeholders):
            result = f"{result} {' '.join(values[len(placeholders):])}"
        return result

    def _column_width_limits(self):
        canvas_width = self._canvas.winfo_width() or self.winfo_width()
        min_cmd = 180
        min_desc = 220
        fixed_width = 220  # arrow, separators, action buttons, scrollbar margin
        max_cmd = max(min_cmd, canvas_width - min_desc - self._input_col_width - fixed_width)
        return min_cmd, max_cmd

    def _input_width_limits(self):
        canvas_width = self._canvas.winfo_width() or self.winfo_width()
        min_input = 150
        min_desc = 220
        fixed_width = 220  # arrow, separators, action buttons, scrollbar margin
        max_input = max(min_input, canvas_width - min_desc - self._cmd_col_width - fixed_width)
        return min_input, max_input

    def _set_input_col_width(self, width):
        min_input, max_input = self._input_width_limits()
        self._input_col_width = max(min_input, min(max_input, int(width)))
        for frame in self._input_col_frames:
            if frame.winfo_exists():
                frame.config(width=self._input_col_width)

    def _set_cmd_col_width(self, width):
        min_cmd, max_cmd = self._column_width_limits()
        self._cmd_col_width = max(min_cmd, min(max_cmd, int(width)))
        for frame in self._cmd_col_frames:
            if frame.winfo_exists():
                frame.config(width=self._cmd_col_width)

    def _start_split_drag(self, event, target="cmd"):
        self._split_drag_target = target
        self._split_drag_start_x = event.x_root
        self._split_drag_start_width = (
            self._input_col_width if target == "input" else self._cmd_col_width)
        return "break"

    def _drag_split(self, event):
        delta = event.x_root - self._split_drag_start_x
        if self._split_drag_target == "input":
            self._set_input_col_width(self._split_drag_start_width - delta)
        else:
            self._set_cmd_col_width(self._split_drag_start_width + delta)
        return "break"

    # ── Actions ───────────────────────────────────────────────────────────────
    def copy_cmd(self, text):
        self.clipboard_clear()
        self.clipboard_append(text)
        self._toast(f"Copied:  {text}")

    def run_cmd(self, run, display):
        if self._running:
            self._stop_cmd()
        self._show_output()
        self._out_title.config(text=f">> {display}")
        self._write(f"PS C:\\> {run}\n\n", "prompt")
        self._running = True
        threading.Thread(target=self._exec, args=(run,), daemon=True).start()

    def _exec(self, cmd):
        try:
            self._proc = subprocess.Popen(
                ["powershell", "-NoProfile", "-Command", cmd],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            for line in self._proc.stdout:
                self._write(line)
            self._proc.wait()
            rc = self._proc.returncode
            self._write(f"\n[Exited: code {rc}]\n", "info" if rc == 0 else "error")
        except FileNotFoundError:
            self._write("\n[PowerShell not found, trying cmd.exe]\n", "error")
            self._exec_cmd(cmd)
        except Exception as ex:
            self._write(f"\n[Error: {ex}]\n", "error")
        finally:
            self._running = False
            self._proc    = None

    def _exec_cmd(self, cmd):
        try:
            proc = subprocess.Popen(
                ["cmd", "/c", cmd],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            for line in proc.stdout:
                self._write(line)
            proc.wait()
        except Exception as ex:
            self._write(f"\n[cmd error: {ex}]\n", "error")

    def open_ps(self, cmd):
        try:
            subprocess.Popen(["powershell", "-NoExit", "-Command", cmd],
                             creationflags=subprocess.CREATE_NEW_CONSOLE)
            self._toast(f"Opened PowerShell: {cmd}")
        except FileNotFoundError:
            try:
                subprocess.Popen(["cmd", "/k", cmd],
                                 creationflags=subprocess.CREATE_NEW_CONSOLE)
                self._toast(f"Opened CMD: {cmd}")
            except Exception as ex:
                self._toast(f"Error: {ex}")

    def _stop_cmd(self):
        if self._proc:
            try: self._proc.kill()
            except: pass
        self._running = False
        self._write("\n[Stopped by user]\n", "error")

    def _show_output(self):
        if not self._output_visible:
            self._out_frame.pack(fill="x", padx=20, pady=(0, 4))
            self._output_visible = True

    def _clear_output(self):
        self._out_frame.pack_forget()
        self._output_visible = False
        self._write("", clear=True)

    def _write(self, text, tag=None, clear=False):
        def _do():
            self._out_text.config(state="normal")
            if clear:
                self._out_text.delete("1.0", "end")
            else:
                self._out_text.insert("end", text, tag) if tag else \
                self._out_text.insert("end", text)
                self._out_text.see("end")
            self._out_text.config(state="disabled")
        self.after(0, _do)

    def _toast(self, msg, ms=2500):
        if hasattr(self, "_tw") and self._tw and self._tw.winfo_exists():
            self._tw.destroy()
        t = tk.Toplevel(self)
        self._tw = t
        t.overrideredirect(True)
        t.attributes("-topmost", True)
        t.configure(bg=PANEL,
                    highlightbackground=SUCCESS,
                    highlightthickness=1)
        tk.Label(t, text=f"  {msg}  ", bg=PANEL, fg=SUCCESS,
                 font=("Consolas", 11), pady=9).pack()
        self.update_idletasks()
        x = self.winfo_x() + self.winfo_width()  - 460
        y = self.winfo_y() + self.winfo_height() - 70
        t.geometry(f"+{x}+{y}")
        t.after(ms, lambda: t.destroy() if t.winfo_exists() else None)

    def _lbl_btn(self, parent, text, cmd, bg, fg):
        b = tk.Label(parent, text=text, bg=bg, fg=fg,
                     font=("Consolas", 10), padx=10, cursor="hand2")
        b.bind("<Button-1>", lambda e: cmd())
        b.bind("<Enter>",    lambda e: b.config(bg=HIGHLIGHT, fg=WHITE))
        b.bind("<Leave>",    lambda e: b.config(bg=bg, fg=fg))
        return b


if __name__ == "__main__":
    app = App()
    app.mainloop()
