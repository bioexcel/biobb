# Claude Code skills for biobb

[Claude Code](https://code.claude.com) skills for working on the BioExcel Building Blocks:

| Skill | Use it to |
|---|---|
| [`add-biobb-block`](skills/add-biobb-block/SKILL.md) | Add a building block to a biobb package: module and docstring, `conf.yml`, unit test, registration, and the generated JSON schemas, configs, `command_line.md` and adapters |
| [`release-biobb-version`](skills/release-biobb-version/SKILL.md) | Release a new version of a biobb package: version bump in every file, changelog, tag, PyPI and the Bioconda recipe PR |

Ask in plain words ("add a pdb_fixer block to biobb_pdb_tools", "release biobb_io") and Claude
loads the right skill, or call it directly with `/add-biobb-block` or `/release-biobb-version`.
The release skill publishes (git tags, PyPI, Bioconda PRs): it shows the full diff and asks before
every outward step, and it never types PyPI or GitHub credentials for you.

## Use them in every biobb repository

Claude Code loads `.claude/skills` from the folder where it starts and its parents, but only up
to the repository root. So these skills load in a session started in this repository, but not in
one started in a `biobb/biobb_*` submodule (each is its own repository) or in a standalone clone
of a package. To have them everywhere, link them into your personal skills folder from your clone
of this repository:

```bash
BIOBB=/path/to/your/biobb/clone
mkdir -p ~/.claude/skills
ln -s $BIOBB/.claude/skills/add-biobb-block ~/.claude/skills/add-biobb-block
ln -s $BIOBB/.claude/skills/release-biobb-version ~/.claude/skills/release-biobb-version
```

Start a new Claude Code session afterwards. A personal skill takes precedence over a project skill
with the same name, so inside this repository the linked copy is used, which is the same file.

## Update and edit

The links point at your clone, so `git pull` updates the skills and an edit in
`.claude/skills/<name>/SKILL.md` applies from the next session. Commit and push the edit so other
people get it.

If you had your own copies in `~/.claude/skills/add-biobb-block` or
`~/.claude/skills/release-biobb-version`, replace them with the links: a personal folder with the
same name hides the shared version.
