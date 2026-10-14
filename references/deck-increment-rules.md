# 总册增量合并规则（mianshi-deck.md）

## 原则

1. **一本总册，多岗共存** — 秋招一季只维护一个 `mianshi-deck.md`。
2. **按岗分章** — 每家公司+岗位独立章节，用 `## 岗：{公司}-{岗位}` 分隔。
3. **同岗更新不叠床架屋** — 同 `deck_entry_id` 再次生成 → 替换该章，旧章进 `audit/archived-*.md`。
4. **跨岗沉淀** — 自我介绍骨架、通用行为题答法，提取到 `## 通用口述库`，注明 `来源岗：xxx`。
5. **局部 Edit** — 合并时只改对应章节和目录索引，禁止 Write 覆盖整本总册。

## deck-index.yaml

```yaml
season: 2027-fall
entries:
  - id: alibaba-tongyi-pm-intern-20260919
    company: 阿里巴巴
    role: 通义实验室 产品实习
    session_file: sessions/alibaba-tongyi-pm-intern-20260919.md
    updated_at: 2026-09-19
    status: active   # active | archived
```

## 合并流程（Agent 或脚本）

1. Read `mianshi-deck.md` + 新 `session` 全文
2. 查 `deck-index.yaml` 是否已有同 `id`
3. **新岗**：在 `## 岗位目录` 加一行链接；在文件末尾追加新章
4. **旧岗更新**：定位 `## 岗：…` 章节边界，StrReplace 整章；写 audit 归档
5. 扫描 session 中可复用段落 → 提议是否写入「通用口述库」（不自动覆盖通用库，需用户确认或显式指令）
6. 写 `audit/deck-merge-<date>.md` 变更摘要

## 岗位目录（总册内自动维护）

```markdown
## 岗位目录

| 公司 | 岗位 | 更新日 | 章节 |
|------|------|--------|------|
| 阿里巴巴 | 通义产品实习 | 2026-09-19 | [跳转](#岗阿里巴巴-通义实验室-产品实习) |
```

## 与多次 JD 迭代

用户第 2 次投同公司不同业务线 → **新 deck_entry_id**（岗位关键词不同即新章）。

用户同 JD 改了一版简历 → 同 id **替换**章节，audit 留旧版对比。
