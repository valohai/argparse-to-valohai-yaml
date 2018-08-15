argparse-to-valohai-yaml
========================

This tool can be used to bootstrap your Valohai.yaml configuration file
based on a Python `argparse` parser object.

Usage
-----

Temporarily drop `argparse_to_valohai_yaml.py` in your project's directory.

Then, after you've instantiated and configured the `argparse.ArgumentParser`
object (assuming it's named `ap`), but before you do `args = ap.parse_args()`
or similar, add the following:

```python
import argparse_to_valohai_yaml as av
print(av.dump_parameter_defs(ap))
```

The output should be valid YAML you can paste in your `valohai.yaml` file.

With this done, you can remove the code and the copied module.