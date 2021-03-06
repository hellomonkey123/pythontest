# -*- coding: utf-8 -*-

import sys;
import numpy as np;
import matplotlib.pyplot as plt;

plt.close();




def equilibrium(c_V):
    h = 1. * T / C;
    if (1. / h < max(beta, gamma, vac_max)):
        return -1;
    t_critical = -3;  # randint(0,C);
    thr = 0;
    res_a = np.zeros(C + 1);

    while (t_critical != thr):

        x_S = np.zeros(C + 1);
        x_I = np.zeros(C + 1);
        my_policy = np.zeros(C + 1);
        x_S[0] = S0;
        x_I[0] = I0;
        for i in range(C):
            if i < t_critical:
                myvac = vac_max;
                my_policy[i] = vac_max;
            else:
                myvac = 0;
                my_policy[i] = 0;
            x_S[i + 1] = x_S[i] + (-beta * x_I[i] * x_S[i] - myvac * x_S[i]) * h;
            x_I[i + 1] = x_I[i] + (beta * x_I[i] * x_S[i] - gamma * x_I[i]) * h;

        J_s = np.zeros(C + 1);
        J_i = np.zeros(C + 1);
        J_r = np.zeros(C + 1);
        J_v = np.zeros(C + 1);

        for count in range(C):
            t_ = C - count;
            slope = c_V - J_s[t_];
            if slope < 0:
                res_a[t_] = vac_max;
                p_s_s = 1 - 1. * beta * x_I[t_ - 1] * h - 1. * vac_max * h;
                p_s_i = 1. * beta * x_I[t_ - 1] * h;
                J_s[t_ - 1] = vac_max * c_V * h + p_s_s * J_s[t_] + p_s_i * J_i[t_];
            else:
                res_a[t_] = 0;
                p_s_s = 1 - beta * x_I[t_ - 1] * h - 0 * h;
                p_s_i = beta * x_I[t_ - 1] * h;
                J_s[t_ - 1] = 0 * c_V * h + p_s_s * J_s[t_] + p_s_i * J_i[t_];
            p_i_s = 0;
            p_i_i = 1 - gamma * h;
            J_i[t_ - 1] = c_I * h + p_i_s * J_s[t_] + p_i_i * J_i[t_];
            J_r[t_ - 1] = J_r[t_];
            J_v[t_ - 1] = J_v[t_];

        for i in range(C + 1):
            if J_s[i] < c_V:
                thr = i;
                break;

        if t_critical > thr:
            t_critical = t_critical - 1;
        if t_critical < thr:
            t_critical = t_critical + 1;

    return thr;


# fixed parameters
c_V =np.linspace(0.01, 1.2, 250);    # cost per unit time of vaccination
c_I = 36.5;  # cost per unit time of infection
gamma = 36.5;

# time horizon
T = 1;
h = 0.001;
C = int(1. * T / h);


# parameters to modify
beta = 73;  # infection rate
vac_max = 10;  # maximum vaccination rate

# initial conditions
S0 = 0.75;
I0 = 0.10;

x_S = np.zeros(C + 1);
x_I = np.zeros(C + 1);
my_policy = np.zeros(C + 1);
v = np.zeros(C + 1);

t_eq = np.zeros(250);
t_opt = np.zeros(250);

for s in range(250):
    j = 0;

    for t_critical in range(C + 1):
        x_S[0] = S0;
        x_I[0] = I0;
        for i in range(C):
            if i < t_critical:
                myvac = vac_max;
                my_policy[i] = vac_max;
            else:
                myvac = 0;
                my_policy[i] = 0;
            x_S[i + 1] = x_S[i] + (-beta * x_I[i] * x_S[i] - myvac * x_S[i]) * h;
            x_I[i + 1] = x_I[i] + (beta * x_I[i] * x_S[i] - gamma * x_I[i]) * h;

        v[j] = sum(1. * c_I * x_I * h + 1. * c_V[s] * x_S * my_policy * h);

        j = j + 1;

    mymin = v[0];
    for i in range(1, C + 1):
        if v[i] < mymin:
            mymin = v[i];
            t_opt[s] = i/1000;

    t_eq[s] = equilibrium(c_V[s])/1000;
print ('not correct values of parameters')
plt.plot(c_V, t_eq);
plt.plot(c_V, t_opt);
plt.show()

