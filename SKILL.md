---
name: laowang-mianshi-zhu
description: 老王工作区面试链考前子 Agent。根据 JD 与简历生成可口述逐字稿，写入 laowang-mianshi-lian 工作册 A 章（考前逐字稿）。与 laowang-mianshi-fu 共用 mianshi-workbook.md，考前考后同一文档。编排入口 laowang-mianshi-lian。不编造经历与数据。
---

# 老王面试逐字稿（laowang-mianshi-zhu）

**子 Agent · 考前半环。** 编排入口：`laowang-mianshi-lian`（可选联动，需另行安装）

简历是纸面逻辑，面试是口述逻辑。本 Skill 把 **JD + 这版简历** 变成你能闭着眼念的稿子，写入共享工作册 **A 章**；面后复盘由 `laowang-mianshi-fu`（可选联动，需另行安装） 写 **B/C 章**，同一文档闭环。


## 独立安装模式（优先于后文工作区联动规则）

本仓库可单独使用，不要求安装 laowang-mianshi-lian。未安装编排层时，先运行本仓库 scripts/bootstrap_workspace.py，使用本 Skill 下 workspace/<season>/mianshi-deck.md 作为总册，按本仓库模板维护章节；不要尝试调用不存在的 lian 脚本。用户已安装编排层并指定共享工作册时，再使用后文 A/B/C 协作模式。其他 Skill 的路径均是可选联动。

## 能力地图

| 模式 | 代号 | 场景 | 产出 |
|------|------|------|------|
| 工作册初始化 | `deck-init` | 第一次用（或交给 lian） | 调用 lian 的 `bootstrap_workbook.py` |
| 单岗写稿 | `jd-transcript` | 新公司/新 JD 要一套稿子 | 写工作册 **A 章** + `sessions/` 草稿 |
| 合并工作册 | `deck-merge` | session 定稿写入 A 章 | 局部 Edit `mianshi-workbook.md` |
| Bullet 深挖 | `bullet-drill` | 只练某一个项目 bullet | `drills/` + 可选写 A3 |
| 面后回写 | `bullet-patch` | 按 fu 的 B4 建议改 A 章 | 只 Edit A 章对应 bullet |
| 考前复习 | `deck-review` | 面试前过 A 章 | 读 A1–A5 |

**不做**：编造项目与数字；通用面试题大全（只写与当前 JD/简历有关的稿）；替代模拟面试对话。

## 数据落点

**共享工作册**（与 fu 共用，由 lian 拥有）：

```text
laowang-mianshi-lian/workspace/2027-fall/
├── mianshi-workbook.md          # 唯一总文档（A/B/C 三章/岗）
├── workbook-index.yaml
├── sessions/                    # zhu 写稿草稿
├── drills/
└── audit/
```

zhu **只 Edit** 各岗 `### A. 考前逐字稿` 节；禁止改 B/C。

## 路由规则

1. 无总册 → `deck-init`
2. 用户给 JD + 简历（或 resume_snapshot_id）→ `jd-transcript`，完成后自动 `deck-merge`
3. 用户说「合并进总册」「追加到面试文档」→ `deck-merge`
4. 用户指定某个项目 bullet 加练 → `bullet-drill`，可选合并进总册对应岗的附录
5. 用户说「明天面字节，帮我过一遍稿子」→ `deck-review`（读 A 章）
6. fu 的 B4 回写建议已确认 → `bullet-patch` 更新 A3/A5

执行前按需读取：

- 总册增量规则：[references/deck-increment-rules.md](references/deck-increment-rules.md)
- 单次稿结构：[references/transcript-schema.md](references/transcript-schema.md)
- 两层追问：[references/follow-up-layers.md](references/follow-up-layers.md)
- 真实边界：[references/truth-boundary.md](references/truth-boundary.md)
- 总册模板：[assets/mianshi-deck-template.md](assets/mianshi-deck-template.md)
- 单次模板：[assets/session-template.md](assets/session-template.md)

## 模式一：deck-init

```bash
python scripts/bootstrap_workspace.py --season 2027-fall
```

从 [mianshi-deck-template.md](assets/mianshi-deck-template.md) 生成空总册，写入 `deck-index.yaml`。

## 模式二：jd-transcript（核心）

### 输入

- JD 全文（必填）
- 简历 Markdown 或 `laowang-jianli` 的 `resume-draft.md`（必填）
- 可选：`laowang-job-fit` 报告、`laowang-toudi-desk` 的 `resume_snapshot_id`

### 流程

