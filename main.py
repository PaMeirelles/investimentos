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
    df = df[df["TICKER"].str[4] == '3']

    estatais = read_1d_csv('estatais')
    df = df[~df[['TICKER']].isin(estatais).any(axis=1)]

    df = df[df['PRECO'].astype(int) != 0]
    df = df[df[" LIQUIDEZ MEDIA DIARIA"].astype(float) >= 3000000]
    df.to_csv("filtrado.csv", index=False)


def extrai():
    df = pd.read_csv("filtrado.csv")
    df = df[["TICKER"]].copy()
    df.to_csv("analise.csv", index=False)


def graham():
    df1 = pd.read_csv("filtrado.csv")
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
    print(novo[["QTD", "PRECO"]])
    s += su.sum()
    print(s)


if __name__ == '__main__':
    filter_all()
    extrai()
    graham()
    teste()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
