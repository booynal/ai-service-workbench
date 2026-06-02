# AI 赚钱落地工作台

这个目录不是单纯的想法记录，而是一个已经开始落地的最小工作台。

## 先看哪里

1. 总报告：`赚钱方案报告-2026-06-03.md`
2. 服务清单：`服务套餐清单.md`
3. 发渠道文案：`渠道发布文案.md`
4. 首周动作：`首周落地清单.md`
5. 客户需求模板：`client_brief_template.md`
6. 渠道执行矩阵：`渠道执行矩阵-2026-06-03.md`
7. Fiverr Gig 草稿：`Fiverr-Gig-草稿.md`
8. Upwork Profile 与 Proposal 草稿：`Upwork-Profile-和-Proposal-草稿.md`
9. 英文外联模板：`英文外联模板.md`
10. 主动外联候选清单：`主动外联候选清单-2026-06-03.md`
11. 定制英文外联草稿：`定制英文外联草稿-2026-06-03.md`
12. 外联消息生成器：`tools/generate_outreach_message.py`
12. 明日首发执行单：`明日首发执行单-2026-06-03.md`
13. 触达记录模板：`触达记录模板.csv`
14. 现成外联包目录：`outreach_packets/`
15. 外联包索引器：`tools/prepare_outreach_packet.py`

## 已验证可用的本地能力

1. 本机 `codex` 已登录，可非交互执行
2. 本机 `claude` 已登录
3. 已用 `codex exec` 成功生成提案样例

## 已落地的公开入口

1. 公开仓库：`https://github.com/booynal/ai-service-workbench`
2. GitHub Pages 站点：`https://booynal.github.io/ai-service-workbench/`
3. 当前状态：仓库已创建并推送成功，Pages 已创建并已验证可访问
4. GitHub issue 接单入口：`https://github.com/booynal/ai-service-workbench/issues/new/choose`

## 提案生成工具

脚本：

`tools/proposal_lab.sh`

配套的 GitHub issue 导入脚本：

`tools/issue_to_brief.py`

一键流水线脚本：

`tools/issue_to_proposal.sh`

自动回帖脚本：

`tools/issue_to_proposal_and_comment.sh`

批量处理 open leads 脚本：

`tools/process_open_leads.sh`

外部线索发现脚本：

`tools/external_lead_report.sh`

线索报表脚本：

`tools/pipeline_report.py`

本机 lead engine：

`tools/run_lead_engine.sh`

launchd 配置模板：

`launchd/com.booynal.ai-service-workbench.plist`

安装脚本：

`tools/install_lead_engine.sh`

移除脚本：

`tools/remove_lead_engine.sh`

用法：

```bash
./tools/proposal_lab.sh sample_client_brief.md report_assets/sample_proposal.md
```

输入：

1. 一个客户需求文件

输出：

1. 一份可直接发客户的中文提案 Markdown

## GitHub issue 到提案的本地流程

1. 从 GitHub issue 表单拿到正文内容
2. 保存成一个 Markdown 文件
3. 用下面的命令转成本地 brief：

```bash
python3 tools/issue_to_brief.py path/to/issue.md report_assets/imported_brief.md
```

4. 再生成提案：

```bash
./tools/proposal_lab.sh report_assets/imported_brief.md report_assets/imported_proposal.md
```

如果希望从 issue 文本直接一条命令走完整链路：

```bash
./tools/issue_to_proposal.sh path/to/issue.md output_dir
```

如果 issue 已经在 GitHub 仓库里，也可以直接传 issue 编号：

```bash
./tools/issue_to_proposal.sh 123 output_dir
```

也可以传 GitHub issue URL，只要 `gh issue view` 能识别：

```bash
./tools/issue_to_proposal.sh https://github.com/booynal/ai-service-workbench/issues/123 output_dir
```

如果希望生成后直接评论回 issue：

```bash
./tools/issue_to_proposal_and_comment.sh 123 output_dir
```

