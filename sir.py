import matplotlib.pyplot as plt
# 支持中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def fa(N, a, b, beta):
    fa = -beta * a * b
    return fa


# Infected equation
def fb(N, a, b, beta, gamma):
    fb = beta * a * b - gamma * b
    return fb


# Recovered/deceased equation
def fc(N, b, gamma):
    fc = gamma * b
    return fc


def rK4(N, a, b, c, fa, fb, fc, beta, gamma, hs):
    a1 = fa(N, a, b, beta) * hs
    b1 = fb(N, a, b, beta, gamma) * hs
    c1 = fc(N, b, gamma) * hs
    ak = a + a1 * 0.5
    bk = b + b1 * 0.5
    ck = c + c1 * 0.5
    a2 = fa(N, ak, bk, beta) * hs
    b2 = fb(N, ak, bk, beta, gamma) * hs
    c2 = fc(N, bk, gamma) * hs
    ak = a + a2 * 0.5
    bk = b + b2 * 0.5
    ck = c + c2 * 0.5
    a3 = fa(N, ak, bk, beta) * hs
    b3 = fb(N, ak, bk, beta, gamma) * hs
    c3 = fc(N, bk, gamma) * hs
    ak = a + a3
    bk = b + b3
    ck = c + c3
    a4 = fa(N, ak, bk, beta) * hs
    b4 = fb(N, ak, bk, beta, gamma) * hs
    c4 = fc(N, bk, gamma) * hs
    a = a + (a1 + 2 * (a2 + a3) + a4) / 6
    b = b + (b1 + 2 * (b2 + b3) + b4) / 6
    c = c + (c1 + 2 * (c2 + c3) + c4) / 6
    return a, b, c


def SIR(N, b0, beta, gamma, hs):
    # Initial condition
    a = float(N - 1) / N - b0
    b = float(1) / N + b0
    c = 0.

    sus, inf, rec = [], [], []
    for i in range(10000):
        sus.append(a)
        inf.append(b)
        rec.append(c)
        a, b, c = rK4(N, a, b, c, fa, fb, fc, beta, gamma, hs)

    return sus, inf, rec


if __name__ == '__main__':
    # Parameters of the model

    N = 51635256
    b0 = 0
    beta = 1
    gamma = 0.21
    hs = 0.11
    sus, inf, rec = SIR(N, b0, beta, gamma, hs)
    f = plt.figure(figsize=(8, 5))
    plt.plot(sus, 'b-', label='易感染人群')
    plt.plot(inf, 'r-', label='感染者')
    plt.plot(rec, 'c-', label='治愈/死亡')
    plt.title("SIR 模型")
    plt.xlabel("时间", fontsize=10)
    plt.ylabel("人口数量", fontsize=10)
    plt.legend(loc='lower right')
    plt.xlim(0, 1000)
    plt.savefig('SIR.png')
    plt.show()
