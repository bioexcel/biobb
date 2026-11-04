# biobb plugin for Claude Code

[Claude Code](https://code.claude.com) skills for working on the BioExcel Building Blocks:

| Skill | Use it to |
|---|---|
| `add-biobb-block` | Add a building block to a biobb package: module and docstring, `conf.yml`, unit test, registration, and the generated JSON schemas, configs, `command_line.md` and adapters |
| `release-biobb-version` | Release a new version of a biobb package: version bump in every file, changelog, tag, PyPI and the Bioconda recipe PR |

The plugin is published by the `bioexcel` marketplace of this repository (`.claude-plugin/marketplace.json`).

## Install

Install it once for your user, so the skills work in any folder: this repository, one of its
`biobb/biobb_*` submodules, or a standalone clone of a biobb package.

```bash
claude plugin marketplace add bioexcel/biobb
claude plugin install biobb@bioexcel
```

Inside a Claude Code session, the same is `/plugin marketplace add bioexcel/biobb` and
`/plugin install biobb@bioexcel`.

## Use

Ask in plain words ("add a pdb_fixer block to biobb_pdb_tools", "release biobb_io") and Claude
loads the right skill, or call it directly:

```
/biobb:add-biobb-block
/biobb:release-biobb-version
```

The release skill publishes (git tags, PyPI, Bioconda PRs): it shows the full diff and asks before
every outward step, and it never types PyPI or GitHub credentials for you.

## Update

The plugin version is the commit of this repository, so every change pushed to `master` is a new
version. Get it with:

```bash
claude plugin marketplace update bioexcel
claude plugin update biobb@bioexcel
```

or turn on auto-update in `/plugin` > Marketplaces > bioexcel. A running session keeps the version
it started with until `/reload-plugins` or a restart.

## Edit the skills

The skills are `skills/<name>/SKILL.md` in this folder. To use your own clone while you edit them,
register it as the marketplace instead of GitHub (only one marketplace can be called `bioexcel`):

```bash
claude plugin marketplace remove bioexcel
claude plugin marketplace add /path/to/your/biobb/clone
claude plugin install biobb@bioexcel
```

The plugin then loads in place from the clone: edits apply in the next session or after
`/reload-plugins`. For a single session, `claude --plugin-dir /path/to/your/biobb/clone/plugins/biobb`
also works. Check the manifests before pushing:

```bash
claude plugin validate .
claude plugin validate plugins/biobb
```

If you also have personal copies in `~/.claude/skills/add-biobb-block` or
`~/.claude/skills/release-biobb-version`, both load (`/release-biobb-version` and
`/biobb:release-biobb-version`) and can drift apart: delete the personal copies.
