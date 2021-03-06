
# Optimal Control Applied to Biological Models. S. Lenhart, J. Workman.

import matplotlib.pyplot as plt
import numpy as np

def g(x, u):
    return k * x * (m - x) - x - u * x

def lambda_function(lambda_, x):
    u = (p_1 * x - lambda_ * x - c) * ((2 * p_2 * x ** 2) ** (-1))
    l = - (u * (p_1 - lambda_ - 2 * p_2 * u * x) + k * lambda_ * (m - 2 * x))
    return l

def runge_kutta_forward(g, u, x_0, h, n_max):
    sol = np.zeros(n_max)
    sol[0] = x_0

    for j in np.arange(n_max - 1):
        x_j = sol[j]
        u_j = u[j]
        u_jp1 = u[j + 1]
        u_mj = 0.5 * (u_j + u_jp1)

        k_1 = g(x_j , u_j)
        k_2 = g(x_j + 0.5 * h * k_1, u_mj)
        k_3 = g(x_j + 0.5 * h * k_2, u_mj)
        k_4 = g(x_j + h * k_3, u_jp1)

        sol[j + 1] = x_j + (h / 6.0) * (k_1 + 2 * k_2 + 2 * k_3 + k_4)

    return sol


def runge_kutta_backward(lambda_function, x, lambda_final, h, n_max):
    sol = np.zeros(n_max)
    sol[-1] = lambda_final

    for j in np.arange(n_max -1, 0, -1):
        lambda_j = sol[j]
        x_j = x[j]
        x_jm1 = x[j - 1]
        x_mj = 0.5 * (x_j + x_jm1)

        k_1 = lambda_function(lambda_j, x_j)
        k_2 = lambda_function(lambda_j - 0.5 * h * k_1, x_mj)
        k_3 = lambda_function(lambda_j - 0.5 * h * k_2, x_mj)
        k_4 = lambda_function(lambda_j - h * k_3, x_jm1)

        sol[j - 1] = lambda_j - (h / 6.0) * (k_1 + 2 * k_2 + 2 * k_3 + k_4)

    return sol


def forward_backward_sweep(g, lambda_function, u, x_0, lambda_final, h, n_max):
    flag = True
    cont = 1
    x = np.zeros(n_max)
    lambda_ = np.zeros(n_max)

    while (flag):
        u_old = u
        x_old = x
        x = runge_kutta_forward(g, u, x_0, h, n_max)
        lambda_old = lambda_
        lambda_ = runge_kutta_backward(lambda_function, x, lambda_final, h, n_max)

        u_1 = (- lambda_ * x + p_1 * x - c) * ((2 * p_2 * x ** 2) ** (-1))
        u = 0.5 * (u_1 + u_old)
        test_1 = np.linalg.norm(u_old - u, 1) * (np.linalg.norm(u, 1) ** (-1))
        test_2 = np.linalg.norm(x_old - x, 1) * (np.linalg.norm(x, 1) ** (-1))
        test_3 = np.linalg.norm(lambda_old - lambda_, 1) * (np.linalg.norm(lambda_, 1) ** (-1))

        test = np.max([test_1, test_2, test_3])

        flag = (test > eps)
        cont = cont + 1
        print cont, test
    return [x, lambda_, u]


t_0 = 0
t_f = 5
n_max = 5000

t = np.linspace(t_0, t_f, n_max)
h = t[1] - t[0]

x_0 = 0.5
k = 0.25
m = 1
p_1 = 2
p_2 = 1
c = 1
lambda_final = 0


u = np.zeros(n_max)
eps = 0.001

x_uncontrol = runge_kutta_forward(g, u, x_0, h, n_max)

[x, lambda_, u] = forward_backward_sweep(g, lambda_function, u, x_0, lambda_final, h, n_max)

plt.plot(t, x, '-', ms=3, lw=1, alpha=0.7, mfc='blue', label = 'Controlled solution')
#plt.plot(t, x_uncontrol, '--', ms=3, lw=1, alpha=0.7, mfc='red', label = 'Uncontrolled solution')
plt.xlabel('Time')
plt.ylabel('Fish population')
#plt.subplot(3, 1, 1)
#plt.plot(t, x)
#plt.ylabel('State')

#plt.subplot(3, 1, 2)
#plt.plot(t, lambda_)
#plt.ylabel('Adjoint')

#plt.subplot(3, 1, 3)
#plt.plot(t, u)
#plt.ylabel('Control')
#plt.xlabel('Time')

plt.legend(loc=0)
plt.show()