1. **拆 JD**：提取 must/core 能力点，每条保留 JD 原文摘录。
2. **映简历**：每个能力点映射到 resume bullet；无证据标 `[无证据，勿硬答]`。
3. **写稿**（按 [transcript-schema.md](references/transcript-schema.md)）：
   - 60–90 秒自我介绍（只含可证据化内容）
   - 每个核心项目的：背景 → 我的动作 → 结果 → 一层追问 → 二层追问 → 兜底句
   - JD 高频题 3–5 道（行为/业务/协作类，附 30 秒与 90 秒两版稿）
   - 可问面试官 3 个问题
4. **存 session**：`sessions/<岗ID>.md`，`岗ID` = `公司拼音-岗位关键词-日期`。
5. **自动 deck-merge**。

### 岗 ID 示例

`alibaba-tongyi-pm-intern-20260919`

## 模式三：deck-merge（增量合并）

把本次 `sessions/*.md` **追加进总册**，不覆盖用户手写备注。

### 合并规则（摘要）

| 情况 | 动作 |
|------|------|
| 全新公司+岗位 | 在总册末尾新增一章，更新 `deck-index.yaml` |
| 同岗 ID 已存在 | **替换**该章正文，旧版移入 `audit/archived-<岗ID>-<date>.md` |
| 跨岗通用句（如自我介绍骨架） | 沉淀到总册顶部「通用口述库」，标注来源岗 |
| 重复问题不同答法 | 保留最新，旧答法进 `audit/` 附注 |

可脚本辅助：

```bash
python scripts/append_to_deck.py \
  --deck workspace/2027-fall/mianshi-deck.md \
  --session workspace/2027-fall/sessions/alibaba-tongyi-pm-intern-20260919.md \
  --index workspace/2027-fall/deck-index.yaml
```

### 总册章节结构

```markdown
# 面试逐字稿总册

## 通用口述库（跨岗复用）
## 岗位目录（自动索引）
## 岗：阿里巴巴-通义实验室-产品实习
### 自我介绍 60–90s
### 项目深挖
### JD 高频题
### 可问面试官
---
## 岗：字节跳动-AI产品实习
...
```

## 模式四：bullet-drill

用户指定：`项目 X / bullet 2`。

输出 90 秒口述稿 + 两层追问 + 兜底；证据不足处标 `[待补数据]`。可 `--append-to-session <岗ID>` 写入该岗 session 的附录。

## 模式五：deck-review

从 `mianshi-deck.md` 按公司抽取：

- 明日面试岗的自我介绍 + Top3 项目稿
- 所有岗共用的「通用口述库」_diff 提醒（避免念错公司名）
- `[无证据]` 与 `[待补数据]` 清单

## 交流原则

- 稿子是要**念出来**的，句子偏短，少书面词。
- 每个数字必须能回指简历；没有就写定性结果或标 `[待补数据]`。
- 合并总册时**只增量/替换章节**，不整文件重写（遵守文件编辑纪律：Read 后局部 Edit）。
- 与 `laowang-toudi-desk` 的 `interview-brief` 分工：toudi-desk 管投递链路口述包；本 Skill 管**跨 JD 可持续迭代的总册**。

## 完成报告

```markdown
## 面试逐字稿报告
- 模式：jd-transcript + deck-merge
- 岗 ID：…
- session 路径：…
- 总册更新：新增/替换章节
- 待补证据：…
- 建议：bullet-drill 哪条 / 模拟面试哪岗
```

## 质量门槛

- [ ] 自我介绍无简历外的新事实
- [ ] 每个 JD 能力点有映射或明确标「无证据」
- [ ] session 已合并进 `mianshi-deck.md`
- [ ] `deck-index.yaml` 与总册目录一致
- [ ] 同岗二次生成时旧版已归档到 `audit/`

## 套件联动

| 上游 | 用途 |
|------|------|
| `laowang-jianli`（可选联动，需另行安装） | 简历与 facts-ledger |
| `laowang-job-fit`（可选联动，需另行安装） | 缺口与面试风险点 |
| `laowang-toudi-desk`（可选联动，需另行安装） | resume_snapshot_id |

| 下游 | 用途 |
|------|------|
| `laowang-mianshi-mo`（可选联动，需另行安装） | 拿 A 章做模拟压测 |
| `laowang-mianshi-fu`（可选联动，需另行安装） | 面后 B/C 章 + 驱动 bullet-patch |
| `laowang-mianshi-lian`（可选联动，需另行安装） | 编排入口 |
