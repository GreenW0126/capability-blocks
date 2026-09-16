# 私有状态与数据生命周期

## 用户可见与后台边界

用户可见：当前需要回答的问题、每轮经历提炼与职业包装、方向建议、岗位名称、能力积木、下一次市场动作。

仅后台：阶段名、经历队列、组织/项目、角色关系、日期范围及其完整状态、事实/解释/假设分类、原始职业语料片段、evidence mapping、证据缺口、JD 全文或摘录、匹配分数、置信度、失败标签、版本号和验收记录。后台字段不得原样复制到对话。

## 运行态

若可写文件，使用当前任务工作区内的 `.capability-blocks-session/`；目录必须加入对应忽略规则，不进入版本控制。目录内保存 `current-state.md`、`capability-blocks.md` 和 `evidence-map.json`。若不可写文件，只在当前会话上下文维护等价结构。

```markdown
# Capability Blocks Runtime State
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
- retention: runtime_only
```

运行态尽量保存引用和必要摘要，不复制整份 CV、作品集或 JD。`evidence-map.json` 可保留能支撑职业判断的用户原话片段，以及下游交接所需的组织/项目、角色关系和日期范围；不保留与证据无关的整段对话，不复制可由旧 CV 提供的姓名、联系方式等信息。暂停时不向用户展示这些后台文件，只用自然语言说明下次可从哪里继续。

## 更新规则

- 新事实：记录来源与用户原意；推断必须与事实分开。
- 事实修正：按“用户明确修正 > 用户最新确认 > 用户原始陈述 > 旧 CV > AI 推断”处理冲突，更新所有受影响映射，旧值不作为可恢复历史长期保存。JD 不在事实优先级中。
- 产物同步：积木的主张、证据链、岗位映射或顺序改变时，同步更新 `capability-blocks.md` 和 `evidence-map.json`，不允许存在无对应 evidence ID 的实质性积木主张。
- 目标变化：只失效受影响的 JD 样本、需求簇与能力排序。
- 用户可见输出：不得包含内部否定状态或后台控制词。
- 外部来源：保存链接、访问日期和必要短摘录，不缓存无关正文。

## 明确结束时的销毁协议

确认用户表达的是结束本进程，而不是暂停，然后：

1. 删除本 Skill 创建的运行态目录，包括 `capability-blocks.md`、`evidence-map.json` 与等价状态文档；
2. 删除个人经历摘要、证据映射、能力候选、用户偏好与身份信息的本地副本；
3. 删除 JD 正文、摘录、缓存、需求映射和与本次搜索可关联的样本记录；
4. 不把上述内容复制到长期记忆、案例、评测或其他项目；
5. 检查本 Skill 控制范围内是否仍有运行态文件，仅向用户确认已清理的资料类别，不复述内容。

长期可保留的只有通用 skill 指令、空白 schema、完全合成案例与无法关联到用户或本次 JD 样本的聚合质量结论。

对平台对话历史、用户自行保存的文件或第三方站点数据没有删除权限时，明确说明这些不在本 Skill 控制范围内，并给出用户可自行执行的最短操作；不得虚假承诺全局删除。
