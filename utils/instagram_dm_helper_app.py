#!/usr/bin/env python3
"""App desktop simples para analisar DMs exportadas e sugerir resposta carinhosa.

Modo seguro:
- não faz login em redes sociais
- não envia mensagens automaticamente
"""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from utils.instagram_dm_helper import analyze_and_suggest, load_export


class InstagramDMHelperApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Saminho DM Helper")
        self.root.geometry("860x640")

        self.file_path = tk.StringVar()
        self.influencer = tk.StringVar()
        self.seed = tk.StringVar()

        self._build_ui()

    def _build_ui(self) -> None:
        frame = ttk.Frame(self.root, padding=14)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Arquivo JSON das conversas").grid(row=0, column=0, sticky="w")
        file_entry = ttk.Entry(frame, textvariable=self.file_path, width=80)
        file_entry.grid(row=1, column=0, sticky="ew", padx=(0, 8))
        ttk.Button(frame, text="Selecionar arquivo", command=self.choose_file).grid(row=1, column=1, sticky="ew")

        ttk.Label(frame, text="Username da influenciadora").grid(row=2, column=0, sticky="w", pady=(10, 0))
        ttk.Entry(frame, textvariable=self.influencer).grid(row=3, column=0, columnspan=2, sticky="ew")

        ttk.Label(frame, text="Semente aleatória (opcional)").grid(row=4, column=0, sticky="w", pady=(10, 0))
        ttk.Entry(frame, textvariable=self.seed).grid(row=5, column=0, columnspan=2, sticky="ew")

        ttk.Button(frame, text="Analisar conversa", command=self.analyze).grid(row=6, column=0, columnspan=2, sticky="ew", pady=14)

        self.output = tk.Text(frame, wrap="word", height=24)
        self.output.grid(row=7, column=0, columnspan=2, sticky="nsew")

        ttk.Button(frame, text="Salvar resposta em TXT", command=self.save_reply).grid(
            row=8, column=0, columnspan=2, sticky="ew", pady=(10, 0)
        )

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=0)
        frame.rowconfigure(7, weight=1)

    def choose_file(self) -> None:
        selected = filedialog.askopenfilename(
            title="Selecione o arquivo JSON",
            filetypes=[("JSON", "*.json"), ("Todos os arquivos", "*.*")],
        )
        if selected:
            self.file_path.set(selected)

    def analyze(self) -> None:
        try:
            path = Path(self.file_path.get().strip())
            if not path.exists():
                raise ValueError("Selecione um arquivo JSON válido.")

            influencer = self.influencer.get().strip()
            if not influencer:
                raise ValueError("Preencha o username da influenciadora.")

            seed_value = self.seed.get().strip()
            seed = int(seed_value) if seed_value else None

            conversations = load_export(path)
            result = analyze_and_suggest(conversations, influencer_username=influencer, seed=seed)

            content = (
                f"Participante escolhido: {result.participant}\n"
                f"Primeira mensagem: {result.first_message}\n"
                f"Sentimento detectado: {result.sentiment}\n"
                f"Palavras-chave: {', '.join(result.keywords) if result.keywords else '(nenhuma)'}\n\n"
                f"Sugestão de resposta:\n{result.suggested_reply}\n"
            )
            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, content)
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Erro", str(exc))

    def save_reply(self) -> None:
        text = self.output.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Aviso", "Faça uma análise antes de salvar.")
            return

        destination = filedialog.asksaveasfilename(
            title="Salvar resposta",
            defaultextension=".txt",
            filetypes=[("Texto", "*.txt")],
        )
        if not destination:
            return

        Path(destination).write_text(text, encoding="utf-8")
        messagebox.showinfo("Pronto", "Arquivo salvo com sucesso.")


def main() -> None:
    root = tk.Tk()
    app = InstagramDMHelperApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
