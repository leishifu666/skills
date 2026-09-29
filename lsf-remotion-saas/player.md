---
name: lsf-remotion-player
description: "LSF Remotion Player：将 Remotion 预览嵌入 React 应用。"
metadata:
  tags: remotion, player, preview, react
---

# LSF Remotion Player

用户需要在 React 中交互式预览时，使用 @remotion/player。

```tsx
import {Player} from '@remotion/player';
import {MyVideo} from './remotion/MyVideo';

export const App: React.FC = () => {
  return (
    <Player
      component={MyVideo}
      durationInFrames={120}
      compositionWidth={1920}
      compositionHeight={1080}
      fps={30}
      controls
    />
  );
};
```

如果元数据是动态的，请手动同步 Player 属性，或复用合成的 calculateMetadata() 逻辑。
相关说明：https://www.remotion.dev/docs/dynamic-metadata.md#with-the-player

Player 的完整 API：https://www.remotion.dev/docs/player/player.md

如果 SaaS 应用还要生成输出文件，请把 Player 预览与 [framework.md](framework.md) 或 [rendering.md](rendering.md) 中的方案结合使用。
