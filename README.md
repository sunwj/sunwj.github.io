# Wanjie Sun 学术主页

主页仍是 GitHub Pages 可直接托管的静态网页。内容、页面模板和样式已分开；更新内容不需要修改首页的布局代码。Python 3 即可生成页面，无需安装任何包。

## 各 section 在哪里更新

| 内容 | 编辑文件 |
| --- | --- |
| 姓名、职务、照片、单位、联系方式 | `content/profile.html` |
| 招生公告和招生方向 | `content/recruitment.html` |
| News | `content/news.json` |
| Research Interest | `content/research.json` |
| Publications | `content/publications.json` |
| Fundings | `content/fundings.json` |
| Services | `content/services.json` |
| Honors | `content/honors.json` |
| Professional Experiences | `content/experience.json` |
| Education | `content/education.json` |
| section 顺序、标题、添加或移除 section | `content/sections.json` |
| 访问统计 | `content/footer.html` |

导航由 `sections.json` 自动生成，调整顺序或新增 section 时无需单独更新导航。请保留已有 `id`，以便旧的 section 链接继续有效。

## 更新流程

1. 修改相应内容文件。
2. 在项目根目录执行 `python3 scripts/build.py`。
3. 打开 `index.html` 预览。也可以执行 `python3 -m http.server 8000`，访问 `http://localhost:8000`。
4. 将内容文件和生成的 `index.html` 一起提交、推送到 GitHub。现有从分支发布的 GitHub Pages 可继续使用。

`index.html` 是生成文件，请不要直接编辑，下次生成时会覆盖。检查生成结果是否最新：`python3 scripts/build.py --check`。

## 添加列表内容

普通 section 的 `blocks` 按顺序显示。`items` 中每个字符串是一条内容，新增内容只需增加一条字符串，例如 `content/fundings.json`：

```json
{
  "blocks": [
    {
      "items": [
        "🧾2026, 新项目名称, 主持",
        "🧾2025, 国家自然科学基金面上项目, 主持"
      ]
    }
  ]
}
```

段落或小标题可用 `{"html": "<p>介绍文字</p>"}`。字符串支持已有的 HTML 强调和链接，如 `<b>重点</b>`、`<a href='https://example.org'>链接</a>`。JSON 字符串中的双引号需写成 `\"`，链接属性也可以使用单引号以减少转义。最后一项后不能有逗号。

## 添加论文

`content/publications.json` 包含 Preprints、Journals、Conferences 三组，各组 `items` 数组的顺序就是页面显示顺序。复制一条论文记录并修改以下字段：

```json
{
  "title": "New paper title",
  "authors": "Ce Wang, <u>Wanjie Sun*</u>",
  "venue": "Journal name (<b>Abbreviation</b>), 2026.",
  "image": "files/imgs/papers/new-paper.jpg",
  "image_size": {"width": 145},
  "links": [
    {"label": "PDF", "url": "https://example.org/paper.pdf"},
    {"label": "Code", "url": "https://github.com/example/project"}
  ],
  "bibtex": "@article{example,\n  title={New paper title},\n  year={2026}\n}"
}
```

论文配图放入 `files/imgs/papers/`。不需要 Code 链接时删除对应链接对象；没有链接时使用 `"links": []`。没有 BibTeX 时设为 `"bibtex": ""`，按钮会隐藏。BibTeX 使用原生展开控件，不需要维护 ID 或 JavaScript，也不会再出现原页面的重复 ID 问题。

## 添加 section

新建 `content/teaching.json`，结构参照列表例子，然后在 `content/sections.json` 的适当位置插入：

```json
{"id": "Teaching", "title": "Teaching", "file": "teaching.json", "type": "list"}
```

重新生成后，页面和导航都会包含新 section。布局模板在 `templates/index.html`，样式在 `files/css/jemdoc.css`。
