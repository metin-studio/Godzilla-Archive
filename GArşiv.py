import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
import json
from PIL import Image, ImageTk
from tkinter import messagebox


# =================================================
# VERİLERİ YÜKLE
# =================================================

with open("data/kaiju.json", "r", encoding="utf-8") as file:
    kaiju_data = json.load(file)


# =================================================
# DİL VERİLERİ
# =================================================

LANGUAGE_FILES = {
    "Türkçe": "data/tr.json",
    "English": "data/en.json",
    "日本語": "data/ja.json"
}

current_language = "Türkçe"
language_data = {}

# =================================================
# GÜVENLİ DİL SİSTEMİ
# =================================================

class SafeLanguageDict(dict):

    def __missing__(self, key):

        return f"[{key}]"


def load_language(language_name):

    global language_data
    global current_language

    file_path = LANGUAGE_FILES[language_name]

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            raw_data = json.load(file)

        language_data = SafeLanguageDict(
            raw_data
        )

        current_language = language_name

    except FileNotFoundError:

        language_data = SafeLanguageDict()

        current_language = language_name

    except json.JSONDecodeError:

        language_data = SafeLanguageDict()

        current_language = language_name


load_language(current_language)


# =================================================
# FONT SİSTEMİ
# =================================================

def get_japanese_font():

    available_fonts = set(
        tkfont.families()
    )

    japanese_fonts = [
        "Yu Gothic UI",
        "Yu Gothic",
        "Meiryo",
        "MS Gothic",
        "MS PGothic",
        "Noto Sans CJK JP"
    ]

    for font_name in japanese_fonts:

        if font_name in available_fonts:
            return font_name

    return "Arial"


def get_font(size=11, bold=False):

    weight = (
        "bold"
        if bold
        else
        "normal"
    )

    if current_language == "日本語":

        return (
            get_japanese_font(),
            size,
            weight
        )

    return (
        "Arial",
        size,
        weight
    )


# =================================================
# RENKLER
# =================================================

BG_COLOR = "#111111"
PANEL_COLOR = "#181818"
CARD_COLOR = "#202020"
CARD_HOVER = "#2b1515"

RED = "#b71c1c"
RED_HOVER = "#d32f2f"

TEXT_COLOR = "#f2f2f2"
SECONDARY_TEXT = "#aaaaaa"
BORDER_COLOR = "#333333"


# =================================================
# PENCERE
# =================================================

window = tk.Tk()

window.option_add(
    "*Font",
    get_font(11)
)

window.title(
    language_data["app_title"]
)

window.geometry("1100x750")
window.minsize(900, 650)
window.state("zoomed")

window.configure(
    bg=BG_COLOR
)


# =================================================
# TKINTER TEMA
# =================================================

style = ttk.Style()

try:
    style.theme_use("clam")
except:
    pass


style.configure(
    "Dark.TCombobox",

    fieldbackground=PANEL_COLOR,
    background=PANEL_COLOR,
    foreground=TEXT_COLOR,

    bordercolor=BORDER_COLOR,
    arrowcolor=TEXT_COLOR,

    font=get_font(10)
)


style.map(
    "Dark.TCombobox",

    fieldbackground=[
        ("readonly", PANEL_COLOR)
    ],

    foreground=[
        ("readonly", TEXT_COLOR)
    ]
)


style.configure(
    "Dark.Vertical.TScrollbar",

    background=PANEL_COLOR,
    troughcolor=BG_COLOR,
    bordercolor=BG_COLOR,
    arrowcolor=TEXT_COLOR
)


# =================================================
# ANA BAŞLIK ALANI
# =================================================

header_frame = tk.Frame(
    window,
    bg=BG_COLOR
)

header_frame.pack(
    fill="x",
    padx=40,
    pady=(30, 10)
)


# =================================================
# ANA BAŞLIK
# =================================================

title = tk.Label(
    header_frame,

    text=language_data["main_title"],

    font=get_font(
        30,
        True
    ),

    fg=TEXT_COLOR,
    bg=BG_COLOR
)

title.pack()


# =================================================
# KIRMIZI ÇİZGİ
# =================================================

title_line = tk.Frame(
    header_frame,
    bg=RED,
    height=3
)

title_line.pack(
    fill="x",
    padx=150,
    pady=(8, 8)
)


# =================================================
# ALT BAŞLIK
# =================================================

subtitle = tk.Label(
    header_frame,

    text=language_data["subtitle"],

    font=get_font(11),

    fg=SECONDARY_TEXT,
    bg=BG_COLOR
)

subtitle.pack()


# =================================================
# FİLTRE PANELİ
# =================================================

filter_panel = tk.Frame(
    window,

    bg=PANEL_COLOR,

    highlightbackground=BORDER_COLOR,
    highlightthickness=1
)

filter_panel.pack(
    fill="x",
    padx=40,
    pady=15
)


# =================================================
# ARAMA ALANI
# =================================================

search_frame = tk.Frame(
    filter_panel,
    bg=PANEL_COLOR
)

search_frame.pack(
    side="left",
    padx=20,
    pady=15
)


search_label = tk.Label(
    search_frame,

    text=language_data["search_label"],

    font=get_font(
        9,
        True
    ),

    fg=SECONDARY_TEXT,
    bg=PANEL_COLOR
)

