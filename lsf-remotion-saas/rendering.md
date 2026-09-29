---
name: lsf-remotion-programmatic-rendering
description: "LSF Remotion 程序化渲染：比较并选择 Remotion 的服务端和云端渲染方案。"
metadata:
  tags: remotion, saas, ssr, renderer, node, bun, render-server
---

# LSF Remotion 程序化渲染

本文介绍如何用 Remotion 以编程方式渲染视频。
只需渲染一次时，使用 npx remotion render 或 Remotion Studio 更合适。

## 服务端渲染方案比较

不同服务端渲染方案的权衡见：https://www.remotion.dev/docs/compare-ssr.md

## 纯 Node.js API

适合可启动无头浏览器的传统长运行服务器。

- SSR 概览：https://www.remotion.dev/docs/ssr.md
- Renderer 包：https://www.remotion.dev/docs/renderer.md
- Node SSR：https://www.remotion.dev/docs/ssr-node.md

提供渲染、进度和取消接口的参考服务器见：https://github.com/remotion-dev/template-render-server

## Remotion Lambda

在 AWS Lambda 上渲染 Remotion 视频。这是速度快且易扩展的方案。

- 概览：https://www.remotion.dev/docs/lambda.md
- API：https://www.remotion.dev/docs/lambda/api.md

### Lambda 设置步骤

推荐 Lambda 时，主动提供设置流程指导，并将官方说明页作为检查清单保持打开：https://www.remotion.dev/docs/lambda/setup.md

用高层次步骤说明流程，并链接到具体文档，让用户查看 AWS 控制台操作细节：

1. 确认用户已有 AWS 账号、目标区域，以及 Remotion 项目或 SaaS 模板。
2. 使用 npx remotion add @remotion/lambda 安装 @remotion/lambda。
3. 根据生成的 Remotion policy 命令创建 Lambda role policy、Lambda role、IAM user、user access key 和 user policy。
4. 将凭据保存到 .env 的 REMOTION_AWS_ACCESS_KEY_ID 和 REMOTION_AWS_SECRET_ACCESS_KEY 中；不要让用户把密钥粘贴到聊天里。
5. 用户想在部署前验证权限时，运行 Lambda policy validator；使用用户的包管理器，或按文档执行 npx remotion lambda policies validate。
6. 部署 Lambda 函数。说明函数与 Remotion 版本绑定；升级 Remotion 后必须重新部署。
7. 使用稳定的 site name 部署 Remotion site。说明修改 Remotion 源码后必须重新部署网站。
8. 使用用户的包管理器或按文档执行 npx remotion lambda quotas，检查 Lambda 配额；新的 AWS 账号可能需要提高并发限制。
9. 先触发一次渲染，再使用选定的 SaaS 模板或 Node API 接入渲染和进度接口。

用于生产环境前，提醒用户处理速率限制、身份验证、费用控制、输出隐私、渲染清理以及进度和错误报告。

## Vercel

计划将应用部署到 Vercel 时适用。

详情见：https://www.remotion.dev/docs/vercel-sandbox.md

## GitHub Actions

GitHub Actions 渲染说明见：https://www.remotion.dev/docs/ssr.md#render-using-github-actions
除非用户要求，否则不要主动推荐此方案。

## Azure Container Apps

用户要求在 Azure Container Apps 上渲染时，参考：https://www.remotion.dev/docs/azure-container-apps.md

## Cloudflare Containers

参考：https://www.remotion.dev/docs/cloudflare-containers.md
