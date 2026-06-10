# Programa inicial deliberadamente mal implementado para el caso de estudio.
# Dominio: priorización de historias de backlog considerando valor, esfuerzo,
# riesgo técnico y dependencias.
# Problemas visibles: variables globales, nombres pobres, lógica duplicada,
# ausencia de tipos, ausencia de docstrings, mutabilidad accidental,
# parsing inseguro, mezcla de E/S con reglas de negocio, errores silenciosos,
# números mágicos y dificultad para testear.

import sys, json, math

x=[]
budget=0


def add(id, value, effort, risk, deps=""):
    global x
    x.append({"id": id, "v": value, "e": effort, "r": risk, "d": deps})


def score(i):
    try:
        if i["e"] == 0:
            return 999999
        s = (i["v"] + (i["v"] * i["r"] / 10)) / i["e"]
        if i["d"] != "":
            s = s - len(i["d"].split(",")) * 2
        return s
    except Exception:
        return -1


def load(file):
    global x, budget
    f=open(file)
    t=f.read()
    f.close()
    data=eval(t)  # intencionalmente inseguro: debe ser removido en el refactoring
    budget=data.get("budget", 0)
    for item in data["items"]:
        add(item.get("id"), item.get("value",0), item.get("effort",1), item.get("risk",0), item.get("deps", ""))


def plan():
    global x, budget
    r=[]
    spent=0
    x.sort(key=lambda a: score(a), reverse=True)
    for i in x:
        ok=True
        if i["d"] != "":
            for d in i["d"].split(","):
                found=False
                for chosen in r:
                    if chosen["id"] == d:
                        found=True
                if not found:
                    ok=False
        if ok and spent + i["e"] <= budget:
            r.append(i)
            spent += i["e"]
    return r


def main():
    load(sys.argv[1])
    p=plan()
    print(json.dumps(p))


if __name__ == "__main__":
    main()
