import random
import math
import matplotlib.pyplot as plt
import numpy as np


def questao_1():
    n=1000000
    point_in_circle=0
    estimadores=[]
    erros_relativos=[]
    quantidade_de_pontos=[1, 10, 100, 1000, 10000, 100000, 1000000]

    for i in range(n):
        x=random.random()-0.5
        if (2*pow(x,2) <= 0.25):
            point_in_circle+=1
        #guarda pontos para gerar gráfico do item 4
        if ((i+1) in quantidade_de_pontos):
            if point_in_circle == 0:
                estimadores.append(0)
            else:
                estimadores.append((float(i+1)/point_in_circle))

    root_2=n/(point_in_circle)
    print("valor estimado de raiz de 2")
    print(root_2)
    print("valor real de raiz de 2")
    print(math.sqrt(2))

    for e in estimadores:
        erros_relativos.append((abs(e-math.sqrt(2)))/math.sqrt(2))

    print(erros_relativos)

    #traça gráfico com erros relativos
    plt.plot(range(7), erros_relativos, '-r', label='evolução do erro')
    ###plt.scatter(data[:,1], data[:,2], c=labels, cmap=plt.cm.Spectral)
    plt.show()

def questao_2():
    #gera transformada inversa da funcao a
    def gera_exponencial(lambida):
        u0=random.random()
        #aplica a transformada inversa da funcao exponencial
        #temos como inversa da funcao acumulativa ln(1-u0)/-lambda, porem como 1-u0 também é uma variavel aleatoria entre 0 e 1 uniforme, podemos utilizar apenas u0
        x=math.log(u0)/-lambida
        print(x)

    #gera transformada inversa da funcao b
    def gera_pareto(x0, alpha):
        u0=random.random()
        #aplica a transformada inversa da funcao exponencial
        #temos como inversa da funcao acumulativa x0/pow(1-u0, -alpha), porem como 1-u0 também é uma variavel aleatoria entre 0 e 1 uniforme, podemos utilizar apenas u0
        x=x0/math.pow(u0, -alpha)
        print(x)

def questao_3():
    import string
    import requests

    k=4
    sites=0
    n=10000
    estimadores=[]
    quantidade_de_pontos=[1, 10, 100, 1000, 10000]
    for i in range(n):
        #gera um dominio
        dom=''.join(random.choice(string.ascii_lowercase) for _ in range(k))

        #checa se site existe
        dom_completo="http://www."+str(dom)+".ufrj.br"
        try:
            request = requests.get(dom_completo)
            if request.status_code == 200:
                sites+=1
        except Exception as e:
            pass

        if ((i+1) in quantidade_de_pontos):
            estimadores.append((float(sites)/float(i+1)))

    Mn=float(sites)/float(n)
    print("Mn = "+str(Mn))

    #traça gráfico com Mns
    plt.plot(range(5), estimadores, '-r', label='evolução de Mn')
    plt.show()

def questao_4():
    import numpy as np
    import scipy.stats as st
    import seaborn as sns
    import matplotlib.pyplot as plt


    sns.set()


    def q(x):
        return st.norm.pdf(x, loc=0, scale=1)

    #valor de lambda default eh 1
    def p(x):
        return st.expon.pdf(x)

    def gera_exponencial(lambida):
        u0=random.random()
        #aplica a transformada inversa da funcao exponencial
        #temos como inversa da funcao acumulativa ln(1-u0)/-lambda, porem como 1-u0 também é uma variavel aleatoria entre 0 e 1 uniforme, podemos utilizar apenas u0
        x=math.log(u0)/-lambida
        return(x)

    def rejection_sampling(iter=1000):
        samples = []

        for i in range(iter):
            #valore de lambda defaut eh 1
            z = gera_exponencial(1)

            #como a distribuicao exponencial so gera numeros >0, com 50% de chance estaremos invertendo para o negativo, pois a normal eh simetrica
            if (random.random()>0.5):
                z=-z
            u = np.random.uniform(0, k*p(z))

            if u <= q(z):
                samples.append(z)

        return np.array(samples)


    x = np.arange(-5, 10)
    k = 2

    plt.plot(x, q(x))
    plt.plot(x, k*p(x))
    plt.show()

    s = rejection_sampling(iter=100000)
    sns.distplot(s)


