#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <brief-file> <output-file>"
  exit 1
fi

brief_file="$1"
output_file="$2"

if [ ! -f "$brief_file" ]; then
  echo "Brief file not found: $brief_file" >&2
  exit 1
fi

mkdir -p "$(dirname "$output_file")"

prompt_file="$(mktemp)"
trap 'rm -f "$prompt_file"' EXIT

cat >"$prompt_file" <<'EOF'
你现在是一个接单顾问，目标是根据客户需求，生成一份可以直接发给客户的中文提案。

输出要求：

1. 只输出 Markdown。
2. 不要寒暄，不要解释你是谁。
3. 结构固定为：
   - 标题
   - 我对需求的理解
   - 建议交付内容
   - 实施步骤
   - 时间预估
   - 报价建议
   - 风险与边界
   - 发给客户的话术
4. 报价建议必须分成 3 档：基础版、标准版、加急版。
5. 风格务实、专业、简洁，像真实接单者写的，不像 AI 套话。
6. 如果客户需求存在信息缺口，要明确列出缺什么，但仍然给出可执行的初版方案。

下面是客户原始需求：
EOF

{
  cat "$prompt_file"
  printf '\n\n'
  cat "$brief_file"
} | codex exec \
  --skip-git-repo-check \
  --dangerously-bypass-approvals-and-sandbox \
  -o "$output_file" \
  -

echo "Wrote proposal to $output_file"
