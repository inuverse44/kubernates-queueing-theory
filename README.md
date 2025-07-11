# 待ち行列理論 M/M/c モデル分析と可視化

このプロジェクトは、M/M/c待ち行列モデルを分析・可視化するPythonスクリプトを提供し、平均待ち時間と応答時間の計算、および最適なサーバー構成の検索に焦点を当てています。

## ファイル

- `calc.py`:
  - 待ち行列理論の核心計算を実装し、`calculate_average_queue_time`と`find_optimal_pods`を含みます。
  - 直接実行して、指定された95パーセンタイル応答時間のサービスレベル目標（SLO）を満たす最適なポッド（サーバー）数を検索できます。

- `contour.py`:
  - 異なるサーバー数（c）における平均応答時間（W）の運用境界を示す等高線プロットを生成します。
  - 到着率（λ）とサービス率（μ）がシステムの目標応答時間達成能力にどのように影響するかを可視化します。
  - プロットを`w_contour_plot.png`として保存します。

- `plot.py`:
  - 様々なサーバー数（c）における到着率（λ）とサービス率（μ）の関数としての平均待ち時間（Wq）の3D表面プロットを生成します。
  - システムパラメータと待ち行列遅延の関係を可視化するのに役立ちます。
  - プロットを`wq_plot_c_X_refined.png`（Xはサーバー数）として保存します。

## 必要条件

これらのスクリプトを実行するには、以下のPythonパッケージが必要です：

- `numpy`
- `matplotlib`

pipを使用してインストールできます：

```bash
pip install -r requirements.txt
```

## 使用方法

1.  **リポジトリをクローン:**
    ```bash
    git clone <repository_url>
    ```

2.  **依存関係をインストール:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **スクリプトを実行:**

    - SLOのための最適なポッドを検索する場合：
      ```bash
      python calc.py
      ```

    - 応答時間の等高線プロットを生成する場合：
      ```bash
      python contour.py
      ```

    - 3D待ち時間プロットを生成する場合：
      ```bash
      python plot.py
      ```

## 生成されるプロット

- `w_contour_plot.png`: 平均応答時間の運用境界を示す等高線プロット。
- `wq_plot_c_6_refined.png`: 6サーバー用の平均待ち時間の3Dプロット。
- `wq_plot_c_8_refined.png`: 8サーバー用の平均待ち時間の3Dプロット。
- `wq_plot_c_10_refined.png`: 10サーバー用の平均待ち時間の3Dプロット。
