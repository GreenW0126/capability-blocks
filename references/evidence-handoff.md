# Capability Evidence Handoff

本文件定义 Capability Blocks 作为 CV Agent 或其他求职工具上游时的交接合同。用户对话中不展示这些后台字段。

## 双产物合同

### `capability-blocks.md`

这是人类与 Agent 共读的职业能力层，保存：

- 已确认的求职方向建议；
- 按当前目标排序的积木 A/B/C/D；
- 每块的核心能力、适配岗位、可迁移价值和压缩证据链；
- 成立的积木组合。

它不是 CV bullet 集合。下游 Agent 应从它获取内容战略和排序，再从 evidence map 展开经历。

### `evidence-map.json`

这是 Agent 可读的事实与推导层，按 [evidence-map.schema.json](evidence-map.schema.json) 创建。它保存：

- 与职业判断相关的用户原话片段与来源引用；
- 不改变用户原意的规范化事实；
- 每段经历的组织/项目、角色关系、日期范围与元数据完整状态；
- 问题、判断、行动、方法、产出、影响、范围和责任边界；
- 积木到 evidence ID 的映射及简短推导；
- 岗位需求簇与 JD 来源引用；
- 可安全展开的主张及不得越过的边界。

## 记录规则

- 原始语料按“能独立支持一个事实或判断”切分；不存无关闲聊、系统提示或 Agent 措辞。
- `raw_statement` 保留用户原意；`normalized_fact` 只做消歧和结构化，不升级所有权、数字、因果或影响。
- `experiences[]` 中的履历元数据优先继承仍然有效的旧 CV；旧 CV 没有的新经历由用户材料或问答确认。组织/项目、角色关系和日期不得由 Agent 猜测。
- `metadata_status=complete` 仅表示三项履历元数据均有可用值；`partial`、`user_withheld` 或 `not_applicable` 允许运行态继续提炼，但不能把该经历作为 CV handoff 的已就绪证据。
- 用 `information_type` 区分 `fact`、`interpretation` 和 `hypothesis`。只有 `fact` 可直接进入 CV；其他类型只能辅助提问或命名，除非后续被用户确认为事实。
- `ownership` 使用用户证据所支持的最高层级；不明时使用 `unspecified`，不由 Agent 自动升级。
- 一个 evidence unit 可支持多块积木，但每个 mapping 必须说明它在不同能力闭环中支持什么；不能靠复制同一事实制造多块近义积木。
- JD 只能进入 `jd_sources` 和 `demand_clusters`，不能进入 `evidence_units`。

## 事实冲突优先级

1. 用户明确修正；
2. 用户最新确认的陈述；
3. 用户原始陈述；
4. 旧 CV 中的信息；
5. AI 的解释或推断。

JD 不属于候选人事实来源。当高优先级来源覆盖旧值时，更新所有受影响的 mapping，不把冲突旧值保留为可导出事实。

## CV 交付包

下游 CV Agent 的完整输入为：

1. `capability-blocks.md`：决定写什么和如何排序；
2. `evidence-map.json`：决定凭什么写及表达边界；
3. 用户旧 CV 或等价的已确认 profile/timeline：提供姓名、联系方式、机构、职位、日期、教育等履历事实；
4. 当次目标 JD：决定需求优先级、市场语言和篇幅，不创造候选人事实。

下游 Agent 必须：

- 每条实质性 CV 主张能反向定位到 block ID 与至少一个 evidence ID；
- 不把积木卡片机械复制成 CV bullet，而是回到具体经历展开；
- 不把多段经历合并成一个虚构项目；
- 不用 JD 补齐用户没有的技能、所有权或结果；
- 发现材料冲突时按上述优先级处理；仍无法判断时使用范围更安全的表达，或只询问会改变 CV 实质内容的一个问题。

正式交接前运行：

```bash
python scripts/validate_evidence_map.py --handoff .capability-blocks-session/evidence-map.json
```

普通校验只检查结构、引用和事实边界；`--handoff` 额外要求所有被能力积木引用的经历均通过履历元数据质量门。

## 交付验收

- `capability-blocks.md` 中每块积木都在 JSON 中有唯一 mapping；
- 每个实质主张至少连接一个可定位 evidence unit；
- 所有 evidence ID、JD source ID 和 demand-cluster ID 唯一且引用可解析；
- 积木映射不引用 `hypothesis` 作为直接 CV 证据；
- JSON 不重复保存旧 CV 可承载的联系信息；
- 每段被积木引用的经历均有 `organization_or_project`、`role_or_relationship` 和完整 `date_range`，且 `metadata_status=complete`；
- 用户的最新修正已同步进入两份产物；
- 产物运行时间、用户管理型保留策略和保存位置已记录。
