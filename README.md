# Appfilter.xml builder

A python script to generate appfilter.xml file for given app icons.

## Requirements

```bash
pip install beautifulsoup4
```
only to prettify xml file

## How to use

### List all available apps

```python
python builder.py -l
```

### Generate appfilter & appmap files

```python
python builder.py -g /path/to/folder/icons
```
generates appfilter.xml & appmap.xml in current directory

### Check whether app is available in template file

```python
python builder.py -c appname
python builder.py -c amazon
```
