import pandas as pd
import csv


def read_1d_csv(name):
    new_a = []
    with open(name, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            new_a.extend(row)

    return new_a


def filter_all():
    df = pd.read_csv("statusinvest-busca-avancada.csv", sep=';', thousands='.', decimal=",")
    print(df.shape)

    df.dropna(inplace=True, subset=['TICKER', 'PRECO', ' LIQUIDEZ MEDIA DIARIA', 'CAGR LUCROS 5 ANOS'])
    print(df.shape)

    df = df[df["TICKER"].str[4] == '3']
    print(df.shape)

    estatais = read_1d_csv('estatais')
    df = df[~df[['TICKER']].isin(estatais).any(axis=1)]
    print(df.shape)
    df = df[df[" LIQUIDEZ MEDIA DIARIA"].astype(float) >= 700000]
    print(df.shape)
    graham()
    print(df.shape)
    gr = pd.read_csv("analise.csv")
    df = df.merge(gr)
    df = df[df["Graham"] < 1]

    print(df.shape)
    df = df[df['CAGR LUCROS 5 ANOS'] >= 30]
    print(df.shape)
    preju = pd.read_csv("prejuizo")
    df = df.merge(preju)
    df = df[df["ALL"] == 0]
    print(df.shape)

    ban = pd.read_csv("ban")
    df = df.merge(ban, how="outer", left_on="TICKER", right_on="BAN")
    df = df[df["BAN"] != df["TICKER"]]
    print(df.shape)
    df.to_csv("filtrado.csv", index=False)


def extrai():
    df = pd.read_csv("statusinvest-busca-avancada.csv", sep=';', thousands='.', decimal=",")
    df = df[["TICKER"]].copy()
    df.to_csv("analise.csv", index=False)


def graham():
    df1 = pd.read_csv("statusinvest-busca-avancada.csv", sep=';', thousands='.', decimal=",")
    df2 = pd.read_csv("analise.csv")
    df2["Graham"] = df1["PRECO"] / (df1[" VPA"].astype(float) * df1[" LPA"].astype(float) * 22.5) ** 0.5
    df2.sort_values(by="Graham", inplace=True)
    df2.dropna(inplace=True)
    df2.to_csv("analise.csv", index=False)


def teste():
    s = 0
    tudo = pd.read_csv("statusinvest-busca-avancada.csv", sep=';', thousands='.', decimal=",")
    tenho = pd.read_csv("possui.csv")
    novo = tudo.merge(tenho)
    su = novo['QTD'].astype(float) * novo['PRECO'].astype(float)
    s += su.sum()
    print(s)


if __name__ == '__main__':
    extrai()
    filter_all()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
