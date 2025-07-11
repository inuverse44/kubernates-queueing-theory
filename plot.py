import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
from calc import calculate_lq, calculate_wq, calculate_rho

"""M/M/c待ち行列モデルの平均待ち時間（Wq）を3Dプロットで可視化するスクリプト。

このスクリプトは、異なるサービスチャネル数（ポッド数）における到着率（λ）と
サービス率（μ）の組み合わせに対する平均待ち時間（Wq）を計算し、
3D曲面として表示します。これにより、システムの負荷と性能の関係を直感的に理解できます。
"""

def calculate_wq_for_plot(arrival_rate: float, service_rate: float, servers: int) -> float | None:
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

    # システムが不安定な場合
    if rho >= 1.0:
        return np.nan

    try:
        lq = calculate_lq(rho, servers)
        wq = calculate_wq(lq, service_rate)
    except (ValueError, OverflowError):
        return np.nan

    if arrival_rate == 0:
        return 0.0

    return wq

# --- プロットのパラメータ設定 ---

# メッシュの解像度
resolution = 200
# 到着率 (λ) の範囲
lambda_vals = np.linspace(50, 250, resolution)
# サービス率 (μ) の範囲
mu_vals = np.linspace(10, 50, resolution)
# メッシュグリッドの作成
L, M = np.meshgrid(lambda_vals, mu_vals)

# プロットするサーバ（ポッド）数のリスト
server_counts = [6, 8, 10]

# --- プロット生成ループ ---

# 各サーバー数 (c) ごとに3Dプロットを生成
for c in server_counts:
    print(f"Calculating for c = {c}...")
    # 平均待ち時間 Wq を格納する配列を初期化
    Wq_vals = np.zeros_like(L)
    # メッシュグリッドの各点に対して平均待ち時間 Wq を計算
    for i in range(L.shape[0]):
        for j in range(L.shape[1]):
            lambda_val = L[i, j]
            mu_val = M[i, j]
            Wq_vals[i, j] = calculate_wq_for_plot(lambda_val, mu_val, c)

    print(f"Plotting for c = {c}...")
    # 新しい図を作成
    fig = plt.figure(figsize=(12, 8))
    # 3Dプロット用のサブプロットを追加
    ax = fig.add_subplot(111, projection='3d')

    # 3D曲面をプロット (Wqの値を0から1.0にクリップして表示)
    surf = ax.plot_surface(M, L, np.clip(Wq_vals, 0, 1.0), cmap='viridis', edgecolor='none')

    # --- グラフの装飾 (ラベル位置を調整) ---
    # タイトル設定
    ax.set_title(f'Average Queue Time ($W_q$) with $c = {c}$ Pods', fontsize=16, pad=20)
    # X軸ラベル設定 (labelpadでラベルと軸の距離を調整)
    ax.set_xlabel('Service Rate per Pod ($\mu$, req/s)', fontsize=12, labelpad=20)
    # Y軸ラベル設定
    ax.set_ylabel('Arrival Rate ($\lambda$, req/s)', fontsize=12, labelpad=20)
    # Z軸ラベル設定
    ax.set_zlabel('Average Queue Time ($W_q$, seconds)', fontsize=12, labelpad=15)
    
    # 視点の角度を設定
    ax.view_init(elev=30, azim=-45)

    # カラーバーを追加
    fig.colorbar(surf, shrink=0.5, aspect=5, label='$W_q$ (seconds)')
    
    # 理論上の安定限界線 (λ = cμ) をプロット
    stable_mu = np.linspace(mu_vals.min(), mu_vals.max(), resolution)
    stable_lambda = c * stable_mu
    ax.plot(stable_mu, stable_lambda, zs=0, zdir='z', color='r', linestyle='--', linewidth=2, label='Stability Boundary ($\lambda = c\mu$)')
    # 凡例を追加
    ax.legend(loc='upper left')

    # レイアウトの調整
    plt.tight_layout()
    
    # --- ファイルに保存 ---
    # 出力ファイル名
    filename = f'wq_plot_c_{c}_refined.png'
    # プロットを画像ファイルとして保存
    plt.savefig(filename)
    print(f'プロットを {filename} として保存しました.\n')

# 全てのプロットを表示
plt.show()