search_label.pack(
    anchor="w"
)


search_box = tk.Entry(
    search_frame,

    width=32,

    font=get_font(11),

    fg=TEXT_COLOR,
    bg="#242424",

    insertbackground=TEXT_COLOR,

    relief="flat",

    highlightbackground=BORDER_COLOR,
    highlightcolor=RED,
    highlightthickness=1
)

search_box.pack(
    pady=(5, 0),
    ipady=7
)


# =================================================
# DÖNEM ALANI
# =================================================

era_frame = tk.Frame(
    filter_panel,
    bg=PANEL_COLOR
)

era_frame.pack(
    side="left",
    padx=20,
    pady=15
)


era_label = tk.Label(
    era_frame,

    text=language_data["era_label"],

    font=get_font(
        9,
        True
    ),

    fg=SECONDARY_TEXT,
    bg=PANEL_COLOR
)

era_label.pack(
    anchor="w"
)


# =================================================
# DÖNEM DEĞERLERİ
# =================================================

def get_era_values():

    return [
        language_data["all_eras"],
        language_data["showa"],
        language_data["heisei"],
        language_data["millennium"],
        language_data["reiwa"]
    ]


era_box = ttk.Combobox(
    era_frame,

    values=get_era_values(),

    state="readonly",

    width=22,

    style="Dark.TCombobox"
)

era_box.pack(
    pady=(5, 0),
    ipady=4
)

era_box.set(
    language_data["all_eras"]
)


# =================================================
# SIRALAMA ALANI
# =================================================

sort_frame = tk.Frame(
    filter_panel,
    bg=PANEL_COLOR
)

sort_frame.pack(
    side="left",
    padx=20,
    pady=15
)


sort_label = tk.Label(
    sort_frame,

    text=language_data["sort_label"],

    font=get_font(
        9,
        True
    ),

    fg=SECONDARY_TEXT,
    bg=PANEL_COLOR
)

sort_label.pack(
    anchor="w"
)


# =================================================
# SIRALAMA DEĞERLERİ
# =================================================

def get_sort_values():

    return [
        language_data["sort_default"],
        language_data["sort_name_az"],
        language_data["sort_name_za"],
        language_data["sort_year_old_new"],
        language_data["sort_year_new_old"]
    ]


sort_box = ttk.Combobox(
    sort_frame,

    values=get_sort_values(),

    state="readonly",

    width=30,

    style="Dark.TCombobox"
)

sort_box.pack(
    pady=(5, 0),
    ipady=4
)

sort_box.set(
    language_data["sort_default"]
)


# =================================================
# DİL ALANI
# =================================================

language_frame = tk.Frame(
    filter_panel,
    bg=PANEL_COLOR
)

language_frame.pack(
    side="left",
    padx=20,
    pady=15
)


language_label = tk.Label(
    language_frame,

    text=language_data["language_label"],

    font=get_font(
        9,
        True
    ),

    fg=SECONDARY_TEXT,
    bg=PANEL_COLOR
)

language_label.pack(
    anchor="w"
)


language_box = ttk.Combobox(
    language_frame,

    values=list(
        LANGUAGE_FILES.keys()
    ),

    state="readonly",

    width=16,

    style="Dark.TCombobox"
)

language_box.pack(
    pady=(5, 0),
    ipady=4
)

language_box.set(
    current_language
)


# =================================================
# KART BAŞLIK ALANI
# =================================================

content_header = tk.Frame(
    window,
    bg=BG_COLOR
)

content_header.pack(
    fill="x",
    padx=40,
    pady=(5, 5)
)


content_title = tk.Label(
    content_header,

    text=language_data["archive_title"],

    font=get_font(
        16,
        True
    ),

    fg=TEXT_COLOR,
    bg=BG_COLOR
)

content_title.pack(
    side="left"
)


count_label = tk.Label(
    content_header,

    text="",

    font=get_font(10),

    fg=SECONDARY_TEXT,
    bg=BG_COLOR
)

count_label.pack(
    side="right"
)


# =================================================
# KARTLAR ALANI
# =================================================

cards_container = tk.Frame(
    window,
    bg=BG_COLOR
)

cards_container.pack(
    fill="both",
    expand=True,
    padx=40,
    pady=(0, 10)
)


# =================================================
# ANA CANVAS
# =================================================

canvas = tk.Canvas(
    cards_container,

    bg=BG_COLOR,

    highlightthickness=0
)

canvas.pack(
    side="left",
    fill="both",
    expand=True
)


# =================================================
# ANA SCROLLBAR
# =================================================

scrollbar = ttk.Scrollbar(
    cards_container,

    orient="vertical",

    command=canvas.yview,

    style="Dark.Vertical.TScrollbar"
)

scrollbar.pack(
    side="right",
    fill="y"
)

canvas.configure(
    yscrollcommand=scrollbar.set
)


# =================================================
# KART FRAME
# =================================================

cards_frame = tk.Frame(
    canvas,
    bg=BG_COLOR
)


canvas_window = canvas.create_window(
    (0, 0),
    window=cards_frame,
    anchor="nw"
)


