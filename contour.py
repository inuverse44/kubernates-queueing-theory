import numpy as np
import matplotlib.pyplot as plt
import math
from calc import calculate_lq, calculate_wq, calculate_rho, calculate_lambda, calculate_mu

"""M/M/c待ち行列モデルの応答時間に関する等高線プロットを生成するスクリプト。

このスクリプトは、異なるサービスチャネル数（ポッド数）における平均応答時間（W）が
特定の目標値（例: 200ミリ秒）を下回る運用境界を視覚化します。
到着率（λ）とサービス率（μ）の組み合わせに対する応答時間を計算し、
等高線図として表示します。
"""

def calculate_average_queue_time(arrival_rate: float, service_rate: float, servers: int) -> float | None:
    """M/M/cモデルにおける平均待ち時間（Wq）を計算します。

    Args:
        arrival_rate (float): 到着率 (λ)。
        service_rate (float): サービス率 (μ)。
        servers (int): サービスチャネル（サーバーまたはポッド）の数 (c)。

    Returns:
        float | None: 平均待ち時間Wq。システムが不安定な場合や計算エラーの場合はNaNを返します。
    """
    if arrival_rate >= servers * service_rate or service_rate <= 0:
        return np.nan

    rho = calculate_rho(arrival_rate, service_rate, servers)
    
    if rho >= 1.0:
        return np.nan

    try:
        # P0 (システムが空である確率) の計算
        r = arrival_rate / service_rate
        sum_term = sum((r**n) / math.factorial(n) for n in range(servers))
        final_term = (r**servers / math.factorial(servers)) * (1 / (1 - rho))
        p0 = 1 / (sum_term + final_term)
    except (ValueError, OverflowError):
        return np.nan

    # 平均待ち行列長 Lq の計算
    lq = ((r**servers * rho) / (math.factorial(servers) * (1 - rho)**2)) * p0

    if arrival_rate == 0:
        return 0.0
    # 平均待ち時間 Wq の計算 (リトルの法則: Wq = Lq / λ)
    wq = lq / arrival_rate

    return wq

# --- プロットのパラメータ設定 ---
# グリッドの解像度
resolution = 200
# 到着率 (λ) の範囲
lambda_vals = np.linspace(1, 300, resolution)
# サービス率 (μ) の範囲
mu_vals = np.linspace(10, 60, resolution)
# メッシュグリッドの作成
L, M = np.meshgrid(lambda_vals, mu_vals)

# 考慮するサーバー（ポッド）の数
server_counts = [6, 8, 10]
# 目標とする平均応答時間 (秒) - 例: 200ミリ秒 = 0.2秒
target_w_s = 0.2

# --- プロットの準備 ---
# スタイルの設定
plt.style.use('seaborn-v0_8-whitegrid')
# 図と軸のオブジェクトを作成
fig, ax = plt.subplots(figsize=(12, 8))
# 各サーバー数に対応するプロットの色
colors = ['#1f77b4', '#ff7f0e', '#2ca02c'] # 青、オレンジ、緑

# --- コンタープロット生成ループ ---
# 各サーバー数 (c) ごとに処理を繰り返す
for i, c in enumerate(server_counts):
    print(f"Calculating for c = {c}...")
    # 応答時間 W = 3*Wq + 1/μ を格納する配列を初期化
    W_vals = np.zeros_like(M)
    # メッシュグリッドの各点に対して応答時間を計算
    for row_idx in range(M.shape[0]):
        for col_idx in range(M.shape[1]):
            mu_val = M[row_idx, col_idx]
            lambda_val = L[row_idx, col_idx]
            
            # 平均待ち時間 Wq を計算
            wq = calculate_average_queue_time(lambda_val, mu_val, c)
            
            if wq is not np.nan:
                # 平均応答時間 W を計算 (W = Wq + 1/μ)。ここでは3*Wqとしているが、これは特定の要件に基づくもの。
                W_vals[row_idx, col_idx] = 3*wq + (1 / mu_val)
            else:
                # 計算不能な場合はNaNを設定
                W_vals[row_idx, col_idx] = np.nan


    # 目標応答時間 (target_w_s) の等高線をプロット
    contour = ax.contour(
        M, L, W_vals,
        levels=[target_w_s],
        colors=[colors[i]],
        linewidths=2.5
    )
    # 凡例表示のためのダミープロット
    ax.plot([], [], color=colors[i], linewidth=2.5, label=f'$c={c}$ pods (Target $W=200$ms)')

    # 理論上の安定限界線 (λ = cμ) もプロット
    stable_mu = np.linspace(mu_vals.min(), mu_vals.max(), 100)
    stable_lambda = c * stable_mu
    ax.plot(
        stable_mu, stable_lambda,
        color=colors[i],
        linestyle='--',
        linewidth=1.5,
        label=f'$c={c}$ pods (Stability Limit $\\lambda=c\\mu$)'
    )


# --- グラフの装飾 ---
# タイトル設定
ax.set_title(r'Operational Boundary for Average Response Time ($W_{95}$) < 200ms', fontsize=16, pad=20)
# X軸ラベル設定
ax.set_xlabel('Service Rate per Pod ($\\mu$, req/s)', fontsize=12)
# Y軸ラベル設定
ax.set_ylabel('Arrival Rate ($\\lambda$, req/s)', fontsize=12)
# 凡例設定
ax.legend(loc='upper left', fontsize=10)
# X軸の表示範囲設定
ax.set_xlim(mu_vals.min(), mu_vals.max())
# Y軸の表示範囲設定
ax.set_ylim(lambda_vals.min(), lambda_vals.max())
# グリッド表示設定
ax.grid(True, which='both', linestyle='--', linewidth=0.5)

# レイアウトの調整
plt.tight_layout()

# --- ファイルに保存 ---
# 出力ファイル名
filename = 'w_contour_plot.png'
# プロットを画像ファイルとして保存
plt.savefig(filename)
print(f'\nプロットを {filename} として保存しました。')

# プロットを表示
plt.show()