如果希望批量扫描公开仓库中还没发送 proposal 的 open leads：

```bash
./tools/process_open_leads.sh output_root_dir
```

如果希望搜索 GitHub 公共 issue 作为外部候选线索：

```bash
./tools/external_lead_report.sh "automation script" output_dir
```

如果希望生成当前线索池的 Markdown 报表：

```bash
python3 tools/pipeline_report.py report_assets/live_pipeline_report.md
```

如果希望一次性执行“处理 open leads + 更新报表”：

```bash
./tools/run_lead_engine.sh report_assets/engine_run
```

当前仓库只提供 launchd 配置模板，不自动安装到系统。

如果后续你想自己开启：

```bash
./tools/install_lead_engine.sh
```

如果想移除：

```bash
./tools/remove_lead_engine.sh
```

如果只想演练、不真正加载 launchctl：

```bash
DRY_RUN=1 ./tools/install_lead_engine.sh
DRY_RUN=1 ./tools/remove_lead_engine.sh
```

这条自动回帖链路也已经完成一次真实 GitHub issue 验证：

`issue #2 -> report_assets/live_comment_run/ -> comment back to issue`

自动打标签链路也已完成真实验证：

`issue #3 -> report_assets/live_label_run/ -> comment back + label proposal-sent`

这条一键链路也已经完成了一次真实验证：

`tests/fixtures/sample_issue.md -> report_assets/pipeline_run/issue.md -> report_assets/pipeline_run/brief.md -> report_assets/pipeline_run/proposal.md`

另外已经完成一次真实 GitHub issue 验证：

`https://github.com/booynal/ai-service-workbench/issues/1 -> report_assets/live_issue_run/`

这条链路已经在当前目录跑通过一次真实样例：

`tests/fixtures/sample_issue.md -> report_assets/imported_brief.md -> report_assets/imported_proposal.md`

## 当前已有样例

1. 烟雾验证：`report_assets/codex_smoke.txt`
2. 提案样例：`report_assets/sample_proposal.md`
3. GitHub issue 导入后的 brief：`report_assets/imported_brief.md`
4. GitHub issue 导入后的提案：`report_assets/imported_proposal.md`
5. 一键流水线输出目录：`report_assets/pipeline_run/`
6. 真实 GitHub issue 输出目录：`report_assets/live_issue_run/`
7. 真实自动回帖输出目录：`report_assets/live_comment_run/`
8. 自动打标签输出目录：`report_assets/live_label_run/`
9. 线索报表：`report_assets/live_pipeline_report.md`
10. 公开案例页：`docs/examples.md`
11. 报告型案例：`report_assets/report_service_proposal.md`
12. 工作流型案例：`report_assets/workflow_service_proposal.md`
13. 报价估算页：`docs/quote-estimator.html`

## 推荐你下一步怎么用

1. 先改 `服务套餐清单.md`，把价格改成你愿意报的数
2. 再把 `渠道发布文案.md` 发到你最容易触达的渠道
3. 收到一个真实需求后，复制成一个新的 brief 文件
4. 用 `tools/proposal_lab.sh` 生成提案
5. 按反馈继续迭代模板和报价

## 当前网络环境下的 GitHub 发布说明

在这台机器当前网络条件下，`git remote-https` 直连 `github.com:443` 会超时，单靠系统代理不稳定。  
实际验证可用的方式是给 Git 命令显式带上代理环境变量：

```bash
HTTPS_PROXY=http://127.0.0.1:7890 \
HTTP_PROXY=http://127.0.0.1:7890 \
ALL_PROXY=socks5://127.0.0.1:7890 \
git push origin main
```

本次公开仓库和 Pages 的最终同步就是按这个方式完成的。

## 当前可用的接单入口

如果有人已经到了仓库，可以直接通过 GitHub issue 表单提交需求：

`https://github.com/booynal/ai-service-workbench/issues/new/choose`

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