# =================================================
# SCROLL REGION
# =================================================

def update_scrollregion(event=None):

    canvas.configure(
        scrollregion=canvas.bbox("all")
    )


cards_frame.bind(
    "<Configure>",
    update_scrollregion
)


# =================================================
# BUTONLAR
# =================================================

buttons = {}


# =================================================
# RESIZE
# =================================================

resize_job = None


# =================================================
# DOSYA ADI
# =================================================

def get_image_path(name):

    return (
        "image/"
        +
        name.lower().replace(
            " ",
            "_"
        )
        +
        ".png"
    )


# =================================================
# KART HOVER
# =================================================

def card_enter(button):

    button.configure(
        bg=CARD_HOVER,
        activebackground=CARD_HOVER
    )


def card_leave(button):

    button.configure(
        bg=CARD_COLOR,
        activebackground=CARD_COLOR
    )


# =================================================
# DÖNEM ANAHTARI
# =================================================

def get_era_text(era):

    era_map = {

        "Showa":
            language_data["showa"],

        "Heisei":
            language_data["heisei"],

        "Millennium":
            language_data["millennium"],

        "Reiwa":
            language_data["reiwa"]
    }

    return era_map.get(
        era,
        era
    )


# =================================================
# KAIJU DETAY PENCERESİ
# =================================================

