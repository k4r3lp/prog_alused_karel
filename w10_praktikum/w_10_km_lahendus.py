import csv
import json


# --- 1. & 6. FAILIDE SISSELUGEMINE ---


def loe_tooted(failinimi):
    """Loeb CSV-failist tooted ja teisendab väljad õigetesse tüüpidesse.

    Tagastab sõnastike järjendi.
    """
    tooted = []
    with open(failinimi, "r", encoding="utf-8") as f:
        lugeja = csv.DictReader(f, delimiter=";")
        for rida in lugeja:
            # Väldime tühje ridu
            if not rida or not any(rida.values()):
                continue
            toode = {
                "inventari_nr": str(rida["inventari_nr"]),
                "nimetus": str(rida["nimetus"]),
                "hind_km_ta": float(rida["hind_km_ta"]),
                "laoseis": int(rida["laoseis"]),
                "km_maar": int(rida["km_maar"]),
            }
            tooted.append(toode)
    return tooted


def loe_tooted_json(failinimi):
    """Loeb tooted JSON-failist.

    JSON-is on arvud juba number-tüüpi, seega täiendav teisendus pole vajalik.
    """
    with open(failinimi, "r", encoding="utf-8") as f:
        return json.load(f)


# --- 2. ABIFUNKTSIOONID ---


def hind_km_ga(hind, maar):
    """Tagastab hinna käibemaksuga, ümardatuna 2 kohani pärast koma.

    Negatiivse hinna korral tõstatab ValueError.
    """
    if hind < 0:
        raise ValueError("Hind ei saa olla negatiivne.")
    return round(hind * (1 + maar / 100), 2)


def uus_maar(maar):
    """Tagastab käibemaksumäära pärast 01.07.2025.

    22% muutub 24%, ülejäänud kehtivad määrad (0, 9, 13, 24) jäävad samaks.
    Vigase määra korral tõstatab ValueError.
    """
    kehtivad_maaradi = {0, 9, 13, 22, 24}
    if maar not in kehtivad_maaradi:
        raise ValueError(f"Tundmatu või kehtetu käibemaksumäär: {maar}")
    if maar == 22:
        return 24
    return maar


def lao_vaartus(tooted, km_ga=False, uue_maaraga=False):
    """Arvutab kõigi toodete hind * laoseis summa.

    km_ga=True korral ümardatakse ühiku hind enne laoseisuga korrutamist.
    """
    summa = 0.0
    for t in tooted:
        laoseis = t["laoseis"]
        if not km_ga:
            hind = t["hind_km_ta"]
        else:
            maar = uus_maar(t["km_maar"]) if uue_maaraga else t["km_maar"]
            hind = hind_km_ga(t["hind_km_ta"], maar)
        summa += hind * laoseis
    return round(summa, 2)


def otsi(tooted, sona):
    """Leiab kõik tooted, mille nimetuses esineb otsitav sõna (tõstutundetult)."""
    sona_lower = sona.lower()
    return [t for t in tooted if sona_lower in t["nimetus"].lower()]


# --- 4. UUE HINNAKIRJA SALVESTAMINE ---


def salvesta_uus_hinnakiri(tooted, valjundfail="tooted_2025_07.csv"):
    """Salvestab uue hinnakirja koos uuendatud käibemaksumäära ja käibemaksuga

    hinnaga.
    """
    valjad = [
        "inventari_nr",
        "nimetus",
        "hind_km_ta",
        "laoseis",
        "km_maar",
        "hind_km_ga",
    ]
    with open(valjundfail, "w", encoding="utf-8", newline="") as f:
        kirjutaja = csv.DictWriter(f, fieldnames=valjad, delimiter=";")
        kirjutaja.writeheader()
        for t in tooted:
            m_uus = uus_maar(t["km_maar"])
            h_km_ga = hind_km_ga(t["hind_km_ta"], m_uus)
            kirjutaja.writerow(
                {
                    "inventari_nr": t["inventari_nr"],
                    "nimetus": t["nimetus"],
                    "hind_km_ta": t["hind_km_ta"],
                    "laoseis": t["laoseis"],
                    "km_maar": m_uus,
                    "hind_km_ga": h_km_ga,
                }
            )


# --- 3. ARUANNE ---


