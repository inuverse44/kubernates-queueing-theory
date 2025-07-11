import numpy as np
import math

def calculate_lq(rho: float, c: int) -> float:
    """M/M/c待ち行列の平均待ち行列長Lqを計算します。

    Args:
        rho (float): システムの利用率。
        c (int): サービスチャネル（窓口）の数。

    Returns:
        float: 平均待ち行列長Lq。rhoが1以上の場合は無限大を返します。
    """
    if rho >= 1:
        return float('inf')

    # Erlang C formula
    sum_terms = 0.0
    for n in range(c):
        sum_terms += ((c * rho)**n) / math.factorial(n)

    pc_numerator = ((c * rho)**c) / (math.factorial(c) * (1 - rho))
    pc = pc_numerator / (sum_terms + pc_numerator)

    lq = (pc * rho) / (1 - rho)
    return lq

def calculate_wq(lq: float, mu: float) -> float:
    """平均待ち行列長Lqとサービス率muから平均待ち時間Wqを計算します。

    Args:
        lq (float): 平均待ち行列長Lq。
        mu (float): サービス率（1サービスチャネルあたりの平均サービス数）。

    Returns:
        float: 平均待ち時間Wq。
    """
    wq = lq / mu
    return wq

def calculate_l(lq: float, rho: float, c: int) -> float:
    """平均待ち行列長Lq、利用率rho、サービスチャネル数cから平均システム内客数Lを計算します。

    Args:
        lq (float): 平均待ち行列長Lq。
        rho (float): システムの利用率。
        c (int): サービスチャネル（窓口）の数。

    Returns:
        float: 平均システム内客数L。
    """
    l = lq + c * rho
    return l

def calculate_w(wq: float, mu: float) -> float:
    """平均待ち時間Wqとサービス率muから平均システム内時間Wを計算します。

    Args:
        wq (float): 平均待ち時間Wq。
        mu (float): サービス率（1サービスチャネルあたりの平均サービス数）。

    Returns:
        float: 平均システム内時間W。
    """
    w = wq + 1 / mu
    return w

def calculate_rho(lambda_val: float, mu: float, c: int) -> float:
    """到着率lambda、サービス率mu、サービスチャネル数cからシステムの利用率rhoを計算します。

    Args:
        lambda_val (float): 到着率。
        mu (float): サービス率（1サービスチャネルあたりの平均サービス数）。
        c (int): サービスチャネル（窓口）の数。

    Returns:
        float: システムの利用率rho。
    """
    rho = lambda_val / (c * mu)
    return rho

def calculate_lambda(rho: float, mu: float, c: int) -> float:
    """利用率rho、サービス率mu、サービスチャネル数cから到着率lambdaを計算します。

    Args:
        rho (float): システムの利用率。
        mu (float): サービス率（1サービスチャネルあたりの平均サービス数）。
        c (int): サービスチャネル（窓口）の数。

    Returns:
        float: 到着率lambda。
    """
    lambda_val = rho * c * mu
    return lambda_val

def calculate_mu(lambda_val: float, rho: float, c: int) -> float:
    """到着率lambda、利用率rho、サービスチャネル数cからサービス率muを計算します。

    Args:
        lambda_val (float): 到着率。
        rho (float): システムの利用率。
        c (int): サービスチャネル（窓口）の数。

    Returns:
        float: サービス率mu。
    """
    mu = lambda_val / (rho * c)
    return mu