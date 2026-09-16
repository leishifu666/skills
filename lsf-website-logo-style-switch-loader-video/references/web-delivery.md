# 通用网页交付

## 母版与交付版

- 生成母版：5.00 秒目标，保留完整创意时间轴。
- 网页交付版：当 5 秒等待感过长时，默认建议约 3.2 秒。
- 优先整体加速，保留轮廓开场、完整材质变换、最终凝聚和片尾纯黑。不要覆盖母版。

参考命令；速度倍率应根据实际母版时长重新计算：

```powershell
ffmpeg -i "loader-master-5s.mp4" -filter:v "setpts=PTS/1.5714286" -an -c:v libx264 -crf 18 -preset slow -movflags +faststart "loader-web-3.2s.mp4"
```

生成后使用 `ffprobe` 核查实际时长、尺寸、帧率、编码和音轨。不能只根据文件名判断时长。

## 通用 React 接入

```tsx
<div className={`loader-overlay ${visible ? "is-visible" : ""}`} aria-hidden="true">
  <video
    className="loader-video"
    autoPlay
    muted
    playsInline
    preload="auto"
    onEnded={finishLoader}
    onError={finishLoader}
  >
    <source src="/loader-web.mp4" type="video/mp4" />
  </video>
</div>
```

```css
.loader-overlay {
  align-items: center;
  background: #000;
  display: flex;
  inset: 0;
  justify-content: center;
  position: fixed;
  z-index: 9999;
}

.loader-video {
  display: block;
  height: 100%;
  object-fit: contain;
  width: 100%;
}
```

`contain` 表示完整显示，不裁切 Logo；非 16:9 屏幕用纯黑自然留边。只有用户明确接受裁切时才考虑 `cover`。

## 行为边界

- 退出加载层依赖视频真实 `onEnded`，并用 `onError` 防止加载失败后永久遮挡页面。
- 可增加一个合理的故障超时作为最后保险，但超时不能代替 `onEnded`。
- 页面主体、导航、贴纸、文案或其他 UI 的后续动画由目标网站决定。本 Skill 不规定它们的内容、层级或顺序。
- 考虑 `prefers-reduced-motion`：可跳过视频或使用短淡入淡出，但不要替用户擅自改变默认品牌体验。

## 验收

- 桌面与移动端都能播放或安全退出。
- 视频没有裁切、拉伸、错误放大或白色留边。
- 慢网、缓存命中、自动播放限制与解码失败都不会永久锁死页面。
- 加载层退出后，页面自己的交互和滚动状态正常。