def questao_5():

    N=1000000

    def f(N):
        #distribuicao uniforme
        return 1/N

    def g(x):
        return x*math.log(x)

    def h(x,N):
        K=N*(N+1)/2
        return x/K

    def calc_segundo_momento():
        sum=0
        for i in range(N):
            sum+=(pow(g(i+1), 2)/h(i+1))
        print("segundo momento = "+ str(sum))
        return 1

    def gera_amostra_h(N):
        K=N*(N+1)/2

        #aplicando a transformada inversa , por bhaskara temos:
        u0=random.random()
        x=(-1+math.sqrt(1+4*u0*N*(N+1)))/2
        return x


    def Gn(N):
        sum=0
        for i in range(N):
            sum+=(i+1)*math.log(i+1)
        return sum

    def importance_sampling(n):
        #samples=[]
        S=0
        for i in range(n):
            #sample from h(x)
            x= gera_amostra_h(N)
            #sample=f()*g(x)/h(x)
            S+=f(N)*g(x)/h(x,N)
            #samples.append(sample)
        print("S")
        print(S*N/n)
        print("GN")
        print(Gn(N))
        #return S/(2*n)
        return S/n

    calc_segundo_momento()

    ns=[10, 100, 1000, 10000, 100000, 1000000, 10000000]
    erros_relativos=[]
    for n in ns:
        erros_relativos.append(abs((N*importance_sampling(n))-Gn(N))/Gn(N))

    plt.plot(range(7), erros_relativos, '-r', label='evolucao do erro')
    plt.show()

def questao_6():
    alphas=[1,2,3]
    a=0
    bs=[1,2,4]
    n=1000000
    quantidade_de_pontos=[1, 10, 100, 1000, 10000, 100000, 1000000]

    def f(x, alpha):
        return pow(x, alpha)

    def g(a, b, alpha):
        return (pow(b, alpha+1)-pow(a, alpha+1))/alpha+1


    for alpha in alphas:
        for b in bs:
            point_under_curve=0
            estimadores=[]
            erros_relativos=[]
            for i in range(n):
                x=random.uniform(a,b)
                y=random.uniform(0,pow(b, alpha))
                if (y<=f(x, alpha)):
                    point_under_curve+=1
                #guarda pontos para gerar gráfico do item 4
                if ((i+1) in quantidade_de_pontos):
                    estimadores.append((point_under_curve/float(i+1)))


            Mn=point_under_curve/n
            integral=Mn*(b-a)*(pow(b,alpha))
            print("b = "+str(b)+" alpha = "+str(alpha))
            print("valor estimado da integral")
            print(integral)
            print("valor da integral")
            print(g(a, b, alpha))

            for e in estimadores:
                erros_relativos.append((abs(e-g(a, b, alpha)))/g(a, b, alpha))

            #print(erros_relativos)

            #traça gráfico com erros relativos
            plt.plot(range(7), erros_relativos, '-r', label='evolução do erro')
            plt.show()


def questao_7():
    import time
    import numpy as np
    import random
    import matplotlib.pyplot as plt

    N=[10000, 1000000, 100000000]
    K=[10, 100, 1000, 10000]

    r=1000

    tempos=[]

    inicial=time.time()

    for rodada in range(r):
        for n in N:
            for k in K:
                #inicial=time.time()

                N_elementos = np.arange(0, n)
                validos=n
                tam_subconjunto= int(random.random()*k)
                for e in range(tam_subconjunto):
                    idx=int(random.random()*validos)
                    temp=N_elementos[(validos-1)]
                    N_elementos[(validos-1)]=N_elementos[idx]
                    N_elementos[idx]=temp
                    validos-=1
                samples=N_elementos[(n-k):n]

                #final=time.time()
                #tempos.append(final-inicial)

            #plt.plot(range(k), estimadores, '-r', label='evolução de Mn')
            #plt.show()
    final=time.time()

    tempo=final-inicial
    print(tempo)

#questao_1()
#questao_2()
#questao_3()
#questao_4()
questao_5()
#questao_6()
#questao_7()
