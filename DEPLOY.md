# 部署说明（GitHub Pages + MkDocs）

本项目已包含用于自动部署 MkDocs 站点到 GitHub Pages 的 GitHub Actions 工作流：`.github/workflows/deploy-mkdocs.yml`。

快速步骤：

1. 确保已将仓库推到 GitHub 的 `main` 分支：

```bash
git add .
git commit -m "Add docs and deploy workflow"
git push origin main
```

2. 工作流触发后会：
- 缓存 pip 依赖以加速构建（使用 `requirements.txt` 的 hash 作为缓存 key）。
- 在 Ubuntu 最新 runner 上安装 Python（默认 3.11，可手动在 Actions 中更改）。
- 安装 `requirements.txt` 中的依赖并运行 `mkdocs build` 生成 `site/`。
- 使用 `peaceiris/actions-gh-pages` 将 `site/` 内容发布到 `gh-pages` 分支（自动创建）。

3. 在 Actions 页面查看构建日志，成功后 Pages 链接通常为：

```
https://<OWNER>.github.io/<REPO>
```

常见排错：
- 若构建失败查看 `Install dependencies` 步骤的日志，可能是依赖版本冲突或网络问题。可在 `requirements.txt` 锁定版本。  
- 若 Pages 未显示，检查 `gh-pages` 分支是否包含 `index.html`。  
- 若需要自定义域（CNAME），在 `docs/` 或 `site/` 下放置 `CNAME` 文件（仅在首次部署前生效）。

可选改进：
- 我可以为工作流添加缓存策略优化、构建并行、或自动把发布链接写入 `README.md`（需要工作流权限写回 `main`）。