def tee_aruanne(tooted):
    """Prindib ekraanile nõutud aruande ja lisaülesannete tulemused."""
    print("=" * 60)
    print("LAO ARUANNE JA KÄIBEMAKSU TÕUSU MÕJU")
    print("=" * 60)

    # 1. Toodete koguarv
    print(f"1. Toodete arv failis: {len(tooted)}")

    # 2. Toodete arv käibemaksumäärade kaupa
    maarade_jaotus = {}
    for t in tooted:
        m = t["km_maar"]
        maarade_jaotus[m] = maarade_jaotus.get(m, 0) + 1

    print("2. Toodete arv käibemaksumäärade kaupa:")
    for m in sorted(maarade_jaotus.keys()):
        print(f"   - Määr {m}%: {maarade_jaotus[m]} toodet")

    # 3. Laost otsas tooted (laoseis == 0)
    otsas = [t for t in tooted if t["laoseis"] == 0]
    print(f"3. Laost otsas tooteid: {len(otsas)}")

    # 4. Kõige kallim ja odavam toode
    kallim = max(tooted, key=lambda t: t["hind_km_ta"])
    odavam = min(tooted, key=lambda t: t["hind_km_ta"])

    kallim_km_ga = hind_km_ga(kallim["hind_km_ta"], kallim["km_maar"])
    odavam_km_ga = hind_km_ga(odavam["hind_km_ta"], odavam["km_maar"])

    print("4. Äärmuslikud hinnad:")
    print(
        f"   - Kõige kallim: {kallim['inventari_nr']}, {kallim['nimetus']} | "
        f"{kallim['hind_km_ta']:.2f} € km-ta | {kallim_km_ga:.2f} € km-ga"
    )
    print(
        f"   - Kõige odavam: {odavam['inventari_nr']}, {odavam['nimetus']} | "
        f"{odavam['hind_km_ta']:.2f} € km-ta | {odavam_km_ga:.2f} € km-ga"
    )

    v_km_ta = lao_vaartus(tooted, km_ga=False)
    print(f"5. Lao väärtus km-ta: {v_km_ta:,.2f} €".replace(",", " "))

    # 6. Lao koguväärtus km-ga (vana määr vs uus määr)
    v_km_vana = lao_vaartus(tooted, km_ga=True, uue_maaraga=False)
    v_km_uus = lao_vaartus(tooted, km_ga=True, uue_maaraga=True)
    vahe = round(v_km_uus - v_km_vana, 2)

    print("6. Lao väärtus käibemaksuga:")
    print(f"   - vana määr: {v_km_vana:,.2f} €".replace(",", " "))
    print(f"   - uus määr:  {v_km_uus:,.2f} €".replace(",", " "))
    print(f"   - vahe:      {vahe:,.2f} €".replace(",", " "))

    # Lisaülesanded
    print("\n--- LISAÜLESANDED ---")
    piim_tooted = otsi(tooted, "piim")
    print(f"- Toodete arv sõnaga 'piim': {len(piim_tooted)}")

    print("- Lao väärtus käibemaksuga iga käibemaksumäära kaupa:")
    for m in sorted(maarade_jaotus.keys()):
        grupp = [t for t in tooted if t["km_maar"] == m]
        g_vana = lao_vaartus(grupp, km_ga=True, uue_maaraga=False)
        g_uus = lao_vaartus(grupp, km_ga=True, uue_maaraga=True)
        m_u = uus_maar(m)
        print(
            f"   * Määr {m}% (uuesti {m_u}%): vana = {g_vana:,.2f} €, uus = {g_uus:,.2f} €".replace(
                ",", " "
            )
        )


def main():
    failinimi = "tooted.csv"
    try:
        tooted = loe_tooted(failinimi)
    except FileNotFoundError:
        print(f"Faili '{failinimi}' ei leitud. Proovin lugeda JSON-faili...")
        try:
            tooted = loe_tooted_json("tooted.json")
        except FileNotFoundError:
            print("VIGA: Ei leitud 'tooted.csv' ega 'tooted.json' faili.")
            return

    tee_aruanne(tooted)
    salvesta_uus_hinnakiri(tooted, "tooted_2025_07.csv")
    print("\nUus hinnakiri salvestati edukalt faili 'tooted_2025_07.csv'.")


if __name__ == "__main__":
    main()