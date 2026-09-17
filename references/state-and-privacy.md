# 私有状态与数据生命周期

## 用户可见与后台边界

用户可见：当前需要回答的问题、每轮经历提炼与职业包装、方向建议、岗位名称、能力积木、下一次市场动作。

仅后台：阶段名、经历队列、组织/项目、角色关系、日期范围及其完整状态、事实/解释/假设分类、原始职业语料片段、evidence mapping、证据缺口、JD 全文或摘录、匹配分数、置信度、失败标签、版本号和验收记录。后台字段不得原样复制到对话。

## 运行态

若可写文件，使用当前任务工作区内的 `.capability-blocks-session/`；目录必须加入对应忽略规则，不进入版本控制。目录内保存 `current-state.md`、`capability-blocks.md` 和 `evidence-map.json`。若不可写文件，只在当前会话上下文维护等价结构。

```markdown
# Career Capability Mapper Runtime State
- run_id: <非身份随机值>
- phase: target | evidence | jd | mapping | blocks | market_loop
- target_ref:
- experience_queue: current / covered / parked
- evidence_refs:
- evidence_map_ref: .capability-blocks-session/evidence-map.json
- jd_source_refs:
- capability_refs:
- capability_blocks_ref: .capability-blocks-session/capability-blocks.md
- last_user_visible_output:
- next_action:
- retention: user_managed
```

运行态尽量保存引用和必要摘要，不复制整份 CV、作品集或 JD。`evidence-map.json` 可保留能支撑职业判断的用户原话片段，以及下游交接所需的组织/项目、角色关系和日期范围；不保留与证据无关的整段对话，不复制可由旧 CV 提供的姓名、联系方式等信息。暂停时不向用户展示这些后台文件，只用自然语言说明下次可从哪里继续。

## 更新规则

- 新事实：记录来源与用户原意；推断必须与事实分开。
- 事实修正：按“用户明确修正 > 用户最新确认 > 用户原始陈述 > 旧 CV > AI 推断”处理冲突，更新所有受影响映射，旧值不作为可恢复历史长期保存。JD 不在事实优先级中。
- 产物同步：积木的主张、证据链、岗位映射或顺序改变时，同步更新 `capability-blocks.md` 和 `evidence-map.json`，不允许存在无对应 evidence ID 的实质性积木主张。
- 目标变化：只失效受影响的 JD 样本、需求簇与能力排序。
- 用户可见输出：不得包含内部否定状态或后台控制词。
- 外部来源：保存链接、访问日期和必要短摘录，不缓存无关正文。

## 文件保留与用户自行管理

- 当前流程完成或暂停时保留 `capability-blocks.md`、`evidence-map.json` 与运行态资料，不自动删除、移动或覆盖。
- 完成时向用户提供两份核心文件并说明 `.capability-blocks-session/` 的位置；文件是否继续保留、复制、归档或删除由用户决定。
- 用户提出清理需求时，只列出本 Skill 创建的文件和目录，并给出用户可以自行执行的最短操作；Agent 不执行删除，也不声称已经替用户清理。
- 不把个人经历、JD 正文、证据映射或身份信息复制到长期记忆、案例、评测或其他项目。通用 Skill 指令、空白 schema 与完全合成的测试结论不属于用户运行态资料。
- 平台对话历史、用户另行保存的副本和第三方站点数据由对应平台或用户管理，本 Skill 不对其删除状态作出承诺。
