import random
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy import sparse


def cria_P_anel(n):
    P=[]
    pi=np.zeros(n)
    for i in range(n):
        linha=np.zeros(n)
        linha[i-1]=1/4
        linha[i]=1/2
        linha[(i+1)%n]=1/4
        P.append(linha)
        pi[i]=1/n

    return P, pi

def cria_P_arvoreBin(n):
    altura_folha=int(np.ceil(np.log2(n)))
    n=2**altura_folha-1
    altura_inicial=1
    node_i=int(n/2)
    P=[]
    pi=np.zeros(n)
    #constante de normalizacao
    K=2*(n-1)

    def criaLinhaArvore(h, node, pai, avo):
        linha=np.zeros(n)

        #no raiz
        if h==1:
            filho1=int(node/2)
            filho2=node+int(node/2+1)

            linha[node]=1/2
            linha[filho1]=1/4
            linha[filho2]=1/4
            pai=node

            pi[node]=2/K
        #nos folha
        elif h==altura_folha:
            linha[node]=1/2
            linha[pai]=1/2

            pi[node]=1/K

        #restante dos nos
        elif node<pai and node<avo:
            filho1=node-int((pai-node)/2)
            filho2=node+int((pai-node)/2)

            linha[node]=1/2
            linha[pai]=1/6
            linha[filho1]=1/6
            linha[filho2]=1/6

            pi[node]=3/K
            #print("1")
        elif node<pai and node>avo:
            filho1=int(node-((node-avo)/2))
            filho2=node+int((node-avo)/2)
            #print("2")

            linha[node]=1/2
            linha[pai]=1/6
            linha[filho1]=1/6
            linha[filho2]=1/6

            pi[node]=3/K
        else:
            filho1=int(node-((node-pai)/2))
            filho2=node+int((node-pai)/2)
            #print("3")
            #print(node)
            #print(pai)

            linha[node]=1/2
            linha[pai]=1/6
            linha[filho1]=1/6
            linha[filho2]=1/6

            pi[node]=3/K



        if h==altura_folha:
            P.append(linha)
            return 0
        else:
            h+=1
            return criaLinhaArvore(h,filho1, node, pai), P.append(linha), criaLinhaArvore(h,filho2, node, pai)

    criaLinhaArvore(altura_inicial,node_i, 0, 0)

    return P, pi

def cria_P_grid2d(n):
    linha=int(np.ceil(np.sqrt(n)))
    n=linha**2
    P=np.zeros((n,n))
    pi=np.zeros(n)

    for i in range(n):
        coluna = int(i/linha)

        vizinho_esquerda= coluna*linha+(i-1)%linha
        vizinho_direita= coluna*linha+(i+1)%linha
        vizinho_cima=i-linha
        vizinho_baixo=(i+linha)%n

        P[i, i] = 1/2
        P[i, vizinho_esquerda] = 1/8
        P[i, vizinho_direita] = 1/8
        P[i, vizinho_cima] = 1/8
        P[i, vizinho_baixo] = 1/8

        pi[i]= 1/n

    return P, pi

def variacao_total(v1, v2):
    variacao=0
    for i in range(len(v1)):
        variacao+=abs(v1[i]-v2[i])
    return variacao/2

def calcula_tempo_mistura(ns, erro):
    tempos_totais=[]

    for n in ns:
        P1, pi1=cria_P_arvoreBin(n)
        P2, pi2=cria_P_anel(n)
        P3, pi3=cria_P_grid2d(n)

        P=[P1, P2, P3]
        pi=[pi1, pi2, pi3]

        tempos=[]
        for i in range(len(P)):
            #DEBUG

            print("n: ", n)
            print("i: ", i)
            pi_inicial=np.zeros(len(P[i]))
            pi_inicial[0]=1

            t=0
            dvt=1

            #testando com matriz esparsa
            sP=sparse.csr_matrix(P[i])

            while dvt>erro:
                pi_inicial=sparse.csr_matrix(pi_inicial)
                pi_inicial=pi_inicial.dot(sP).toarray()[0]

                dvt=variacao_total(pi[i], pi_inicial)
                t+=1

                #DEBUG
                # if (t%10)==0:
                #     #print(i)
                #     print(P[i])
                #     print(pi_inicial)
                #     print(pi[i])
                #     a=input("test")

            tempos.append(t)

        tempos_totais.append(tempos)

    matriz = np.array(tempos_totais)
    return matriz.transpose()



if __name__ == '__main__':

    ts=[1, 10, 100, 1000, 10000, 100000]
    variacoes_totais=[]
    n = 100
    P1, pi1=cria_P_arvoreBin(n)
    P2, pi2=cria_P_anel(n)
    P3, pi3=cria_P_grid2d(n)

    P=[P1, P2, P3]
    pi=[pi1, pi2, pi3]


    #calculo das variacoes totais referente a questao 3 da lista 4
    for i in range(len(P)):
        vts=[]
        pi_inicial=np.zeros(len(P[i]))
        pi_inicial[0]=1
        for t in range(ts[-1]):
            pi_inicial=pi_inicial.dot(P[i])
            if (t+1) in ts:
                vts.append(variacao_total(pi[i], pi_inicial))
        variacoes_totais.append(vts)


    #print(variacoes_totais)


    plt.xlabel("log t")
    plt.ylabel("log Dvt")
    for variacao in variacoes_totais:
        plt.plot(range(len(ts)), np.log(variacao), label='evolução da Variacao total')
    plt.show()



    # #calculo dos tempos de mistura referentes a questao 4 da lista 4
    ns=[10, 50, 100, 300, 700, 1000]
    erro=0.0001
    tempos_de_mistura = calcula_tempo_mistura(ns, erro)


    plt.xlabel("log n")
    plt.ylabel("log tempo de mistura")
    for tempo in tempos_de_mistura:
        plt.plot(np.log(ns), np.log(tempo), label='evolução do tempo de mistura')
    plt.show()
