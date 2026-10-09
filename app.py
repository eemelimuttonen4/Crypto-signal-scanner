rows = []

for coin in coins:
    price_change = coin.get(
        "price_change_percentage_7d_in_currency"
    ) or 0

    change_24h = coin.get(
        "price_change_percentage_24h"
    ) or 0

    volume = coin.get("total_volume") or 0
    market_cap = coin.get("market_cap") or 1

    volume_ratio = volume / market_cap if market_cap else 0

    score = (
        min(max(price_change, 0), 25)
        + min(max(change_24h, 0), 15)
        + min(volume_ratio * 100, 20)
    )

    rows.append({
        "Nimi": coin["name"],
        "Symboli": coin["symbol"].upper(),
        "Hinta USD": coin["current_price"],
        "Muutos 24h %": round(change_24h, 2),
        "Muutos 7pv %": round(price_change, 2),
        "Volyymi USD": volume,
        "Signaalipisteet": round(score, 2),
        "CoinGecko": (
            "https://www.coingecko.com/en/coins/"
            + coin["id"]
        )
    })

df = pd.DataFrame(rows)
df = df.sort_values(
    "Signaalipisteet", ascending=False
)

st.caption(
    "Pisteet ovat kokeellinen seulontamittari, "
    "eivät AI-ennuste eivätkä sijoitusneuvo."
)

minimum_score = st.slider(
    "Vähimmäispisteet",
    min_value=0,
    max_value=60,
    value=5
)

filtered = df[
    df["Signaalipisteet"] >= minimum_score
]

st.subheader("🔎 Kiinnostavimmat kryptot")
st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True
)

st.download_button(
    "Lataa tulokset CSV-tiedostona",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="crypto_signals.csv",
    mime="text/csv"
)
