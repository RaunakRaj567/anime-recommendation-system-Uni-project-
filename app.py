import random
import tkinter as tk
from tkinter import messagebox, ttk
from recommender import AnimeRecommender


class AnimeRecommenderApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Anime Recommendation System")
        self.root.geometry("1050x660")
        self.root.minsize(900, 580)

        # Apply clean TTK style theme
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self._configure_styles()

        # Initialize recommender engine (loads anime_recommender.pkl)
        try:
            self.recommender = AnimeRecommender()
            self.all_titles = self.recommender.get_all_titles()
        except Exception as e:
            messagebox.showerror("Error Loading Model", f"Could not load pickle file or dataset:\n{e}")
            self.all_titles = []

        # Build UI layout
        self._create_header()
        self._create_controls()
        self._create_results_table()
        self._create_details_panel()
        self._create_status_bar()

        # Populate initial dropdown titles
        self._populate_titles()

    def _configure_styles(self):
        """Customizes TTK widget styles."""
        self.style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground="#1e293b", background="#e2e8f0")
        self.style.configure("SubHeader.TLabel", font=("Segoe UI", 9), foreground="#64748b", background="#e2e8f0")

        self.style.configure("TFrame", background="#f8fafc")
        self.style.configure("Header.TFrame", background="#e2e8f0")

        self.style.configure("TLabelframe", background="#f8fafc", font=("Segoe UI", 10, "bold"))
        self.style.configure("TLabelframe.Label", background="#f8fafc", foreground="#0f172a")

        self.style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), background="#2563eb", foreground="#ffffff")
        self.style.map("Primary.TButton", background=[("active", "#1d4ed8")])

        self.style.configure("Secondary.TButton", font=("Segoe UI", 9), background="#e2e8f0", foreground="#0f172a")
        self.style.map("Secondary.TButton", background=[("active", "#cbd5e1")])

        self.style.configure("Treeview", font=("Segoe UI", 9), rowheight=26)
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#cbd5e1", foreground="#0f172a")
        self.style.map("Treeview", background=[("selected", "#3b82f6")], foreground=[("selected", "#ffffff")])

    def _create_header(self):
        header_frame = ttk.Frame(self.root, style="Header.TFrame", padding=(15, 12))
        header_frame.pack(fill="x", side="top")

        title_lbl = ttk.Label(header_frame, text="🎌 Anime Recommendation System", style="Header.TLabel")
        title_lbl.pack(anchor="w")

        subtitle_lbl = ttk.Label(
            header_frame,
            text="Powered by Content-Based Filtering (TF-IDF & Cosine Similarity)",
            style="SubHeader.TLabel"
        )
        subtitle_lbl.pack(anchor="w")

    def _create_controls(self):
        ctrl_frame = ttk.LabelFrame(self.root, text=" Search & Settings ", padding=(12, 10))
        ctrl_frame.pack(fill="x", padx=15, pady=10)

        # Title Selection
        ttk.Label(ctrl_frame, text="Select or Search Anime Title:", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.title_var = tk.StringVar()
        self.title_cb = ttk.Combobox(ctrl_frame, textvariable=self.title_var, width=45, font=("Segoe UI", 9))
        self.title_cb.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        self.title_cb.bind("<KeyRelease>", self._on_title_keyrelease)

        # Top N Spinbox
        ttk.Label(ctrl_frame, text="Top Recommendations:", font=("Segoe UI", 9, "bold")).grid(row=0, column=2, sticky="w", padx=(15, 5), pady=5)

        self.top_n_var = tk.IntVar(value=10)
        self.top_n_spin = ttk.Spinbox(ctrl_frame, from_=1, to=50, textvariable=self.top_n_var, width=5, font=("Segoe UI", 9))
        self.top_n_spin.grid(row=0, column=3, sticky="w", padx=5, pady=5)

        # Buttons
        btn_frame = ttk.Frame(ctrl_frame)
        btn_frame.grid(row=0, column=4, sticky="e", padx=(15, 5), pady=5)

        rec_btn = ttk.Button(btn_frame, text="Get Recommendations", style="Primary.TButton", command=self.get_recommendations)
        rec_btn.pack(side="left", padx=3)

        rand_btn = ttk.Button(btn_frame, text="Random Title", style="Secondary.TButton", command=self.select_random_title)
        rand_btn.pack(side="left", padx=3)

    def _create_results_table(self):
        table_frame = ttk.LabelFrame(self.root, text=" Recommended Anime ", padding=(10, 8))
        table_frame.pack(fill="both", expand=True, padx=15, pady=5)

        columns = ("rank", "title", "similarity", "rating", "episodes", "year", "genres")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("rank", text="#")
        self.tree.heading("title", text="Anime Title")
        self.tree.heading("similarity", text="Match %")
        self.tree.heading("rating", text="Rating")
        self.tree.heading("episodes", text="Episodes")
        self.tree.heading("year", text="Year")
        self.tree.heading("genres", text="Genres")

        self.tree.column("rank", width=40, anchor="center")
        self.tree.column("title", width=250, anchor="w")
        self.tree.column("similarity", width=80, anchor="center")
        self.tree.column("rating", width=65, anchor="center")
        self.tree.column("episodes", width=75, anchor="center")
        self.tree.column("year", width=65, anchor="center")
        self.tree.column("genres", width=360, anchor="w")

        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        self.tree.bind("<<TreeviewSelect>>", self._on_select_item)

    def _create_details_panel(self):
        self.details_frame = ttk.LabelFrame(self.root, text=" Selected Anime Details ", padding=(12, 8))
        self.details_frame.pack(fill="x", padx=15, pady=5)

        self.details_lbl = ttk.Label(
            self.details_frame,
            text="Click on any anime in the recommendations table above to view full details.",
            font=("Segoe UI", 9, "italic"),
            foreground="#475569"
        )
        self.details_lbl.pack(anchor="w")

    def _create_status_bar(self):
        self.status_var = tk.StringVar(value=f"Ready. Loaded {len(self.all_titles):,} anime records from anime_recommender.pkl.")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief="sunken", anchor="w", padding=(10, 4), font=("Segoe UI", 8))
        status_bar.pack(fill="x", side="bottom")

    def _populate_titles(self):
        if self.all_titles:
            self.title_cb["values"] = self.all_titles
            self.title_cb.set(self.all_titles[0])

    def _on_title_keyrelease(self, event):
        """Filters combobox dropdown list as user types."""
        val = self.title_var.get()
        if not val:
            self.title_cb["values"] = self.all_titles
        else:
            filtered = [t for t in self.all_titles if val.lower() in t.lower()]
            self.title_cb["values"] = filtered[:30]

    def select_random_title(self):
        """Selects a random title for quick demonstration."""
        if self.all_titles:
            random_title = random.choice(self.all_titles)
            self.title_var.set(random_title)
            self.get_recommendations()

    def get_recommendations(self):
        """Fetches and renders recommendations directly from pickled model."""
        title = self.title_var.get().strip()
        top_n = self.top_n_var.get()

        if not title:
            messagebox.showwarning("Missing Title", "Please select or type an anime title.")
            return

        self.status_var.set(f"Generating recommendations for '{title}'...")
        self.root.update_idletasks()

        # Clear existing rows
        for item in self.tree.get_children():
            self.tree.delete(item)

        results = self.recommender.recommend(title=title, top_n=top_n)
        if results is None:
            messagebox.showerror("Not Found", f"Anime title '{title}' was not found in the dataset.")
            self.status_var.set("Title not found.")
            return

        # Insert results into Treeview
        for res in results:
            self.tree.insert(
                "",
                "end",
                values=(
                    res["rank"],
                    res["anime_title"],
                    f"{res['similarity_score']}%",
                    res["rating"],
                    res["episodes"],
                    res["year_of_release"],
                    res["genres"]
                )
            )

        self.status_var.set(f"Displaying top {len(results)} recommendations for '{title}'.")

    def _on_select_item(self, event):
        """Displays details when a treeview row is selected."""
        selected_items = self.tree.selection()
        if not selected_items:
            return

        item_id = selected_items[0]
        vals = self.tree.item(item_id, "values")
        if not vals:
            return

        rank, title, score, rating, eps, year, genres = vals
        detail_text = f"Title: {title}  |  Match Score: {score}  |  Rating: ⭐ {rating}/10  |  Episodes: {eps}  |  Release Year: {year}\nGenres: {genres}"
        self.details_lbl.config(text=detail_text, font=("Segoe UI", 9, "bold"), foreground="#0f172a")


def main():
    root = tk.Tk()
    app = AnimeRecommenderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
