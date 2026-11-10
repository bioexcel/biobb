---
name: release-biobb-version
description: Release a new version of a biobb package - bump the version across all files, write the changelog, tag and push to GitHub, publish to PyPI, and open the Bioconda recipe PR. Use after adding or changing building blocks in biobb_pdb_tools, biobb_amber, biobb_gromacs, biobb_vs, biobb_mem, etc., when asked to make a new version, cut a release, bump the version, publish to PyPI, or update the bioconda recipe.
---

# Release a new version of a biobb package

The reference procedure is `utils_biobb/utils_biobb/new_version/new_conda_version.sh` (interactive
shell walkthrough) and `new_version/new_version.py` (partially-working automation). Prefer doing
the steps explicitly, in order: the shell script is a checklist, not a black box, and its
`git push` / `twine upload` / branch-delete steps are irreversible.

**This skill publishes. Every step from §5 on is outward-facing.** Do §1–§4 (all local), show the
full diff, and get an explicit go-ahead before tagging, uploading, or pushing anything. Never
enter PyPI or GitHub credentials — if a command prompts for a token, hand the command to the user.

Paths (from `all.sh` / `new_conda_version.sh`, whose defaults are `$HOME/repo/biobb/...`; find
the user's real clones before using them):

```
biobb_dir       = <bioexcel/biobb clone>/biobb             # the biobb packages as submodules
pkg             = $biobb_dir/biobb_<pkg>
utils_biobb     = $biobb_dir/utils_biobb/utils_biobb
bioconda        = <clone of the user's bioconda-recipes>   # a fork of bioconda/bioconda-recipes
```

## 1. Pick the version and the release message

Two independent strings, both needed everywhere:

- **version** `X.Y.Z` — **`X.Y` is not yours to choose: it is the `X.Y` of the pinned
  `biobb_common`.** Every biobb tracks `biobb_common`'s minor line, so a package pinning
  `biobb_common==5.3.1` releases as `5.3.Z` — never `5.4.0`. Only **Z** moves in a normal release,
  whether the change is new building blocks or a dependency refresh.
- **message** `YYYY.N` — the BioExcel release label (`2026.1`, `2025.2`), used verbatim as the git
  commit message, the tag annotation, and the second field of the README `### Version` line.

So the version is *derived*, not proposed:

```bash
grep -n 'version=\|biobb_common' $pkg/setup.py     # current version + the biobb_common pin
git -C $pkg describe --tags --abbrev=0             # last released tag
```

Take `X.Y` from the `biobb_common` pin and `Z` = current `Z` + 1. `Z` is per-package and does not
have to match `biobb_common`'s — `biobb_amber` 5.3.1 and `biobb_analysis` 5.3.0 both pin
`biobb_common==5.3.1`.

Reaching a new `X.Y` is a different job: `biobb_common` releases `5.4.0` first, then each package
re-pins to it and releases its own `5.4.0`. If the user asks for a minor bump while the pin still
says the old line, say so and settle it before editing anything — either the pin moves too (a
`biobb_common` upgrade, and its new version goes in the changelog bullet) or the release is a `Z`.

Confirm the resulting version and message with the user — they are baked into ~10 files and a git
tag.

## 2. Pre-flight, while everything is still local

**Ask whether to re-run the unit tests** — like `new_conda_version.sh`'s
`Do you want to run tests for this repository [Y/n]?` prompt. The suite normally already ran in CI
(`.github/workflows/linting_and_testing.yml` on every push to `master`, `pr-tests.yml` on PRs), so
a local re-run is often redundant and can take a long time for the heavy packages. Check the CI
status for the commit being released instead:

```bash
gh run list --repo bioexcel/biobb_<pkg> --branch master --limit 3
```

Green CI on the release commit is sufficient. Offer the local run when CI is red, was skipped, or
when the change touches something CI ignores — it excludes the container/docker/singularity tests
(`--ignore-glob=*container.py --ignore-glob=*docker.py --ignore-glob=*singularity.py`) and CI runs
without the wrapped binaries some blocks need:

```bash
pytest -s $pkg/biobb_<pkg>/test/unitests
```

Either way, don't publish on a red or unknown test state — say which of the two you relied on.

Then regenerate the derived files, because a release ships them (see the `add-biobb-block` skill
for the generator details). The generators **import the package being released**, so they must run
in the conda env where that package (and therefore `biobb_common`) is installed — normally
`biobb_all`. Activate it, or put its `bin` on `PATH` for the one call:

```bash
conda activate biobb_all                            # env where biobb_<pkg> is installed
$utils_biobb/all.sh biobb_<pkg>                     # JSON schemas → configs → command_line.md → adapters
```

Run from the wrong env, `all.sh` **fails without stopping**: every generator dies on
`ModuleNotFoundError: No module named 'biobb_common'`, the script continues to the next one (with a
stray `all.sh: line 10: [: too many arguments` along the way) and exits 0 having written some
adapter files and no schemas. So don't trust the exit status — grep the log for
`ModuleNotFoundError`, and if you find one, fix the env and re-run before looking at `git status`
(the partial run may have left half-written adapters behind).

At minimum `json_generator.py` + `json_validator.py` must have been run since the last block
change. Check `git status` afterwards: unexpected churn in `json_schemas/` means a docstring
changed and the release notes should mention it.

Also re-check the dependency pins *before* editing versions — `biobb_common` almost always moved:
`setup.py:install_requires`, `.github/env.yaml`, and the bioconda `requirements` must agree.

## 3. Bump the version — every file

`new_conda_version.sh` opens these one by one in the IDE. Edit them directly instead, then diff.

| File | What changes |
|---|---|
| `setup.py` | `version="X.Y.Z"`; `install_requires` pins; `python_requires`; classifiers |
| `biobb_<pkg>/__init__.py` | `__version__ = "X.Y.Z"` |
| `.github/env.yaml` | dependency versions (CI test env) |
| `README.md` | `### Version` → `vX.Y.Z <message>`; the `pip install "…>=X.Y.Z"` and `conda install …>=X.Y.Z` lines; the `quay.io/biocontainers/…:X.Y.Z--pyhdfd78af_0` docker pull/run lines; the singularity `depot.galaxyproject.org` URL and its badge; the `(c) 2015-YYYY` years |
| `biobb_<pkg>/docs/source/readme.md` | verbatim copy — `cp -v README.md biobb_<pkg>/docs/source/readme.md` as the **last** step of this section |
| `biobb_<pkg>/json_schemas/biobb_<pkg>.json` | top-level `"version"`, plus the `"docker"` and `"singularity"` URLs (same `X.Y.Z--pyhdfd78af_0` tag). Leave the `tools` array alone — `json_generator.py` owns it |
| `biobb_<pkg>/docs/source/conf.py` | `version` and `release` (both `X.Y.Z`), `copyright` year |
| `biobb_<pkg>/docs/source/schema.html` | `"softwareVersion"` |

**Do not touch `CITATION.cff`.** The `Sync Citation.cff` workflow (`.github/workflows/citation.yaml`)
overwrites it wholesale from `bioexcel/biobb`'s master copy on every push to `master` and again
every Monday, then commits the result as `github-actions[bot]`. A local edit is reverted, and the
`version:` there tracking a different number than `setup.py` is expected, not a bug to fix. It
changes only when the shared file in `bioexcel/biobb` changes. `new_conda_version.sh` still prompts
to open it — that prompt predates the workflow; skip it.

The `--pyhdfd78af_0` build-string suffix is the bioconda noarch-python build hash; it only becomes
real once bioconda builds the package. Reuse whatever suffix the previous version used and don't
invent one — verify against the previous release's URL in git history.

## 4. Changelog

`docs/source/change_log.md`: promote the `## [Unreleased]` section into a released heading, keeping
the house format exactly:

```markdown
## What's new in version [X.Y.Z](https://github.com/bioexcel/biobb_<pkg>/releases/tag/vX.Y.Z)?

### Changes

* [UPDATE] Update to biobb_common 5.3.1
* New `tool_name` building block: one line.
```

Use the **package's own** repo in that URL — several existing files were copy-pasted from
`biobb_amber` and point at the wrong repo; don't propagate that. Leave a fresh empty
`## [Unreleased]` above it. Draft the bullets from the commits since the last tag:

```bash
git -C $pkg log $(git -C $pkg describe --tags --abbrev=0)..HEAD --oneline | cut -d " " -f 2-1000 | awk '{print "*",$0}'
```

Rewrite that raw list into user-facing bullets — commit subjects like `Update defaults` are not
release notes. Older released sections use `### New features` instead of `### Changes`; leave them
as they are.

**Stop here and show the user the complete diff.** Everything below is published.

## 5. Tag and push GitHub

```bash
git -C $pkg status
git -C $pkg add .
git -C $pkg commit -m "<message>"
git -C $pkg push
git -C $pkg tag -a vX.Y.Z -m "<message>"
git -C $pkg push origin vX.Y.Z
```

The tag is the thing that's awkward to undo — confirm the version string one last time before it
goes up. Some clones also have a `bioexcel` remote alongside `origin`; check `git remote -v` and
push to both if so.

The push to `master` triggers the citation-sync workflow, which may land a
`Updated CITATION.cff` bot commit on top of yours — `git pull` before any follow-up push (§8).

## 6. PyPI

```bash
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*
```

Ask before running the upload — a version number on PyPI can never be reused, only yanked. If
twine prompts for a token, stop and let the user run it. Then clean up:

```bash
rm -rfv biobb_<pkg>.egg-info dist build
```

Keep the sdist tarball's hash before deleting `dist/` — it's the same file bioconda will download:

```bash
sha256sum dist/biobb_<pkg>-X.Y.Z.tar.gz
```

If `dist/` is already gone, take it from the PyPI "Download files" page, or:

```bash
curl -sL https://pypi.io/packages/source/b/biobb_<pkg>/biobb_<pkg>-X.Y.Z.tar.gz | sha256sum
```

(PyPI needs a minute to serve a fresh upload; a 404 means retry, not a bad version.)

## 7. Bioconda recipe PR

`$bioconda`'s `origin` is the user's **fork**, with no `upstream` remote. Sync the fork's master
first, otherwise the branch is cut from a stale tree:

```bash
gh repo sync <user>/bioconda-recipes -b master
git -C $bioconda checkout -f master && git -C $bioconda pull origin master
```

The script then force-deletes the per-package branch on both sides. That branch holds the previous
release's PR — **confirm the previous PR was merged or closed before deleting it**, and note that
`checkout -f` discards uncommitted work in that clone:

```bash
git -C $bioconda branch -D biobb_<pkg>
git -C $bioconda push origin --delete biobb_<pkg>
git -C $bioconda checkout -b biobb_<pkg>
```

Edit `recipes/biobb_<pkg>/meta.yaml`:

- `{% set version = "X.Y.Z" %}`
- `sha256:` → the hash from §6
- `build: number: 0` — reset it; it only increments for rebuilds of an unchanged version
- `requirements.host` / `requirements.run` — mirror `setup.py`'s `install_requires` and
  `python_requires` exactly (this is the dependency drift the script's prompt is warning about)
- `test.imports` — add any new subpackage
- `about.summary` / `about.description` — regenerate from the new `README.md` if it changed;
  `description` is the README as an escaped YAML string, copyright years included

Then:

```bash
git -C $bioconda add recipes/biobb_<pkg>/
git -C $bioconda status
git -C $bioconda commit -m "[biobb_<pkg>] update X.Y.Z"
git -C $bioconda push -u origin biobb_<pkg>
```

Open the PR against `bioconda/bioconda-recipes:master` — ask before creating it, since it's a PR to
a third-party repo:

```bash
gh pr create --repo bioconda/bioconda-recipes --base master --head <user>:biobb_<pkg> --title "[biobb_<pkg>] update X.Y.Z" --body-file <body.md>
```

or hand the user the URL `https://github.com/bioconda/bioconda-recipes/pull/new/biobb_<pkg>`.

The body is bioconda's own template, `$bioconda/.github/PULL_REQUEST_TEMPLATE.md`: replace its first
line ("Describe your pull request here") with one sentence on the release (what changed, and
whether dependencies or `run_exports` moved) and keep the rest verbatim.

After opening it, offer Auto-fix on the PR (it wakes the session on failures only), and **notify
the user once every check has passed** — that's when they comment `@BiocondaBot please add label`
to request review. Ignore the `Mergify Merge Queue` check: it stays `skipping`/pending until a
maintainer queues the PR, so it never completes and `gh pr checks --watch` never returns. Judge the
other checks (`Lint`, `Linux Tests`, `OSX-64 Tests`, `build and test (ARM)`, `Summary`):

```bash
gh pr checks <N> --repo bioconda/bioconda-recipes | grep -v '^Mergify Merge Queue'
```

All `pass` → send the notification. Any `fail` → Auto-fix handles it. Still `pending` → wait for
the next event; the Linux tests take ~15 min.

## 8. After the bioconda PR merges

Bioconda's CI builds the conda package, and the biocontainers docker/singularity images appear
some hours later. Verify the URLs already written in §3 actually resolve — a different build
string means `README.md` and `biobb_<pkg>.json` need a follow-up commit. Also check readthedocs
picked up the new tag. Do not create a GitHub release: biobb only pushes tags (the changelog URL
`releases/tag/vX.Y.Z` opens the tag page without one).

## Multi-package releases

A `biobb_common` bump cascades: release `biobb_common` first, wait for it on bioconda, then run
§1–§7 per dependent package with the same `message`. `all.sh` with no arguments lists the packages
in that release set. Do them one at a time and confirm each — do not loop the publish steps
unattended.
