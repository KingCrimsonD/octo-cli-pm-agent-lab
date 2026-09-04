# 07. 安装与发布

## 本模块回答范围

本文件覆盖 npm 安装、go install、GitHub Releases、install.sh、npm 包命名和发布信任模型。

## 关键结论

### 结论 1：npm 安装包名是 `@mininglamp-oss/octo-cli`

README 和 npm README 均给出 npm 安装命令 `npm install -g @mininglamp-oss/octo-cli`。

来源: README.md#L53-L65
来源: npm/README.md#L1-L9
来源: npm/package.json#L1-L7

### 结论 2：npm 包是 Node wrapper，匹配平台二进制来自 optional dependency，不从 GitHub postinstall 下载

npm README 说明主包是 prebuilt Go binary 的 thin Node wrapper；匹配平台 binary 通过 optional dependency，如 `@mininglamp-oss/octo-cli-darwin-arm64`；install 不从 GitHub 下载。

来源: npm/README.md#L19-L25

### 结论 3：go install 安装命令是 `go install github.com/Mininglamp-OSS/octo-cli/cmd/octo-cli@latest`

README 明确给出 go install 命令。

来源: README.md#L66-L70

### 结论 4：GitHub Release archive 命名为 `octo-cli_<version>_<os>_<arch>.tar.gz`

README 给出 archive 命名规则和 curl/tar 安装示例，Windows archive 也是 `.tar.gz`。

来源: README.md#L78-L92

### 结论 5：install.sh 从 GitHub Releases 下载最新版本，校验 checksums.txt 后安装

install.sh 读取 latest release tag，构造 `octo-cli_${VERSION}_${OS}_${ARCH}.tar.gz`，下载 archive 与 checksums.txt，校验 sha256 后安装到 `/usr/local/bin` 或 `$INSTALL_DIR`。

来源: install.sh#L1-L10
来源: install.sh#L27-L45
来源: install.sh#L46-L61
来源: install.sh#L63-L81

### 结论 6：npm 包支持 macOS/Linux/Windows 的 x64/arm64

npm README 列出支持平台为 macOS、Linux、Windows on x64/arm64。

来源: npm/README.md#L19-L25

### 结论 7：npm 发布带 provenance，可用 npm audit signatures 验证

npm README 说明包以 npm `--provenance` 发布，生成 Sigstore attestations，可用 `npm audit signatures` 验证。

来源: npm/README.md#L30-L42

## 边界与不确定点

- Homebrew 在 README 中标为 coming soon，不应回答为当前已可用。

来源: README.md#L72-L76
