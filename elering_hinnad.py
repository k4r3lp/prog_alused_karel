"""Pärib Eleringi kogulehelt (dashboard.elering.ee) tänased päev-ette elektrihinnad,
prindib need ja salvestab faili hinnad.csv.

API dokumentatsioon: https://dashboard.elering.ee/assets/swagger-ui/index.html
Vastus tuleb 15-minutiliste intervallidena: {'timestamp': unix-aeg, 'price': EUR/MWh}.
Ajad arvutatakse Eesti ajavööndis (Europe/Tallinn), sõltumata arvuti enda seadetest.

Käivita:  python elering_hinnad.py
"""
import csv
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

import requests

API = "https://dashboard.elering.ee/api/nps/price"
FAILI_NIMI = "hinnad.csv"
EESTI = ZoneInfo("Europe/Tallinn")


def tanased_hinnad() -> dict[datetime, float]:
    """Tagastab tänased hinnad sõnastikuna {Eesti kellaaeg: hind EUR/MWh}.

    API ootab algus- ja lõpuaega koos ajavööndiga (ISO 8601), lõpp on kaasa arvatud,
    seega küsime Eesti aja järgi 00:00:00 kuni 23:59:59.
    """
    tana = datetime.now(EESTI).date()
    algus = datetime.combine(tana, time.min, tzinfo=EESTI)
    lopp = datetime.combine(tana, time.max, tzinfo=EESTI)
    vastus = requests.get(API, params={"start": algus.isoformat(), "end": lopp.isoformat()})
    vastus.raise_for_status()

    hinnad = {}
    for kirje in vastus.json()["data"]["ee"]:
        aeg = datetime.fromtimestamp(kirje["timestamp"], EESTI)
        hinnad[aeg] = kirje["price"]
    return hinnad


def salvesta_csv(hinnad: dict[datetime, float], failinimi: str) -> None:
    """Kirjutab hinnad CSV-faili: esimesel real veerupäised, edasi aeg;hind."""
    with open(failinimi, "w", newline="") as f:
        kirjutaja = csv.writer(f, delimiter=";")
        kirjutaja.writerow(["aeg", "hind_eur_mwh"])
        for aeg, hind in hinnad.items():
            kirjutaja.writerow([f"{aeg:%Y-%m-%d %H:%M}", hind])


def main() -> None:
    hinnad = tanased_hinnad()
    salvesta_csv(hinnad, FAILI_NIMI)
    print(f"Salvestatud faili {FAILI_NIMI}\n")
    print(f"{datetime.now(EESTI):%Y-%m-%d} elektrihinnad ({len(hinnad)} intervalli):")
    for aeg, hind in hinnad.items():
        print(f"  {aeg:%H:%M}  {hind:7.2f} EUR/MWh")

    odavaim = min(hinnad, key=hinnad.get)
    kalleim = max(hinnad, key=hinnad.get)
    print(f"\nOdavaim 15min: {odavaim:%H:%M} {hinnad[odavaim]:.2f} EUR/MWh")
    print(f"Kalleim 15min: {kalleim:%H:%M} {hinnad[kalleim]:.2f} EUR/MWh")




    hinnad_list = sorted(hinnad.items())
    akna_pikkus = 16  # 4 tundi * 4 (15 min intervallid)

    odavaim_4h_summa = float('inf')
    odavaim_4h_algus = None
    odavaim_4h_lopp = None

    if len(hinnad_list) >= akna_pikkus:
        for i in range(len(hinnad_list) - akna_pikkus + 1):
            aken = hinnad_list[i : i + akna_pikkus]
            akna_summa = sum(hind for aeg, hind in aken)

            if akna_summa < odavaim_4h_summa:
                odavaim_4h_summa = akna_summa
                odavaim_4h_algus = aken[0][0]
                # Viimase intervalli algusaeg + 15 min annab perioodi tegeliku lõpu
                odavaim_4h_lopp = aken[-1][0] + timedelta(minutes=15)

        keskmine_hind = odavaim_4h_summa / akna_pikkus
        print(f"Odavaim 4 järjestikust tundi: {odavaim_4h_algus:%H:%M} - {odavaim_4h_lopp:%H:%M}")
        print(f"Selle 4h perioodi keskmine hind: {keskmine_hind:.2f} EUR/MWh")
    else:
        print("\nEi ole piisavalt andmeid 4-tunnise perioodi arvutamiseks.")

    with open("odav.txt", "w", encoding="utf-8") as f:
        f.write(f"Aeg: {odavaim:%Y-%m-%d %H:%M}\nOdavaim hind: {hinnad[odavaim]:.2f} EUR/MWh\n")

    with open("kallis.txt", "w", encoding="utf-8") as f:
        f.write(f"Aeg: {kalleim:%Y-%m-%d %H:%M}\nKalleim hind: {hinnad[kalleim]:.2f} EUR/MWh\n")

    print("\nSalvestatud failidesse odav.txt ja kallis.txt")


if __name__ == "__main__":
    main()