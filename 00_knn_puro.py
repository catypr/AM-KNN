"""
Implementação de Classificador KNN em Python puro(sem numpy)
"""
import math

def distancia_euclidiana(p1, p2):
    """Calcula a distâncioa euclidiana(linha reta) entre dois pontos"""
    dx = p1[0] - p2[0]
    dy = p1[0] - p2[0]
    return math.sqrt(dx**2 + dy**2) #sqrt - função raiz quadrada 

def distancia_manhattan(p1, p2):
    """Calcula a distância manhattan(caminho em grade) entre dois pontos"""
    dx = abs(p1[0] - p2[0])
    dy = abs(p1[1] - p2[1]) #abs - número absoluto(retira negativos)
    return dx + dy 

def knn_classificar(dados_treino, novo_ponto, k=3, metrica="euclidiana"):
    """Classifica um ponto usando KNN e retorna os detalhes da votação"""
    if metrica == "euclidiana":
        funcao_dist == distancia_euclidiana
    elif metrica == "manhattan":
        funcao_dist = distancia_manhattan
    else:
        raise ValueError("Metrica inválida. Use 'euclidiana' ou 'manhattan'. ")

    # 1. Calcula a distância para todas as amostras
    distancias = []
    for amostra in dados_treino:
        ponto_treino = [amostra[0], amostra[1]]
        classe = amostra[2]
        dist = funcao_dist(novo_ponto, ponto_treino)
        distancias.append((dist, classe, ponto_treino))

    # 2. Ordena as distãncias da menor para a maior 
    distancias.sort(key=lambda x:x[0])

    # 3. Filtrar os K vizinhos mais próximos 
    vizinhos = distancias[:k]

    # 4. Contar os votos por maior(moda)
    votos_0 = sum(1 for v in vizinhos if v[1] == 0)
    votos_1 = sum(1 for v in vizinhos if v[1] == 1)

    # 5. Retorna a classe marjoritaria e os detalhes dos vizinhos 
    classe_predita = 1 if votos_1 > votos_0 else 0 
    return classe_predita, vizinhos, votos_0, votos_1

if __name__ == "__main__":
    # Dados históricos de treino : [tempo_indisponibilidade, usuarios_impactados, prioridade]
    dados_treino = [
        [1.0, 1.0, 0],
        [2.0, 2.0, 0],
        [3.0, 2.0, 0],
        [4.0, 3.0, 0],
        [6.0, 5.0, 1],
        [7.0, 6.0, 1],
        [8.0, 7.0, 1],
        [9.0, 7.0, 1],
    ]

    # Novo chamado a ser classificado
    novo_chamado = [7.0, 6.0]
    k_vizinhos = 3

    print("=" * 60)
    print(" TRIAGEM DE CHAMADOS DE SUPORT (KNN PURO)")
    print("=" * 60)
    print(f"Novo chamado sob análise: {novo_chamado}")

    for metrica in ["euclidiana", "manhattam"]:
        predicao, vizinhos, v0, v1 = knn_classificar(
            dados_treino, novo_chamado, k=k_vizinhos, metrica=metrica
        )

        rotulo_predicao = (
            "Prioridade alta(Classe 1)"
            if predicao == 1
            else "Prioridade noraml(Classe 0)"
        )
        unidade = "unidades" if metrica == "euclidiana" else "quarteirões" 

        print(f"--- Metrica: Distância {metrica.capitalize()} (k={k_vizinhos}) ---")
        for i, (dist, classe, ponto) in enumerate(vizinhos, start=1):
            tipo = "Alta (1)" if classe == 1 else "Normal (0)"
            print(
                f"Vizinho {i}: Ponto={ponto} | classe={tipo} | Distância={dist:.4f} {unidade}"
            )

        print(f"Apuração de Votos: {v1} voto(s) para Alta vs {v0} voto(s) para Normal")
        print(f"Resultado Final: {rotulo_predicao}\n")

    print("=" * 60)
    