# GitHub Issue 到提案操作流

这条流程解决的是：

1. 外部通过 GitHub issue 提交需求
2. 你把 issue 正文导出或复制到本地
3. 本地快速生成 brief
4. 再用智能体生成一份能发给客户的提案

## 第一步：收需求

公开入口：

`https://github.com/booynal/ai-service-workbench/issues/new/choose`

客户会按表单填写：

1. 服务类型
2. 当前问题
3. 想要的最终输出
4. 现有资料
5. 交付时间
6. 预算范围
7. 不能碰的约束

## 第二步：保存 issue 正文

把 issue 表单正文保存成一个 Markdown 文件，例如：

`tmp_issue.md`

## 第三步：转成本地 brief

```bash
python3 tools/issue_to_brief.py tmp_issue.md report_assets/imported_brief.md
```

结果文件：

`report_assets/imported_brief.md`

## 第四步：生成客户提案

```bash
./tools/proposal_lab.sh report_assets/imported_brief.md report_assets/imported_proposal.md
```

## 更快的方式：一条命令直接走完整链路

```bash
./tools/issue_to_proposal.sh tmp_issue.md output_dir
```

输出目录中会得到：

1. `issue.md`
2. `brief.md`
3. `proposal.md`

这条一键命令已经在当前目录真实跑通过一次：

`tests/fixtures/sample_issue.md -> report_assets/pipeline_run/`

结果文件：

`report_assets/imported_proposal.md`

## 第五步：人工快速检查

重点看 4 个点：

1. 报价是否合理
2. 风险边界是否说清
3. 是否缺少必须补充的信息
4. 话术是否像真人接单，不像 AI 套话

## 这条流程的价值

这意味着现在已经不只是“收一个线索”。

而是：

1. 收需求
2. 结构化需求
3. 快速回方案

这比单纯写个展示页更接近挣钱。
