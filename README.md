# Capability Blocks

把零散、非线性或难以职业化表达的真实经历，转化为可迁移的能力积木，以及能够追溯事实来源的 evidence map。

`capability-blocks` 是一个面向 Codex 的求职探索 Skill。它通过支持性的经历访谈、目标市场 JD 调研和证据映射，帮助用户识别自己能稳定解决的问题，并把这些价值翻译成招聘市场能够识别的语言。

当前版本：`0.4.1`

## 这个项目解决什么问题

许多人的经历并不天然符合标准职位名称：跨行业、自由职业、校园项目、个人项目、照护空档或混合型工作都可能包含真实而有价值的职业能力，但用户未必知道该如何命名它们。

本项目将职业分析留给 Agent，让用户只需要讲述真实发生过的事情。Skill 负责：

- 从经历中识别可重复的问题解决模式；
- 对照目标地区和目标岗位的当前 JD，校准能力命名与优先级；
- 在不虚构事实的前提下进行职业语言包装；
- 维护能力主张与原始证据之间的可追溯关系；
- 为后续 CV 共创提供结构化、可校验的交接资产。

它不直接撰写完整 CV，不自动投递，也不替代面试准备。

## 核心设计

### 1. 双产物同步

每次运行维护两份相互对应的产物：

- `capability-blocks.md`：面向用户与下游 Agent 的能力积木、适配方向和组合；
- `evidence-map.json`：保存经历事实、原始语料来源、责任边界、JD 需求簇和能力映射。

用户可见内容保持简洁、肯定和职业化；证据状态、缺口与流程控制字段在后台维护。

### 2. 支持性的迁移访谈

访谈不要求用户先完成职业分析，也不把回忆过程做成审讯：

- 每轮只设置一个主要记忆入口；
- 雇佣关系、数字口径、个人所有权和业务影响等高压问题，同一轮最多一个；
- 明确允许口头反馈、没有形成正式影响和不完整记忆；
- 每轮先确认已经成立的具体价值，再自然展开下一段细节。

### 3. 市场校准而非关键词拼贴

JD 用于识别目标市场反复出现的业务问题、职责和能力语言，不用于替用户创造经历。每块能力积木必须同时得到经历证据和目标岗位需求簇的支持。

### 4. 真实性与职业包装并重

允许重组顺序、合并同一工作链路、补足事实直接支持的对象与目的，并采用更有力量的职业语言；不新增事件、数字、技能、职位、所有权、因果关系或影响程度。

## 工作流

1. 建立目标地区、岗位方向和现实约束的最小快照；
2. 浏览经历全貌，并对高相关经历进行有限深挖；
3. 调研当前目标市场中的代表性 JD；
4. 映射经历证据、JD 需求簇和候选方向；
5. 形成通常 2–4 块互不重叠的能力积木；
6. 通过投递、行业交流、新 JD 或补充经历进行局部校准；
7. 在需要进入 CV 流程时，校验并交接双产物。

详细规则见 [`SKILL.md`](SKILL.md) 和 [`references/workflow.md`](references/workflow.md)。

## 安装

将仓库克隆到 Codex 的 Skills 目录：

```bash
git clone https://github.com/GreenW0126/capability-blocks.git ~/.codex/skills/capability-blocks
```

重新打开 Codex 会话后，可直接描述求职方向探索、跨行能力梳理或经历迁移分析需求。Skill 保持默认的自动发现能力，也可以显式使用 `$capability-blocks`。

## 典型请求

```text
我想转行，但不知道过去的经历能迁移到哪些岗位，帮我先梳理能力积木。
```

```text
我有几段不连续的工作和项目经历，想知道在上海的用户研究岗位里能如何被理解。
```

```text
先不要写简历，请结合这些经历和我带来的 JD，帮我确认可以被市场识别的能力。
```

## 运行态与隐私

在可写环境中，运行态默认保存在当前任务的 `.capability-blocks-session/`：

```text
.capability-blocks-session/
├── capability-blocks.md
└── evidence-map.json
```

- evidence map 只保存职业判断所需的信息，不重复收集可由旧 CV 承载的姓名和联系方式；
- 用户明确结束并要求清理时，Skill 会删除自己创建的运行态资料；
- 真实用户经历、JD 正文和映射不得进入示例、长期记忆或测试数据；
- 平台保存的会话历史不属于本 Skill 能够删除的范围。

完整规则见 [`references/state-and-privacy.md`](references/state-and-privacy.md)。

## Evidence map 校验

检查结构和交叉引用：

```bash
python3 scripts/validate_evidence_map.py .capability-blocks-session/evidence-map.json
```

在交接给 CV 流程前，同时检查被引用经历的组织或项目、角色关系和日期范围：

```bash
python3 scripts/validate_evidence_map.py \
  --handoff .capability-blocks-session/evidence-map.json
```

运行仓库现有的结构验证测试：

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

## 项目结构

```text
capability-blocks/
├── README.md
├── LICENSE
├── .gitignore
├── SKILL.md
├── references/
│   ├── capability-quality.md
│   ├── evidence-handoff.md
│   ├── evidence-map.schema.json
│   ├── state-and-privacy.md
│   ├── workflow-contract.md
│   └── workflow.md
├── scripts/
│   └── validate_evidence_map.py
└── tests/
    └── test_validate_evidence_map.py
```

## 适用边界

适合：

- 岗位方向尚未完全确定；
- 跨行业、跨专业或非线性经历梳理；
- 职场、校园、自由职业或个人项目的能力迁移分析；
- 在写 CV 前建立可靠的经历证据底座。

不适合：

- 自动投递或代替用户进行市场沟通；
- 对每一份 JD 进行机械改写；
- 直接生成完整 CV、求职招呼语或面试答案；
- 用未经用户确认的信息补全经历。

## License

本项目采用 [MIT License](LICENSE)。