def show_kaiju(
    name,
    year,
    kaiju_type,
    height,
    first_film,
    era,
    description,
    films,
    appearances
):

    info_window = tk.Toplevel(
        window
    )

    info_window.title(
        name
    )

    info_window.geometry(
        "950x700"
    )

    info_window.minsize(
        800,
        600
    )

    info_window.configure(
        bg=BG_COLOR
    )


    # =================================================
    # ANA ALAN
    # =================================================

    main_frame = tk.Frame(
        info_window,
        bg=BG_COLOR
    )

    main_frame.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=20
    )


    # =================================================
    # SOL BİLGİ ALANI
    # =================================================

    left_frame = tk.Frame(
        main_frame,
        bg=BG_COLOR
    )

    left_frame.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(0, 10)
    )


    # =================================================
    # SOL CANVAS
    # =================================================

    info_canvas = tk.Canvas(
        left_frame,
        bg=BG_COLOR,
        highlightthickness=0
    )

    info_canvas.pack(
        side="left",
        fill="both",
        expand=True
    )


    # =================================================
    # SOL SCROLLBAR
    # =================================================

    info_scrollbar = ttk.Scrollbar(
        left_frame,

        orient="vertical",

        command=info_canvas.yview,

        style="Dark.Vertical.TScrollbar"
    )

    info_scrollbar.pack(
        side="right",
        fill="y"
    )

    info_canvas.configure(
        yscrollcommand=info_scrollbar.set
    )


    # =================================================
    # SOL İÇERİK
    # =================================================

    info_content = tk.Frame(
        info_canvas,
        bg=BG_COLOR
    )

    info_canvas_window = info_canvas.create_window(
        (0, 0),
        window=info_content,
        anchor="nw"
    )


    # =================================================
    # SOL SCROLL REGION
    # =================================================

    def update_info_scrollregion(event=None):

        info_canvas.configure(
            scrollregion=info_canvas.bbox(
                "all"
            )
        )


    info_content.bind(
        "<Configure>",
        update_info_scrollregion
    )


    # =================================================
    # SOL GENİŞLİK
    # =================================================

    def update_info_width(event):

        info_canvas.itemconfig(
            info_canvas_window,
            width=event.width
        )


    info_canvas.bind(
        "<Configure>",
        update_info_width
    )


    # =================================================
    # BAŞLIK
    # =================================================

    info_title = tk.Label(
        info_content,

        text=name,

        font=get_font(
            26,
            True
        ),

        fg=TEXT_COLOR,
        bg=BG_COLOR
    )

    info_title.pack(
        pady=(5, 8)
    )


    # =================================================
    # KIRMIZI ÇİZGİ
    # =================================================

    line = tk.Frame(
        info_content,
        bg=RED,
        height=3
    )

    line.pack(
        fill="x",
        padx=50,
        pady=(0, 15)
    )


    # =================================================
    # ÜST BİLGİ
    # =================================================

    top_info_frame = tk.Frame(
        info_content,
        bg=BG_COLOR
    )

    top_info_frame.pack(
        fill="x",
        pady=(0, 20)
    )


    # =================================================
    # TEMEL BİLGİLER
    # =================================================

    basic_info_frame = tk.Frame(
        top_info_frame,

        bg=PANEL_COLOR,

        highlightbackground=BORDER_COLOR,
        highlightthickness=1
    )

    basic_info_frame.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(0, 20)
    )


    information = tk.Label(
        basic_info_frame,

        text=(
            f"{language_data['first_appearance']}:  "
            f"{year}\n\n"

            f"{language_data['type']}:  "
            f"{kaiju_type}\n\n"

            f"{language_data['height']}:  "
            f"{height}\n\n"

            f"{language_data['first_film']}:  "
            f"{first_film}\n\n"

            f"{language_data['era']}:  "
            f"{get_era_text(era)}"
        ),

        font=get_font(11),

        fg=TEXT_COLOR,
        bg=PANEL_COLOR,

        justify="left",
        anchor="nw"
    )

    information.pack(
        fill="both",
        padx=20,
        pady=20
    )


    # =================================================
    # RESİM ALANI
    # =================================================

    image_frame = tk.Frame(
        top_info_frame,

        bg=BG_COLOR,

        width=200,
        height=230
    )

    image_frame.pack(
        side="right"
    )

    image_frame.pack_propagate(
        False
    )


    # =================================================
    # ANA RESİM
    # =================================================

    image_path = get_image_path(
        name
    )

    try:

        image = Image.open(
            image_path
        )

        image = image.resize(
            (180, 220)
        )

        photo = ImageTk.PhotoImage(
            image
        )

        image_label = tk.Label(
            image_frame,
            image=photo,
            bg=BG_COLOR
        )

        image_label.image = photo

        image_label.pack(
            expand=True
        )

    except FileNotFoundError:

        image_label = tk.Label(
            image_frame,

            text=language_data[
                "image_not_found"
            ],

            font=get_font(11),

            fg=SECONDARY_TEXT,
            bg=BG_COLOR
        )

        image_label.pack(
            expand=True
        )


    # =================================================
    # HAKKINDA
    # =================================================

    description_title = tk.Label(
        info_content,

        text=language_data[
            "about"
        ],

        font=get_font(
            16,
            True
        ),

        fg=TEXT_COLOR,
        bg=BG_COLOR
    )

    description_title.pack(
        anchor="w",
        pady=(5, 8)
    )


    description_frame = tk.Frame(
        info_content,

        bg=PANEL_COLOR,

        highlightbackground=BORDER_COLOR,
        highlightthickness=1
    )

    description_frame.pack(
        fill="x",
        pady=(0, 20)
    )


    description_label = tk.Label(
        description_frame,

        text=(
            description
            if description
            else
            language_data[
                "no_description"
            ]
        ),

        font=get_font(11),

        fg=(
            TEXT_COLOR
            if description
            else
            SECONDARY_TEXT
        ),

        bg=PANEL_COLOR,

        wraplength=500,

        justify="left",

        anchor="w"
    )

    description_label.pack(
        fill="x",
        padx=20,
        pady=20
    )


    # =================================================
    # GÖRÜNÜMLER / FORMLAR
    # =================================================

    if appearances:

        appearances_title = tk.Label(
            info_content,

            text=language_data["appearances"],

            font=get_font(
                16,
                True
            ),

            fg=TEXT_COLOR,
            bg=BG_COLOR
        )

        appearances_title.pack(
            anchor="w",
            pady=(5, 8)
        )

        appearances_frame = tk.Frame(
            info_content,
            bg=BG_COLOR
        )

        appearances_frame.pack(
            fill="x",
            pady=(0, 20)
        )

        appearances_frame.grid_columnconfigure(
            0,
            weight=1
        )

        appearances_frame.grid_columnconfigure(
            1,
            weight=1
        )

        for index, appearance in enumerate(
            appearances
        ):

            row = index // 2
            column = index % 2

            appearance_frame = tk.Frame(
                appearances_frame,

                bg=PANEL_COLOR,

                highlightbackground=BORDER_COLOR,
                highlightthickness=1
            )

            appearance_frame.grid(
                row=row,
                column=column,

                padx=8,
                pady=8,

                sticky="nsew"
            )

            # -----------------------------------------
            # GÖRÜNÜM ADI
            # -----------------------------------------

            appearance_key = appearance.get(
                "label_key",
                ""
            )

            appearance_label = language_data.get(
                "appearance_labels",
                {}
            ).get(
                appearance_key,
                appearance.get(
                    "label",
                    get_era_text(
                        appearance.get(
                            "era",
                            ""
                        )
                    )
                )
            )

            appearance_title = tk.Label(
                appearance_frame,

                text=appearance_label,

                font=get_font(
                    12,
                    True
                ),

                fg=RED,
                bg=PANEL_COLOR
            )

            appearance_title.pack(
                pady=(10, 5)
            )

            # -----------------------------------------
            # RESİM
            # -----------------------------------------

            appearance_image_path = (
                "image/"
                +
                appearance.get(
                    "image",
                    ""
                )
            )

            try:

                appearance_image = Image.open(
                    appearance_image_path
                )

                appearance_image = (
                    appearance_image.resize(
                        (150, 185)
                    )
                )

                appearance_photo = ImageTk.PhotoImage(
                    appearance_image
                )

                appearance_image_label = tk.Label(
                    appearance_frame,

                    image=appearance_photo,

                    bg=PANEL_COLOR
                )

                appearance_image_label.image = (
                    appearance_photo
                )

                appearance_image_label.pack(
                    pady=5
                )

            except FileNotFoundError:

                appearance_image_label = tk.Label(
                    appearance_frame,

                    text=language_data[
                        "image_not_found"
                    ],

                    font=get_font(
                        10
                    ),

                    fg=SECONDARY_TEXT,
                    bg=PANEL_COLOR
                )

                appearance_image_label.pack(
                    pady=60
                )

            # -----------------------------------------
            # YIL
            # -----------------------------------------

            appearance_year = tk.Label(
                appearance_frame,

                text=str(
                    appearance.get(
                        "year",
                        ""
                    )
                ),

                font=get_font(
                    10
                ),

                fg=SECONDARY_TEXT,
                bg=PANEL_COLOR
            )

            appearance_year.pack(
                pady=(0, 10)
            )


    # =================================================
    # SAĞ FİLM ALANI
    # =================================================

    right_frame = tk.Frame(
        main_frame,
        bg=BG_COLOR,
        width=350
    )


    # =================================================
    # FİLMLER BAŞLIK
    # =================================================

    films_title = tk.Label(
        right_frame,

        text=language_data[
            "films"
        ],

        font=get_font(
            16,
            True
        ),

        fg=TEXT_COLOR,
        bg=BG_COLOR
    )

    films_title.pack(
        pady=(0, 10)
    )


    # =================================================
    # FİLM PANELİ
    # =================================================

    films_panel = tk.Frame(
        right_frame,

        bg=PANEL_COLOR,

        highlightbackground=BORDER_COLOR,
        highlightthickness=1
    )

    films_panel.pack(
        fill="both",
        expand=True
    )


    # =================================================
    # FİLM CANVAS
    # =================================================

    films_canvas = tk.Canvas(
        films_panel,

        bg=PANEL_COLOR,

        highlightthickness=0
    )

    films_canvas.pack(
        side="left",
        fill="both",
        expand=True
    )


    # =================================================
    # FİLM SCROLLBAR
    # =================================================

    films_scrollbar = ttk.Scrollbar(
        films_panel,

        orient="vertical",

        command=films_canvas.yview,

        style="Dark.Vertical.TScrollbar"
    )

    films_scrollbar.pack(
        side="right",
        fill="y"
    )

    films_canvas.configure(
        yscrollcommand=films_scrollbar.set
    )


    # =================================================
    # FİLM İÇERİK
    # =================================================

    films_content = tk.Frame(
        films_canvas,
        bg=PANEL_COLOR
    )

    films_canvas_window = (
        films_canvas.create_window(
            (0, 0),
            window=films_content,
            anchor="nw"
        )
    )


    def update_films_scrollregion(
        event=None
    ):

        films_canvas.configure(
            scrollregion=films_canvas.bbox(
                "all"
            )
        )


    films_content.bind(
        "<Configure>",
        update_films_scrollregion
    )


    def update_films_width(event):

        films_canvas.itemconfig(
            films_canvas_window,
            width=event.width
        )


    films_canvas.bind(
        "<Configure>",
        update_films_width
    )


    # =================================================
    # DÖNEM SIRASI
    # =================================================

    era_order = [
        "Showa",
        "Heisei",
        "Millennium",
        "Reiwa"
    ]


    # =================================================
    # FİLMLERİ GRUPLA
    # =================================================

    grouped_films = {}


    for film in films:

        film_era = film.get(
            "era",
            "Other"
        )

        if film_era not in grouped_films:

            grouped_films[film_era] = []

        grouped_films[
            film_era
        ].append(
            film
        )


    # =================================================
    # FİLMLERİ GÖSTER
    # =================================================

    film_number = 1


    for era_name in era_order:

        if era_name not in grouped_films:
            continue


        era_title = tk.Label(
            films_content,

            text=get_era_text(
                era_name
            ).upper(),

            font=get_font(
                12,
                True
            ),

            fg=RED,

            bg=PANEL_COLOR,

            anchor="w"
        )

        era_title.pack(
            fill="x",
            padx=15,
            pady=(15, 8)
        )


        for film in grouped_films[
            era_name
        ]:

            film_title = film.get(
                "title",
                language_data.get(
                    "unknown",
                    "Bilinmeyen Film"
                )
            )


            film_year = film.get(
                "year",
                ""
            )


            film_director = film.get(
                "director",
                language_data[
                    "unknown"
                ]
            )


            film_label = tk.Label(
                films_content,

                text=(
                    f"{film_number}. "
                    f"{film_title} "
                    f"({film_year})\n"

                    f"    "
                    f"{language_data['director']}: "
                    f"{film_director}"
                ),

                font=get_font(10),

                fg=TEXT_COLOR,

                bg=PANEL_COLOR,

                anchor="w",

                justify="left",

                wraplength=280
            )

            film_label.pack(
                fill="x",
                padx=15,
                pady=7
            )

            film_number += 1


    # =================================================
    # FİLM YOKSA
    # =================================================

    if not films:

        no_film_label = tk.Label(
            films_content,

            text=language_data[
                "no_films"
            ],

            font=get_font(10),

            fg=SECONDARY_TEXT,

            bg=PANEL_COLOR,

            wraplength=260
        )

        no_film_label.pack(
            padx=15,
            pady=20
        )


    # =================================================
    # MOUSE SCROLL - SOL
    # =================================================

    def info_mouse_scroll(event):

        info_canvas.yview_scroll(
            int(
                -1 *
                (event.delta / 120)
            ),
            "units"
        )


    # =================================================
    # MOUSE SCROLL - SAĞ
    # =================================================

    def films_mouse_scroll(event):

        films_canvas.yview_scroll(
            int(
                -1 *
                (event.delta / 120)
            ),
            "units"
        )


    # =================================================
    # MOUSE ENTER / LEAVE
    # =================================================

    def bind_info_scroll(event):

        info_canvas.bind_all(
            "<MouseWheel>",
            info_mouse_scroll
        )


    def unbind_info_scroll(event):

        info_canvas.unbind_all(
            "<MouseWheel>"
        )


    def bind_films_scroll(event):

        films_canvas.bind_all(
            "<MouseWheel>",
            films_mouse_scroll
        )


    def unbind_films_scroll(event):

        films_canvas.unbind_all(
            "<MouseWheel>"
        )


    info_canvas.bind(
        "<Enter>",
        bind_info_scroll
    )

    info_canvas.bind(
        "<Leave>",
        unbind_info_scroll
    )


    films_canvas.bind(
        "<Enter>",
        bind_films_scroll
    )

    films_canvas.bind(
        "<Leave>",
        unbind_films_scroll
    )


    # =================================================
    # PENCERE AYARLARI
    # =================================================

    info_window.transient(
        window
    )

    info_window.grab_set()

    info_window.focus_force()


