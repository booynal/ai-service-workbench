# AI 赚钱落地工作台

这个目录不是单纯的想法记录，而是一个已经开始落地的最小工作台。

## 先看哪里

1. 总报告：`赚钱方案报告-2026-06-03.md`
2. 服务清单：`服务套餐清单.md`
3. 发渠道文案：`渠道发布文案.md`
4. 首周动作：`首周落地清单.md`
5. 客户需求模板：`client_brief_template.md`

## 已验证可用的本地能力

1. 本机 `codex` 已登录，可非交互执行
2. 本机 `claude` 已登录
3. 已用 `codex exec` 成功生成提案样例

## 已落地的公开入口

1. 公开仓库：`https://github.com/booynal/ai-service-workbench`
2. GitHub Pages 站点：`https://booynal.github.io/ai-service-workbench/`
3. 当前状态：仓库已创建并推送成功，Pages 已创建并已验证可访问

## 提案生成工具

脚本：

`tools/proposal_lab.sh`

用法：

```bash
./tools/proposal_lab.sh sample_client_brief.md report_assets/sample_proposal.md
```

输入：

1. 一个客户需求文件

输出：

1. 一份可直接发客户的中文提案 Markdown

## 当前已有样例

1. 烟雾验证：`report_assets/codex_smoke.txt`
2. 提案样例：`report_assets/sample_proposal.md`

## 推荐你下一步怎么用

1. 先改 `服务套餐清单.md`，把价格改成你愿意报的数
2. 再把 `渠道发布文案.md` 发到你最容易触达的渠道
3. 收到一个真实需求后，复制成一个新的 brief 文件
4. 用 `tools/proposal_lab.sh` 生成提案
5. 按反馈继续迭代模板和报价

## 当前最值得优先卖的服务

1. 自动化脚本代做
2. 会议纪要 / 文档整理成报告
3. AI 工作流搭建

## 还缺但不是必须的东西

1. 你的真实案例
2. 你的收款方式
3. 你的主渠道
4. 你的目标客户画像

这些补上以后，工作台可以继续扩成：

1. 多行业提案模板
2. 自动报价器
3. 作品集页面
4. 标准交付 SOP
