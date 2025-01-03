# Fourier-Font-Expansion

## 使用指南

### Linux

需要事先安装有 Blender 4.2.4 LTS，并配置好 `TextToSpline` 内的相应生成脚本。

```
cd TextToSpline && ./GenerateAlphabets.sh ../Generated Letters && cd ..
python Generator.py --operation generate_letters > shaderCommon.glsl
```

> Windows 操作类似。

## 解释

[Explaination.md (请使用支持行内公式的 Markdown 编辑器打开)](Explaination.md)