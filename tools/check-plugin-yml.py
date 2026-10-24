#!/usr/bin/env python3
"""Checks that src/main/resources/plugin.yml parses as YAML once ${project.version} is filled in, the way Maven does.
Run from the project root:  python3 -I tools/check-plugin-yml.py
After `mvn package`, also run:  unzip -l target/NexusDungeons-*.jar | grep plugin.yml   (it must be listed)."""
import sys, yaml

try:
    text = open('src/main/resources/plugin.yml', encoding='utf-8').read().replace('${project.version}', '0.0.0')
    data = yaml.safe_load(text)
except Exception as e:
    print('plugin.yml does not parse:', e)
    sys.exit(1)
for key in ('name', 'main', 'api-version', 'version'):
    if key not in data:
        print('plugin.yml has no', key)
        sys.exit(1)
for name, cmd in (data.get('commands') or {}).items():
    if not isinstance(cmd.get('usage', ''), str):
        print('command', name, 'has a usage that is not text')
        sys.exit(1)
print('plugin.yml parses;', len(data.get('commands') or {}), 'command(s),', len(data.get('permissions') or {}), 'permission(s)')