# =================================================
# KAIJU AÇ
# =================================================

def open_kaiju(name):

    data = kaiju_data.get(name)

    if not data:
        return

    show_kaiju(
        name,

        data.get(
            "year",
            "?"
        ),

        data.get(
            "kaiju_type",
            language_data["unknown"]
        ),

        data.get(
            "height",
            language_data["unknown"]
        ),

        data.get(
            "first_film",
            language_data["unknown"]
        ),

        data.get(
            "era",
            ""
        ),

        data.get(
            "description",
            ""
        ),

        data.get(
            "films",
            []
        ),

        data.get(
            "appearances",
            []
        )
    )


# =================================================
# KAIJU KARTI
# =================================================

def create_kaiju_card(
    name,
    row,
    column
):

    image_path = get_image_path(
        name
    )


    try:

        image = Image.open(
            image_path
        )

        image = image.resize(
            (105, 130)
        )

        photo = ImageTk.PhotoImage(
            image
        )

    except FileNotFoundError:

        photo = None


    button = tk.Button(
        cards_frame,

        text=name,

        image=photo,

        compound="top",

        width=130,
        height=170,

        font=get_font(
            10,
            True
        ),

        fg=TEXT_COLOR,

        bg=CARD_COLOR,

        activeforeground=TEXT_COLOR,

        activebackground=CARD_HOVER,

        relief="flat",

        bd=0,

        highlightbackground=BORDER_COLOR,

        highlightcolor=RED,

        highlightthickness=1,

        cursor="hand2",

        command=lambda kaiju_name=name:
            open_kaiju(
                kaiju_name
            )
    )


    if photo is not None:

        button.image = photo


    button.bind(
        "<Enter>",

        lambda event,
        b=button:
            card_enter(b)
    )


    button.bind(
        "<Leave>",

        lambda event,
        b=button:
            card_leave(b)
    )


    button.grid(
        row=row,

        column=column,

        padx=10,

        pady=10
    )


    buttons[name] = button

