from collections import Counter
from pprint import pprint

import matplotlib.pyplot as plt
import pandas as pd


def o_kategorisera(text):
    text = text.lower()
    kategorier = {
        "Willys": "Mat",
        "HEMKOP": "Mat",
        "LIDL": "Mat",
        "ICA": "Mat",
        "Systembo": "Alkohol",
        "VATTENFALL": "Elräkning",
        "OKQ8": "Bränsle",
        "SL": "Transport",
        "APPL": "Computer",
        "Överf Mobil":'utLån',
        "SIGNALISTEN": "Hyra",
        "ALMEN": "Hyra",
        "AKADEMIKERFÖ": "Försäkring",
        "Avanza": 'Sparande',
        "Elhandeln":"Elräkning",
        "PENSION": 'Pension',
        "Pizza":"Restaurang",
    }

    for nyckelord, kategori in kategorier.items():
        if nyckelord in text:
            return kategori

    #print(text)  # Kan tas bort om du inte vill ha oklassificerade transaktioner loggade
    return "Vet Ej"

kategorier = {
    "mat & dagligvaror": [
        "hemkop", "lidl 350 solna", "maxi ica storm",
        "ica kvantum so", "ica nara furuv", "willys",
        "coop", "stora coop sun", "rusta - solna",'pressbyran'
        "svens hembager"
    ],
    "transport": [
        "sl", "trängselskat", "okq8", "ingo",
        "parkster", "trafikverk"
    ],
    "boende & fasta utgifter": [
        "signalisten", "vattenfall", "almen",
        "folksam", "akademikerförbundet"
    ],
    "nöjen & restaurang": [
        "olstugan", "pizza stugan", "restaurang okt",
        "thai korat", "oishii sushi", "haga bottega",
        "harry b james", "saffran indisk"
    ],
    "abonnemang & teknik": [
        "spotify", "klarna", "apple",
        "bonner news", "fello"
    ],
    "övriga kostnader": [
        "apoteket", "dressmann", "bauhaus",
        "clas ohlson", "alecta", "musikföreningen", "zettle_",'enerot', 'lindh','mobil','svärd','apot','bustamante'
    ],
    "pension lön":['lön','pension', 'alecta']
}


o_kategorier = {
    'Livsmedel': ['ica', 'coop', 'hemkop', 'willys', 'matbutik', 'lidl'],
    'Restaurang': ['mc donalds', 'sibylla', 'restaurang', 'pizzeria', 'sushi','systembolaget','sergen'],
    'Transport': ['sl', 'uber', 'bensin', 'tanka', 'trafik','ingo','folksam','biltema','körkortsavgift','okq8','parkster'],
    'Nöje': ['spotify', 'netflix', 'bio', 'sf', 'pizza','hembag','lillsved','saffran','thai'],
    'Räkningar': ['el', 'vatten', 'hyra', 'telia', 'comviq'],
    'Inkomst': ['lön', 'insättning', 'överföring från', 'pension', 'alecta', 'trr'],
    'hyra':['signalisten', 'almen'],
    'apotek':['apot'],
    'eneroth': ['enerot','svärd','lindh'],
    'fack': ['ingenj', 'akadem'],
    'överföring':['överf'],
    'avanza':['avanza'],
    'frisör':['zettle'],
    'sport': ['friskis'],
    'datorer': ['apple'],
    'bygg':['hornbach', 'ohlson','rusta','bauhaus'],

    'Övrigt': []
}


def kategorisera(beskrivning):
    beskrivning = str(beskrivning).lower()
    for kategori, nyckelord in kategorier.items():
        if any(nyckelordet in beskrivning for nyckelordet in nyckelord):
            return kategori
    print(beskrivning)
    return 'Övrigt'




df = pd.read_csv("transaktioner.csv", sep=";", decimal=",", parse_dates=["Reskontradatum", "Transaktionsdatum"],skiprows=9)

df["Belopp"] = df["Belopp"].str.replace("−", "-", regex=True)  # Fix Unicode minus
df["Belopp"] = df["Belopp"].str.replace(",", ".", regex=True)  # Replace comma with dot
df["Belopp"] = df["Belopp"].astype(float)  # Convert to float

# Visa de första raderna
#print(df.head(50))

pprint(Counter(df['Text']))


# Skapa en ny kolumn för kategorier
df["Kategori"] = df["Text"].apply(kategorisera)


# Summera utgifter per kategori
print(df.groupby("Kategori")["Belopp"].sum())

df["Månad"] = df["Transaktionsdatum"].dt.to_period("M")

# Summera utgifter per månad
#df["Belopp"] = df["Belopp"].str.replace(",", ".").astype(float)
# månadssummering = df[df["Belopp"] < 0].groupby("Månad")["Belopp"].sum()
#
#
#
# plt.figure(figsize=(10,5))
# månadssummering.plot(kind="bar", color="red")
# månadssummering.plot()
# plt.xlabel("Månad")
# plt.ylabel("Total utgift (SEK)")
# plt.title("Utgifter per månad")
# plt.xticks(rotation=45)
# plt.grid()
# plt.show()


# plt.figure(figsize=(10, 5))
# plt.bar(df["Kategori"], df["Belopp"], color="skyblue")
# plt.xlabel("Kategori")
# plt.ylabel("Belopp (SEK)")
# plt.title("Utgifter per kategori")
# plt.xticks(rotation=45)  # Roterar texten för bättre läsbarhet
# plt.show()

exit(0)
df_grouped = df.groupby("Kategori")["Belopp"].sum()
#
# Skapa en barplot med grupperade data
plt.figure(figsize=(10, 5))
plt.bar(df_grouped.index, abs(df_grouped.values), color="skyblue")
plt.xlabel("Kategori")
plt.ylabel("Totalt belopp (SEK)")
plt.title("Utgifter per kategori")
plt.xticks(rotation=45)  # Roterar texten för bättre läsbarhet
plt.show()


# plt.figure(figsize=(10, 5))
# bars = plt.bar(df_grouped.keys(), [abs(v) for v in df_grouped.values], color="skyblue")
#
# # Lägg till summor ovanför varje stapel
# for bar, value in zip(bars, df_grouped.values):
#     plt.text(bar.get_x() + bar.get_width()/2, abs(value) + 10, f"{value:.2f} SEK",
#              ha="center", fontsize=12, fontweight="bold")
#
# plt.xlabel("Kategori")
# plt.ylabel("Belopp (SEK)")
# plt.title("Utgifter per kategori")
# plt.xticks(rotation=45)
# plt.show()