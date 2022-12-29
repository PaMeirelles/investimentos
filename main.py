import pandas as pd

from acoes.filter import filter_all


def total_investido(produto):
    s = 0
    if produto == 'a':
        p = 'acoes'
    elif produto == 'f':
        p = 'FIIs'
    else:
        print("Produto inválido")
        return
    tudo = pd.read_csv(f"{p}/Interno/statusinvest-busca-avancada.csv", sep=';', thousands='.', decimal=",")
    tenho = pd.read_csv(f"{p}/possui.csv")
    novo = tudo.merge(tenho)
    su = novo['QTD'].astype(float) * novo['PRECO'].astype(float)
    s += su.sum()
    return s


def definir_compra(valor, produto, completar=False):
    if produto == 'a':
        df = pd.read_csv("acoes/possui.csv").merge(pd.read_csv("acoes/Interno/filtrado.csv"))
    elif produto == 'f':
        df = pd.read_csv("FIIs/possui.csv").merge(pd.read_csv("FIIs/Interno/statusinvest-busca-avancada.csv", sep=';', thousands='.', decimal=","))
    else:
        print("Produto inválido")
        return
    if completar:
        valor = valor - total_investido(produto)
    valor_inicial = valor
    cada_um = (total_investido(produto) + valor) / df.shape[0]
    df["variacao"] = cada_um - df["QTD"] * df["PRECO"]
    dic = {}
    gasto = 0
    for i, value in df.iterrows():
        dic[value["TICKER"]] = {"QTD": value["QTD"], "PRECO": value["PRECO"], "variacao": value["variacao"], "comprado": 0}
    while len(dic) > 0:
        max_key = [key for key in dic.keys() if dic[key]["variacao"] == max([dic[key2]["variacao"] for key2 in dic.keys()])][0]
        maximo = dic[max_key]
        if abs(maximo["variacao"] - maximo["PRECO"]) < abs(maximo["variacao"]) and maximo["PRECO"] < valor:
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
    definir_compra(5000, 'f', False)