# =================================================
# KARTLARI YENİLE
# =================================================

def refresh_cards(event=None):

    # =================================================
    # ESKİ KARTLARI SİL
    # =================================================

    for button in buttons.values():
        button.destroy()

    buttons.clear()


    # =================================================
    # ARAMA METNİ
    # =================================================

    search_text = (
        search_box.get()
        .lower()
        .strip()
    )


    # =================================================
    # SEÇİLEN DÖNEM
    # =================================================

    selected_era = era_box.get()


    # =================================================
    # SEÇİLEN SIRALAMA
    # =================================================

    selected_sort = sort_box.get()


    # =================================================
    # KAIJU LİSTESİ
    # =================================================

    sorted_names = list(
        kaiju_data.keys()
    )


    # =================================================
    # SIRALAMA
    # =================================================

    if selected_sort == language_data[
        "sort_name_az"
    ]:

        sorted_names.sort(
            key=lambda name:
                name.lower()
        )


    elif selected_sort == language_data[
        "sort_name_za"
    ]:

        sorted_names.sort(
            key=lambda name:
                name.lower(),
            reverse=True
        )


    elif selected_sort == language_data[
        "sort_year_old_new"
    ]:

        sorted_names.sort(
            key=lambda name:
                kaiju_data[name].get(
                    "year",
                    0
                )
        )


    elif selected_sort == language_data[
        "sort_year_new_old"
    ]:

        sorted_names.sort(
            key=lambda name:
                kaiju_data[name].get(
                    "year",
                    0
                ),
            reverse=True
        )


    # =================================================
    # DÖNEM FİLTRE HARİTASI
    # =================================================

    era_filter_map = {

        language_data["showa"]:
            "Showa",

        language_data["heisei"]:
            "Heisei",

        language_data["millennium"]:
            "Millennium",

        language_data["reiwa"]:
            "Reiwa"
    }


    # =================================================
    # FİLTRELENMİŞ KAIJU LİSTESİ
    # =================================================

    filtered_names = []


    for name in sorted_names:

        data = kaiju_data[name]


        # =================================================
        # DÖNEM FİLTRESİ
        # =================================================

        if selected_era != language_data[
            "all_eras"
        ]:

            selected_era_key = era_filter_map.get(
                selected_era
            )


            if data.get(
                "era",
                ""
            ) != selected_era_key:

                continue


        # =================================================
        # ARAMA
        # =================================================

        search_match = False


        # -------------------------------------------------
        # KAIJU ADI
        # -------------------------------------------------

        if search_text in str(
            name
        ).lower():

            search_match = True


        # -------------------------------------------------
        # İLK ÇIKIŞ YILI
        # -------------------------------------------------

        if search_text in str(
            data.get(
                "year",
                ""
            )
        ).lower():

            search_match = True


        # -------------------------------------------------
        # TÜR
        # -------------------------------------------------

        if search_text in str(
            data.get(
                "kaiju_type",
                ""
            )
        ).lower():

            search_match = True


        # -------------------------------------------------
        # İLK FİLM
        # -------------------------------------------------

        if search_text in str(
            data.get(
                "first_film",
                ""
            )
        ).lower():

            search_match = True


        # =================================================
        # KAIJU DÖNEMİ
        # =================================================

        era_key = data.get(
            "era",
            ""
        )


        era_text = get_era_text(
            era_key
        )


        if search_text in str(
            era_key
        ).lower():

            search_match = True


        if search_text in str(
            era_text
        ).lower():

            search_match = True


        # =================================================
        # FİLMLER
        # =================================================

        for film in data.get(
            "films",
            []
        ):

            film_title = film.get(
                "title",
                ""
            )

            film_year = film.get(
                "year",
                ""
            )

            film_era = film.get(
                "era",
                ""
            )


            # Film adı
            if search_text in str(
                film_title
            ).lower():

                search_match = True


            # Film yılı
            if search_text in str(
                film_year
            ).lower():

                search_match = True


            # Film dönemi
            if search_text in str(
                film_era
            ).lower():

                search_match = True


            # Film döneminin çevrilmiş adı
            film_era_text = get_era_text(
                film_era
            )


            if search_text in str(
                film_era_text
            ).lower():

                search_match = True


        # =================================================
        # GÖRÜNÜMLER / FORMLAR
        # =================================================

        for appearance in data.get(
            "appearances",
            []
        ):

            appearance_year = appearance.get(
                "year",
                ""
            )

            appearance_era = appearance.get(
                "era",
                ""
            )

            appearance_label = appearance.get(
                "label",
                ""
            )

            appearance_key = appearance.get(
                "label_key",
                ""
            )


            # Görünüm yılı
            if search_text in str(
                appearance_year
            ).lower():

                search_match = True


            # Görünüm dönemi
            if search_text in str(
                appearance_era
            ).lower():

                search_match = True


            # Çevrilmiş görünüm dönemi
            appearance_era_text = get_era_text(
                appearance_era
            )


            if search_text in str(
                appearance_era_text
            ).lower():

                search_match = True


            # JSON'daki label
            if search_text in str(
                appearance_label
            ).lower():

                search_match = True


            # label_key
            if search_text in str(
                appearance_key
            ).lower():

                search_match = True


            # Yerelleştirilmiş görünüm adı
            localized_appearance_label = (
                language_data.get(
                    "appearance_labels",
                    {}
                ).get(
                    appearance_key,
                    ""
                )
            )


            if search_text in str(
                localized_appearance_label
            ).lower():

                search_match = True


        # =================================================
        # SONUCA EKLE
        # =================================================

        if not search_match:
            continue


        filtered_names.append(
            name
        )


    # =================================================
    # SÜTUN SAYISI
    # =================================================

    available_width = canvas.winfo_width()

    card_total_width = 150

    columns = max(
        1,
        available_width //
        card_total_width
    )


    # =================================================
    # GRID SÜTUNLARINI TEMİZLE
    # =================================================

    for column in range(20):

        cards_frame.grid_columnconfigure(
            column,
            weight=0
        )


    # =================================================
    # GRID SÜTUNLARINI EŞİT DAĞIT
    # =================================================

    for column in range(
        columns
    ):

        cards_frame.grid_columnconfigure(
            column,
            weight=1
        )


    # =================================================
    # KARTLARI OLUŞTUR
    # =================================================

    for index, name in enumerate(
        filtered_names
    ):

        row = index // columns

        column = index % columns

        create_kaiju_card(
            name,
            row,
            column
        )


    # =================================================
    # KAYIT SAYISI
    # =================================================

    count_label.config(
        text=(
            f"{len(filtered_names)} "
            f"{language_data['registered']}"
        )
    )


    # =================================================
    # SCROLL BÖLGESİ
    # =================================================

    cards_frame.update_idletasks()

    canvas.configure(
        scrollregion=canvas.bbox(
            "all"
        )
    )


    # =================================================
    # EN ÜSTE DÖN
    # =================================================

    canvas.yview_moveto(
        0
    )

