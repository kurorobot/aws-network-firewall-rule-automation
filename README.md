# AWS Network Firewall 最小構成サンプル

このリポジトリは、AWS Network Firewall を最小構成で構築するための Terraform コードと、Python によるルール管理スクリプトを提供します。

## 構成内容

- Network Firewall とその必要最小限の構成要素（VPC、サブネット等）
- Network Firewall ルールグループ (Suricata ルールベース)
- Python によるルール管理ツール

## 前提条件

- Terraform v1.0.0 以上
- AWS CLI
- Python 3.6 以上
- boto3

## デプロイ方法

1. リポジトリをクローン

```
git clone https://github.com/your-username/ccoe-network-firewall.git
cd ccoe-network-firewall
```

2. Terraform を初期化

```
terraform init
```

3. 計画を確認

```
terraform plan
```

4. リソースをデプロイ

```
terraform apply
```

## Suricata ルールファイル

- `suricata-prod.rules`: 本番環境用ルール
- `suricata-nonprod.rules`: 非本番環境用ルール

## Python によるルール管理

以下の Python スクリプトを使用して、Suricata ルールの管理が可能です：

### 1. ルールのダウンロード

```
python suricata_rule_download.py
```

既存の Network Firewall ルールグループからルール定義をダウンロードします。
AWS 認証情報を適切に設定してください。

### 2. ルールの管理

```
python suricata_rule_manager.py
```

このツールを使用して以下の操作が可能です：

- ルールの一覧表示
- 新規ルールの追加
- 既存ルールの削除
- ルールの更新

## リソースのクリーンアップ

```
terraform destroy
```

## 注意事項

- このサンプルは最小構成であり、実際の本番環境では追加のセキュリティ設定が必要です
- Network Firewall は使用料金が発生します（料金詳細は[AWS 公式ページ](https://aws.amazon.com/network-firewall/pricing/)を参照）
