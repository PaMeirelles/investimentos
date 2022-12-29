import pandas as pd


def filter_all():
    df = pd.read_csv("Interno/statusinvest-busca-avancada.csv", sep=';', thousands='.', decimal=",")
    # taxa = pd.read_csv("taxas")

    # df = df.merge(taxa)
    df.dropna(inplace=True, subset=["TICKER",
                                    "PRECO",
                                    "P/VP",
                                    "LIQUIDEZ MEDIA DIARIA",
                                    "CAGR DIVIDENDOS 3 ANOS",
                                    " CAGR VALOR CORA 3 ANOS",
                                    "DY"])

    df = df[df["P/VP"] < 1.25]
    df = df[df["LIQUIDEZ MEDIA DIARIA"] > 7000]
    df = df[df["CAGR DIVIDENDOS 3 ANOS"] > -12]
    df = df[df[" CAGR VALOR CORA 3 ANOS"] > -12]
    df = df[df["DY"] > 10]
    print(df.sort_values(by="DY"))
    '''
    taxas = {"baixo": 80,
             "medio": 105,
             "alto": 125}

    porta_taxa = {"baixo": [],
                  "medio": [],
                  "alto": []}
    for i, row in df.iterrows():
        for t in taxas.keys():
            if row["BENCHMARK"] < taxas[t]:
                porta_taxa[t].append((taxas[t] - row["BENCHMARK"]) * row["PERFORMANCE"] / 100 + row["FLAT"] + row["BONUS_PERF"])
            else:
                porta_taxa[t].append(row["FLAT"])
    for t in taxas.keys():
        df[t] = porta_taxa[t]
    df = df.sort_values(by="alto")
    print(df[["TICKER", "BENCHMARK", "PERFORMANCE", "baixo", "medio", "alto"]])'''


filter_all()