# =================================================
# DİL DEĞİŞTİR
# =================================================

def change_language(event=None):

    selected_language = language_box.get()

    if (
        selected_language
        not in LANGUAGE_FILES
    ):

        return


    # =================================================
    # ESKİ DEĞERLERİ SAKLA
    # =================================================

    current_era = era_box.get()
    current_sort = sort_box.get()


    # =================================================
    # DİLİ YÜKLE
    # =================================================

    load_language(
        selected_language
    )


    # =================================================
    # GENEL FONT
    # =================================================

    window.option_add(
        "*Font",
        get_font(11)
    )


    style.configure(
        "Dark.TCombobox",
        font=get_font(10)
    )


    # =================================================
    # PENCERE BAŞLIĞI
    # =================================================

    window.title(
        language_data[
            "app_title"
        ]
    )


    # =================================================
    # ANA BAŞLIKLAR
    # =================================================

    title.config(
        text=language_data[
            "main_title"
        ],

        font=get_font(
            30,
            True
        )
    )


    subtitle.config(
        text=language_data[
            "subtitle"
        ],

        font=get_font(11)
    )


    content_title.config(
        text=language_data[
            "archive_title"
        ],

        font=get_font(
            16,
            True
        )
    )


    count_label.config(
        font=get_font(10)
    )


    # =================================================
    # ARAMA
    # =================================================

    search_label.config(
        text=language_data[
            "search_label"
        ],

        font=get_font(
            9,
            True
        )
    )


    search_box.config(
        font=get_font(11)
    )


    # =================================================
    # DÖNEM
    # =================================================

    old_era_map = {

        "Tüm Dönemler":
            "all_eras",

        "All Eras":
            "all_eras",

        "すべての時代":
            "all_eras",

        "Showa Dönemi":
            "showa",

        "Showa Era":
            "showa",

        "昭和":
            "showa",

        "Heisei Dönemi":
            "heisei",

        "Heisei Era":
            "heisei",

        "平成":
            "heisei",

        "Millennium Dönemi":
            "millennium",

        "Millennium Era":
            "millennium",

        "ミレニアム":
            "millennium",

        "Reiwa Dönemi":
            "reiwa",

        "Reiwa Era":
            "reiwa",

        "令和":
            "reiwa"
    }


    era_box["values"] = (
        get_era_values()
    )


    era_label.config(
        text=language_data[
            "era_label"
        ],

        font=get_font(
            9,
            True
        )
    )


    era_key = old_era_map.get(
        current_era,
        "all_eras"
    )


    era_box.set(
        language_data[
            era_key
        ]
    )


    # =================================================
    # SIRALAMA
    # =================================================

    old_sort_map = {

        "Varsayılan":
            "sort_default",

        "Default":
            "sort_default",

        "デフォルト":
            "sort_default",

        "İsim: A-Z":
            "sort_name_az",

        "Name: A-Z":
            "sort_name_az",

        "名前：A-Z":
            "sort_name_az",

        "İsim: Z-A":
            "sort_name_za",

        "Name: Z-A":
            "sort_name_za",

        "名前：Z-A":
            "sort_name_za",

        "İlk çıkış yılı: Eskiden yeniye":
            "sort_year_old_new",

        "First appearance: Oldest to newest":
            "sort_year_old_new",

        "初登場年：古い順":
            "sort_year_old_new",

        "İlk çıkış yılı: Yeniden eskiye":
            "sort_year_new_old",

        "First appearance: Newest to oldest":
            "sort_year_new_old",

        "初登場年：新しい順":
            "sort_year_new_old"
    }


    sort_box["values"] = (
        get_sort_values()
    )


    sort_label.config(
        text=language_data[
            "sort_label"
        ],

        font=get_font(
            9,
            True
        )
    )


    sort_key = old_sort_map.get(
        current_sort,
        "sort_default"
    )


    sort_box.set(
        language_data[
            sort_key
        ]
    )


    # =================================================
    # DİL ETİKETİ
    # =================================================

    language_label.config(
        text=language_data[
            "language_label"
        ],

        font=get_font(
            9,
            True
        )
    )


    # =================================================
    # KARTLARI YENİLE
    # =================================================

    refresh_cards()


