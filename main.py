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
    return s


def definir_compra(valor):
    valor_inicial = valor
    df = pd.read_csv("possui.csv").merge(pd.read_csv("filtrado.csv"))
    cada_um = (teste() + valor) / df.shape[0]
    df["variacao"] = cada_um - df["QTD"] * df["PRECO"]
    dic = {}
    gasto = 0
    for i, value in df.iterrows():
        dic[value["TICKER"]] = {"QTD": value["QTD"], "PRECO": value["PRECO"], "variacao": value["variacao"], "comprado": 0}

    while len(dic) > 0:
        max_key = [key for key in dic.keys() if dic[key]["variacao"] == max([dic[key2]["variacao"] for key2 in dic.keys()])][0]
        maximo = dic[max_key]
        if maximo["PRECO"] < maximo["variacao"] and maximo["PRECO"] < valor:
            maximo["comprado"] += 1
            valor -= maximo['PRECO']
            maximo["variacao"] = cada_um - (maximo["QTD"] + maximo["comprado"]) * maximo["PRECO"]
            gasto += maximo["PRECO"]
        else:
            print(max_key, maximo["comprado"])
            del dic[max_key]
    print(f"Gasto: R${round(gasto,2)} ({round(100 * gasto / valor_inicial, 2)}%)")

if __name__ == '__main__':
    definir_compra(7160)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
