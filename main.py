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
    df = pd.read_csv("acoes/Interno/statusinvest-busca-avancada.csv", sep=';', thousands='.', decimal=",")
    estatais = read_1d_csv('acoes/estatais')
    gr = pd.read_csv("acoes/Interno/analise.csv")
    preju = pd.read_csv("acoes/prejuizo")
    ban = pd.read_csv("acoes/ban")

    print(df.shape)
    df.dropna(inplace=True, subset=['TICKER', 'PRECO', ' LIQUIDEZ MEDIA DIARIA', 'CAGR LUCROS 5 ANOS'])
    graham()
    df = df.merge(gr, how="outer")
    df = df.merge(preju, how="outer")
    df = df.merge(ban, how="outer", left_on="TICKER", right_on="BAN")
    print(df.shape)
    df = df[df["TICKER"].str[4] == '3']
    print(df.shape)
    df = df[~df[['TICKER']].isin(estatais).any(axis=1)]
    print(df.shape)
    df = df[df[" LIQUIDEZ MEDIA DIARIA"].astype(float) >= 700000]
    print(df.shape)
    df = df[df["Graham"] < 1]
    print(df.shape)

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


def total_investido():
    s = 0
    tudo = pd.read_csv("acoes/Interno/statusinvest-busca-avancada.csv", sep=';', thousands='.', decimal=",")
    tenho = pd.read_csv("acoes/possui.csv")
    novo = tudo.merge(tenho)
    su = novo['QTD'].astype(float) * novo['PRECO'].astype(float)
    s += su.sum()
    return s


def definir_compra(valor, completar=False):
    df = pd.read_csv("acoes/possui.csv").merge(pd.read_csv("acoes/Interno/filtrado.csv"))
    if completar:
        valor = valor - total_investido()
    valor_inicial = valor
    cada_um = (total_investido() + valor) / df.shape[0]
    df["variacao"] = cada_um - df["QTD"] * df["PRECO"]
    dic = {}
    gasto = 0
    for i, value in df.iterrows():
        dic[value["TICKER"]] = {"QTD": value["QTD"], "PRECO": value["PRECO"], "variacao": value["variacao"], "comprado": 0}

    while len(dic) > 0:
        max_key = [key for key in dic.keys() if dic[key]["variacao"] == max([dic[key2]["variacao"] for key2 in dic.keys()])][0]
        maximo = dic[max_key]
        if abs(maximo["variacao"] + maximo["PRECO"]) < abs(maximo["variacao"]) and maximo["PRECO"] < valor:
            maximo["comprado"] += 1
            valor -= maximo['PRECO']
            maximo["variacao"] = cada_um - (maximo["QTD"] + maximo["comprado"]) * maximo["PRECO"]
            gasto += maximo["PRECO"]
        else:
            print(max_key, maximo["comprado"])
            del dic[max_key]
    print(f"Gasto: R${round(gasto,2)} ({round(100 * gasto / valor_inicial, 2)}%)")


if __name__ == '__main__':
    filter_all()
    definir_compra(50)
