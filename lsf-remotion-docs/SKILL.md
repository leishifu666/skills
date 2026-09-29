---
name: lsf-remotion-docs
description: "LSF Remotion 文档查询：搜索并读取最新 Remotion API 与官方文档。"
version: 4.0.529
---

# LSF Remotion 文档查询

本技能用于查找并阅读当前版本的 Remotion 文档。若任务与文档查询无关，请改用 `lsf-remotion-best-practices`。

## 搜索文档

使用 Algolia 搜索 API 查找相关文档页面：

```
POST https://plsduol1ca-dsn.algolia.net/1/indexes/*/queries?x-algolia-api-key=3e42dbd4f895fe93ff5cf40d860c4a85&x-algolia-application-id=PLSDUOL1CA
Content-Type: application/x-www-form-urlencoded

{
  "requests": [
    {
      "query": "<your search query>",
      "indexName": "remotion",
      "params": "attributesToRetrieve=[\"hierarchy.lvl0\",\"hierarchy.lvl1\",\"hierarchy.lvl2\",\"url\"]&hitsPerPage=10"
    }
  ]
}
```

每条搜索结果都包含指向文档页面的 `url` 字段。

## 获取 Markdown 格式文档

在任意 Remotion 文档 URL 末尾加上 `.md`，即可获取 Markdown 源文档并减少上下文占用：

```
https://www.remotion.dev/docs/use-video-config.md
https://www.remotion.dev/docs/sequence.md
https://www.remotion.dev/docs/lambda/rendermediaonlambda.md
```

## 查询流程

1. 用 Algolia 搜索所需概念或 API。
2. 从结果中选出最相关的 URL。
3. 在每个 URL 后加上 `.md` 并获取页面内容。
4. 根据当前文档实现功能，不要只凭记忆使用 API。
