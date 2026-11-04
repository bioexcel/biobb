---
name: add-biobb-block
description: Add a new building block (module) to any biobb package - biobb_pdb_tools, biobb_amber, biobb_analysis, biobb_chemistry, biobb_gromacs, biobb_structure_utils, biobb_vs, biobb_mem, etc. Covers the module docstring contract, conf.yml, unit test, registration, and regenerating JSON schemas / configs / command_line.md / adapters with utils_biobb. Use when asked to implement a module, wrap a new tool as a biobb, or add a block to a biobb package.
---

# Add a building block to a biobb package

Only three things are hand-written: **the module, its `conf.yml` entry, and its unit test**.
JSON schemas, config files and `command_line.md` are *generated* from the module docstring
by `utils_biobb` — never hand-maintain them if the generators can be run.

Layout (`biobb_<pkg>/biobb_<pkg>/`): `<block>/` module folders, `json_schemas/`,
`docs/source/`, `test/{conf.yml,data/,data/config/,reference/,unitests/}`.

## 1. Write the module

Copy the closest existing module **in the same package** and rename — sibling modules
encode that package's conventions (quote style, staging, container support). Fall back to
`biobb_template/biobb_template/template/template.py`, which is the annotated reference.

`biobb_<pkg>/biobb_<pkg>/<block>/<tool_name>.py`:

- Class `ToolName(BiobbObject)`; module-level function `tool_name(...)` returning
  `ToolName(**dict(locals())).launch()`; then `tool_name.__doc__ = ToolName.__doc__` and
  `main = ToolName.get_main(tool_name, "<short description>")` + `if __name__ == "__main__": main()`.
- `__init__`: `super().__init__(properties)`, `self.locals_var_dict = locals().copy()`,
  `self.io_dict = {"in": {...}, "out": {...}}`, one `properties.get(...)` per property
  (including `binary_path` for wrapped executables), then `self.check_init(properties)`
  (older packages: `check_properties` + `check_arguments`).
- `launch()` decorated with `@launchlogger`: `check_restart()` → `stage_files()` → build
  `self.cmd` as a list from `self.stage_io_dict["in"][...]` and `self.io_dict["out"][...]`
  → `run_biobb()` → `copy_to_host()` → `remove_tmp_files()` →
  `check_arguments(output_files_created=True, raise_exception=False)` → `return self.return_code`.
- Log each decision with `fu.log(msg, self.out_log, self.global_log)`.

### The docstring is the contract

The generators parse it, so the format is not cosmetic (full spec:
`utils_biobb/utils_biobb/json/README.md`):

```
| biobb_<pkg> ToolName
| Short description. Mandatory, single line, prefixed by a pipe.
| Long description. Optional.

Args:
    input_file_path (str): Description. File type: input. `Sample file <raw.githubusercontent URL>`_. Accepted formats: pdb (edam:format_1476).
    output_file_path (str) (Optional): Description. File type: output. `Sample file <...>`_. Accepted formats: zip (edam:format_3987).
    properties (dic):
        * **prop** (*str*) - ("default") [1~10|1] Description. Values: a (meaning), b (meaning).
        * **binary_path** (*str*) - ("exe") Path to the exe executable binary.
        * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
        * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

Examples:  (plain Python call, `properties=prop`)
Info:      (wrapped_software: name/version/license; ontology: EDAM)
```

Rules that break generation if ignored: `File type: input|output` on every file argument;
`Accepted formats:` with an `edam:format_XXXX` per format; `(Optional)` right after the
type for optional args; property defaults in parentheses; `[WF property]` for workflow
properties. Sample-file URLs point at files that really exist in the repo
(`.../master/biobb_<pkg>/test/data/<block>/<input>` and `.../test/reference/<block>/<ref>`) —
prefer reusing an existing test file over adding a renamed duplicate.

Docstring lines are long by design; do not reflow them for E501.

## 2. Register it

- `biobb_<pkg>/biobb_<pkg>/<block>/__init__.py` — add the module to `__all__`
  (the generators only see modules listed here).
- `setup.py` — `"<tool_name> = biobb_<pkg>.<block>.<tool_name>:main",` in `console_scripts`
  (some packages prefix the script name, follow the neighbours).
- `biobb_<pkg>/biobb_<pkg>/docs/source/<block>.rst` — `automodule` section, alphabetical.
- `biobb_<pkg>/biobb_<pkg>/json_schemas/biobb_<pkg>.json` — add the block entry
  (`block`, `tool`, `desc`, `exec`, `docs` readthedocs anchor, `"rest": true`); the
  generators leave this file alone.

## 3. Test data and unit test

- Input under `test/data/<block>/`, reference output under `test/reference/<block>/`.
  Generate the reference by running the real tool — never hand-write it.
- `test/conf.yml`: block keyed by the exec/function name, with `paths`
  (`input_...`, `output_...`, `ref_output_...` using `file:test_data_dir/...` and
  `file:test_reference_dir/...`) and `properties`. This drives both the test and the
  generated config files, so put the property values you want documented here.
- `test/unitests/test_<block>/test_<tool_name>.py`: `fx.test_setup(self, '<tool_name>')`,
  then assert `fx.not_empty(...)`, `fx.equal(output, ref)`, `fx.exe_success(returncode)`.

## 4. Regenerate the derived files

From `utils_biobb/utils_biobb` (needs the package's conda env active, plus
`PYTHONPATH` including the `utils_biobb` repo root):

```bash
python3 json/json_generator.py -p biobb_<pkg> -o /path/to/biobb_<pkg>/biobb_<pkg>/
python3 json/json_validator.py -p biobb_<pkg> -i /path/to/biobb_<pkg>/biobb_<pkg>/json_schemas/ -s json/schema/master_schema.json
python3 configs/configs_generator.py -i /path/to/biobb_<pkg>/biobb_<pkg>/test/conf.yml -o /path/to/biobb_<pkg>/biobb_<pkg>/test/data/config/
python3 command_line/command_line_doc_generator.py -j /path/to/biobb_<pkg>/biobb_<pkg>/json_schemas/ -c /path/to/biobb_<pkg>/biobb_<pkg>/test/data/config/ -b biobb_<pkg> -o /path/to/biobb_<pkg>/biobb_<pkg>/docs/source/command_line.md
```

`utils_biobb/utils_biobb/all.sh [biobb_<pkg>]` runs the whole chain (JSON → configs →
command_line.md → CWL/PyCOMPSs/Horus/Galaxy adapters into `biobb_adapters`); its variables
must point at the local repo paths. Adapters live in `biobb_adapters` and are only needed
when that repo is being updated too.

If a generator can't be run (missing env), hand-write the JSON schema, both config files
and the `command_line.md` section by copying a sibling block's output verbatim, and say
so — the next generator run must produce the same content.

Changelog: one concise bullet under `## [Unreleased]` / `### Added` in
`docs/source/change_log.md`, e.g. ``- New `tool` building block: <one line>.`` Leave
released sections in their existing style.

## 5. Verify

The wrapped binary and `pytest` are often absent from the default python. Find an env with
both the binary and `biobb_common`:

```bash
ls ~/miniforge3/envs/*/bin/<binary>
```

Run the test with that env's `bin` prepended to `PATH` — the block shells out to the
binary, so `PATH` matters, not just the interpreter. Without `pytest`, drive the test class
from a scratch script: instantiate it, call `setup_class`, the test method, `teardown_class`.
A pass logs an `RMS:` near zero against the reference. Also sanity-check the CLI:

```bash
python -m biobb_<pkg>.<block>.<tool_name> -h
```
