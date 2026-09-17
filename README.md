# Career Capability Mapper

把零散、非线性或难以职业化表达的真实经历，转化为可迁移的能力积木，以及能够追溯事实来源的 evidence map。

`career-capability-mapper` 把一段经历压缩为：真实问题 → 个人判断与行动 → 可核验产出 → 可迁移价值

变化的关键不是换几个动词，而是同时完成三件事：

1. **不越界**：参与不能写成独立负责，课堂测试不能写成商业增长。
2. **可迁移**：从行业任务中找出换到新环境后仍能重复解决的问题。
3. **可追溯**：每个实质主张都能回到 `evidence-map.json` 中的原始证据。

当前版本：`0.5.0`

## 这个项目解决什么问题

许多人的经历并不天然符合标准职位名称：跨行业、自由职业、校园项目、个人项目、照护空档或混合型工作都可能包含真实而有价值的职业能力，但用户未必知道该如何命名它们。

本项目将职业分析留给 Agent，让用户只需要讲述真实发生过的事情。Skill 负责：

- 从经历中识别可重复的问题解决模式；
- 对照目标地区和目标岗位的当前 JD，校准能力命名与优先级；
- 在不虚构事实的前提下进行职业语言包装；
- 维护能力主张与原始证据之间的可追溯关系；
- 将人类可读的能力结论与机器可读的证据关系整理为可移植资产。

本项目以完成 `capability-blocks.md` 和 `evidence-map.json` 为完整交付。用户可以自主保存、审阅和修改这两份文件，也可以将其连接到其他职业文档或 CV 生产工具；本 Skill 不依赖或绑定任何特定的下游工具。

## 三个案例

怎么读案例 / How to read

每个案例只有四部分：

- **Persona**：目标市场和背景；
- **Before**：未经分析的原始表达；
- **After**：2–3 个能力积木；
- **Why it changed**：哪些事实支持了变化，哪些边界被保留。

`evidence-map.json` 是给 Agent 或方法研究者看的机器可读层。普通游客不需要阅读它，也能理解案例。

| 案例 | 迁移情境 | 完整案例 |
| --- | --- | --- |
| 林玮 | 国内从业者进入海外市场 | [查看完整 Before & After](examples/01-china-to-global/) |
| 周安 | 海外毕业生回国求职 | [查看完整 Before & After](examples/02-overseas-graduate-to-china/) |
| 陈屿 | 文科／艺术从业者转入 AI | [查看完整 Before & After](examples/03-humanities-to-ai/) |

## 核心设计

### 1. 双产物同步

每次运行维护两份相互对应的产物：

- `capability-blocks.md`：面向用户与其他工具的能力积木、适配方向和组合；
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
7. 完成双产物的一致性校验，使其能够被用户保存或连接到其他工具。

详细规则见 [`SKILL.md`](SKILL.md) 和 [`references/workflow.md`](references/workflow.md)。

## 安装

将仓库克隆到 Codex 的 Skills 目录：

```bash
git clone https://github.com/GreenW0126/career-capability-mapper.git ~/.codex/skills/career-capability-mapper
```

重新打开 Codex 会话后，可直接描述求职方向探索、跨行能力梳理或经历迁移分析需求。Skill 保持默认的自动发现能力，也可以显式使用 `$career-capability-mapper`。

## 连接其他工具

两份文件共同构成一个不绑定具体产品的职业能力接口：

- `capability-blocks.md` 提供用户已经确认的能力名称、适配方向、可迁移价值与必要证据链，适合人类审阅和文本工具读取；
- `evidence-map.json` 提供稳定 ID、原始来源、责任边界、JD 需求簇与主张映射，适合需要验证或重新组织内容的 Agent 使用。

用户可以自行选择后续工具，并将两份文件作为同一组输入一起提供。下游工具应以 evidence map 作为事实边界，不应根据目标文档需要反向创造经历；任何事实修正都应先回写到这组能力资产。

## 运行态与隐私

在可写环境中，运行态默认保存在当前任务的 `.capability-blocks-session/`：

```text
.capability-blocks-session/
├── capability-blocks.md
└── evidence-map.json
```

- evidence map 只保存职业判断所需的信息，不重复收集姓名、联系方式等与能力映射无关的个人信息；
- 流程完成或暂停时保留双产物与运行态资料，文件由用户自行管理；即使用户提出清理需求，Skill 也只说明文件位置，不代替用户删除；
- 真实用户经历、JD 正文和映射不得进入示例、长期记忆或测试数据；
- 平台保存的会话历史不属于本 Skill 能够删除的范围。

完整规则见 [`references/state-and-privacy.md`](references/state-and-privacy.md)。

## Evidence map 校验

检查结构和交叉引用：

```bash
python3 scripts/validate_evidence_map.py .capability-blocks-session/evidence-map.json
```

准备将两份文件连接到需要完整履历元数据的其他工具前，同时检查被引用经历的组织或项目、角色关系和日期范围：

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
career-capability-mapper/
├── README.md
├── LICENSE
├── .gitignore
├── SKILL.md
├── examples/
│   ├── 01-china-to-global/
│   ├── 02-overseas-graduate-to-china/
│   └── 03-humanities-to-ai/
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
- 建立可供其他职业工具读取的可靠能力与证据资产。

## License

本项目采用 [MIT License](LICENSE)。
