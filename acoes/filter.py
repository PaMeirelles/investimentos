import csv

import pandas as pd


def read_1d_csv(name):
    new_a = []
    with open(name, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            new_a.extend(row)

    return new_a


def filter_all():
    df = pd.read_csv("acoes/Interno/statusinvest-busca-avancada.csv", sep=';', thousands='.', decimal=",")
    estatais = read_1d_csv('acoes/estatais')
    gr = pd.read_csv("acoes/Interno/analise.csv")
    preju = pd.read_csv("acoes/prejuizo")
    ban = pd.read_csv("acoes/ban")

    graham()
    df = df.merge(gr, how="outer")
    df = df.merge(preju, how="outer")
    df = df.merge(ban, how="outer", left_on="TICKER", right_on="BAN")
    df = df[df["TICKER"].str[4] == '3']
    df = df[~df[['TICKER']].isin(estatais).any(axis=1)]
    df = df[df[" LIQUIDEZ MEDIA DIARIA"].astype(float) >= 70000]
    df = df[df["Graham"] < 1]
    df = df[df['CAGR LUCROS 5 ANOS'] >= 30]
    df = df[df["ALL"] == 0]
    df = df[df["BAN"] != df["TICKER"]]

    df.to_csv("acoes/Interno/filtrado.csv", index=False)


def extrai():
    df = pd.read_csv("acoes/Interno/statusinvest-busca-avancada.csv", sep=';', thousands='.', decimal=",")
    df = df[["TICKER"]].copy()
    df.to_csv("acoes/Interno/analise.csv", index=False)


def graham():
    extrai()

    df1 = pd.read_csv("acoes/Interno/statusinvest-busca-avancada.csv", sep=';', thousands='.', decimal=",")
    df2 = pd.read_csv("acoes/Interno/analise.csv")

    df2["Graham"] = df1["PRECO"] / (df1[" VPA"].astype(float) * df1[" LPA"].astype(float) * 22.5) ** 0.5

    df2.sort_values(by="Graham", inplace=True)
    df2.dropna(inplace=True)
    df2.to_csv("acoes/Interno/analise.csv", index=False)