# =================================================
# CANVAS BOYUTU DEĞİŞİNCE
# =================================================

def update_canvas_width(event):

    global resize_job

    canvas.itemconfig(
        canvas_window,
        width=event.width
    )


    if resize_job is not None:

        window.after_cancel(
            resize_job
        )


    resize_job = window.after(
        200,
        refresh_cards
    )


canvas.bind(
    "<Configure>",
    update_canvas_width
)


# =================================================
# ANA EKRAN MOUSE SCROLL
# =================================================

def mouse_scroll(event):

    canvas.yview_scroll(
        int(
            -1 *
            (event.delta / 120)
        ),
        "units"
    )


canvas.bind_all(
    "<MouseWheel>",
    mouse_scroll
)


# =================================================
# OLAYLARI BAĞLA
# =================================================

era_box.bind(
    "<<ComboboxSelected>>",
    refresh_cards
)


sort_box.bind(
    "<<ComboboxSelected>>",
    refresh_cards
)


search_box.bind(
    "<KeyRelease>",
    refresh_cards
)


language_box.bind(
    "<<ComboboxSelected>>",
    change_language
)


# =================================================
# İLK AÇILIŞ
# =================================================

refresh_cards()


# =================================================
# PROGRAMI BAŞLAT
# =================================================

window.mainloop()