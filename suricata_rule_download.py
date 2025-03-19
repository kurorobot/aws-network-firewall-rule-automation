import boto3
import json

# AWS クライアント作成
session = boto3.Session(profile_name="my-sso-session", region_name="ap-northeast-3")
client = session.client("network-firewall")

# ルールグループ ARN (手動で設定 or list-rule-groups で取得)
rule_group_arn = "arn:aws:network-firewall:ap-northeast-3:my-account-id:stateful-rulegroup/network-firewall-rulegroup-stateful-suricata-prod"

# Network Firewall ルール取得
response = client.describe_rule_group(RuleGroupArn=rule_group_arn)

# ルールを抽出
rule_data = response["RuleGroup"]["RulesSource"].get("RulesString", "")

# 結果を表示
print("=== 現在の Suricata ルール ===")
print(rule_data)
