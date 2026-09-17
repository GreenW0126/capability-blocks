# Workflow 编排合同

本文件约束维护本 Skill 的生产与测试任务，不向求职用户展示。

## Commission

每个任务开始前写明：

- Task
- Why this task exists
- Required evidence
- Output format
- Acceptance criteria
- Known constraints
- Decision authority
- Stop condition

## Inspect → Reject / Revise / Accept → Update state

- **Inspect**：检查交付物、证据定位、硬约束、用户可见/后台边界和文件保留规则；向 CV Agent 交接时，额外检查所有被积木引用的经历是否具备组织/项目、角色关系和日期范围。
- **Reject**：方向错误、核心证据缺失或存在硬伤；重新 commission，不把错误资产写入 canonical state。
- **Revise**：方向正确且局部可修；指出确切缺口、证据要求和停止条件。
- **Accept**：全部 acceptance criteria 通过且风险已记录。
- **Update state**：每次 verdict 后立即更新台账；只有接受的产物进入 canonical state。

## Risk contract

每个实质决策记录：

| 字段 | 取值 |
|---|---|
| Decision | 决策及替代方案 |
| 影响范围 | low：单文案/测试；medium：单阶段/schema；high：跨阶段、数据生命周期或用户可见行为 |
| 安全回滚 | yes / partial / no，并写恢复点 |
| 重构成本 | low / medium / high |

属于既定范围且可回滚的工作由 master 自主决定。只有超出范围、不可逆外部操作，或缺少无法推断的用户事实时才请求用户；工作流结构、分工、返工轮次和内部阈值不升级给用户。

## 状态维护者职责

状态维护者只维护 commission 台账、检查记录、verdict、revision 与 state update，不代替生产者写内容，不把内部 reject/revise 信息展示给求职用户。流程完成或暂停时保留双产物和运行态台账，不执行自动删除；文件由用户自行管理，也不得将其中的个人资料与 JD 信息复制到长期记忆、案例、评测或其他项目。
